<#
.SYNOPSIS
    Rapporterar TempDB High Availability-status för SQL Server-instanser.

.DESCRIPTION
    Detta script analyserar TempDB-konfiguration och HA-status för SQL Server-instanser.
    Det kan köras mot enskilda servrar eller hela grupper via Central Management Server (CMS).
    
    Scriptet kontrollerar:
    - TempDB-filantal och om det matchar best practices (1 fil per CPU-kärna, max 8)
    - Filstorlekar och om alla filer har samma storlek
    - Tillväxtinställningar (bör vara MB, inte %)
    - HA-konfiguration (Always On Availability Groups, Mirroring, etc.)
    - Filplacering och rekommendationer

.PARAMETER SqlInstance
    En eller flera SQL Server-instanser att analysera.
    Exempel: "SERVER01", "SERVER01\INSTANCE01"

.PARAMETER CMSServer
    Central Management Server att hämta serverlista från.
    Exempel: "DBACMS"

.PARAMETER CMSGroup
    CMS-grupp att analysera. Används tillsammans med CMSServer.
    Exempel: "active\prod", "active\ickeprod"

.PARAMETER ExportPath
    Sökväg för Excel-export. Om inte anges, visas endast konsolutput.
    Exempel: "C:\Rapporter\TempDB_HA_Status.xlsx"

.PARAMETER Credential
    PSCredential-objekt för SQL Server-autentisering.
    Om inte anges används Windows-autentisering.

.EXAMPLE
    .\Get-TempDBHAStatus.ps1 -SqlInstance "SERVER01"
    Analyserar TempDB på en enskild server.

.EXAMPLE
    .\Get-TempDBHAStatus.ps1 -CMSServer "DBACMS" -CMSGroup "active\prod"
    Analyserar alla servrar i CMS-gruppen "active\prod".

.EXAMPLE
    .\Get-TempDBHAStatus.ps1 -CMSServer "DBACMS" -CMSGroup "active\prod" -ExportPath "C:\Rapporter\TempDB_Status.xlsx"
    Analyserar servrar och exporterar till Excel.

.NOTES
    Författare: Fredrik Elmqvist
    Email: fe@mintv.nu
    Datum: 2026-01-09
    Version: 1.0.0
    
    Kräver:
    - PowerShell 5.1 eller senare
    - dbatools-modul
    - ImportExcel-modul (valfri, CSV används som fallback)
#>

[CmdletBinding(DefaultParameterSetName = 'Direct')]
param(
    [Parameter(Mandatory = $true, 
               ParameterSetName = 'Direct',
               HelpMessage = "En eller flera SQL Server-instanser")]
    [string[]]$SqlInstance,
    
    [Parameter(Mandatory = $true,
               ParameterSetName = 'CMS',
               HelpMessage = "Central Management Server")]
    [string]$CMSServer,
    
    [Parameter(Mandatory = $true,
               ParameterSetName = 'CMS',
               HelpMessage = "CMS-grupp att analysera")]
    [string]$CMSGroup,
    
    [Parameter(Mandatory = $false)]
    [string]$ExportPath,
    
    [Parameter(Mandatory = $false)]
    [PSCredential]$Credential
)

#Requires -Module dbatools

# Importera dbatools
Import-Module dbatools -ErrorAction Stop

# Funktion för att skriva färgad text
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$ForegroundColor = "White"
    )
    Write-Host $Message -ForegroundColor $ForegroundColor
}

# Funktion för att skriva progressbar
function Write-ProgressBar {
    param(
        [int]$Current,
        [int]$Total,
        [string]$Activity,
        [string]$Status
    )
    
    $percentComplete = ($Current / $Total) * 100
    Write-Progress -Activity $Activity `
                   -Status $Status `
                   -PercentComplete $percentComplete `
                   -CurrentOperation "[$Current/$Total]"
}

# Funktion för att kontrollera TempDB best practices
function Test-TempDBBestPractices {
    param(
        [object[]]$TempDBFiles,
        [int]$CPUCount
    )
    
    $issues = @()
    $recommendations = @()
    
    # Kontrollera antal filer
    $dataFileCount = ($TempDBFiles | Where-Object { $_.Type -eq 0 }).Count
    $recommendedFileCount = [Math]::Min($CPUCount, 8)
    
    if ($dataFileCount -ne $recommendedFileCount) {
        $issues += "Antal TempDB-filer ($dataFileCount) matchar inte rekommenderat antal ($recommendedFileCount)"
        $recommendations += "Skapa $($recommendedFileCount - $dataFileCount) fler TempDB-datafiler"
    }
    
    # Kontrollera om alla filer har samma storlek
    $dataFiles = $TempDBFiles | Where-Object { $_.Type -eq 0 }
    $sizes = $dataFiles | Select-Object -ExpandProperty Size -Unique
    
    if ($sizes.Count -gt 1) {
        $issues += "TempDB-filer har olika storlekar"
        $recommendations += "Sätt alla TempDB-filer till samma storlek: $([Math]::Max($sizes)) MB"
    }
    
    # Kontrollera tillväxtinställningar
    foreach ($file in $dataFiles) {
        if ($file.GrowthType -eq 'Percent') {
            $issues += "Fil '$($file.Name)' använder procentuell tillväxt"
            $recommendations += "Ändra tillväxt för '$($file.Name)' till MB istället för %"
        }
    }
    
    return @{
        Issues = $issues
        Recommendations = $recommendations
        Score = if ($issues.Count -eq 0) { 100 } else { [Math]::Max(0, 100 - ($issues.Count * 20)) }
    }
}

# SQL Query för att hämta TempDB-information
$tempDBQuery = @"
SELECT 
    @@SERVERNAME AS ServerName,
    DB_NAME(database_id) AS DatabaseName,
    name AS FileName,
    type_desc AS FileType,
    physical_name AS PhysicalPath,
    size * 8.0 / 1024 AS SizeMB,
    CASE 
        WHEN is_percent_growth = 1 THEN CAST(growth AS VARCHAR) + '%'
        ELSE CAST(growth * 8.0 / 1024 AS VARCHAR) + ' MB'
    END AS Growth,
    is_percent_growth AS IsPercentGrowth,
    file_id AS FileId
FROM sys.master_files
WHERE database_id = 2  -- TempDB
ORDER BY type, file_id;
"@

# SQL Query för att hämta CPU-information
$cpuQuery = @"
SELECT 
    cpu_count AS CPUCount,
    hyperthread_ratio AS HyperthreadRatio,
    cpu_count / hyperthread_ratio AS PhysicalCPUCount
FROM sys.dm_os_sys_info;
"@

# SQL Query för att hämta HA-information
$haQuery = @"
SELECT 
    SERVERPROPERTY('IsHadrEnabled') AS IsAlwaysOnEnabled,
    CASE 
        WHEN EXISTS (SELECT 1 FROM sys.availability_groups) THEN 1
        ELSE 0
    END AS HasAvailabilityGroups,
    CASE 
        WHEN EXISTS (SELECT 1 FROM sys.database_mirroring WHERE mirroring_guid IS NOT NULL) THEN 1
        ELSE 0
    END AS HasMirroring,
    SERVERPROPERTY('IsClustered') AS IsClustered
"@

# Huvudlogik
try {
    Write-ColorOutput "`n════════════════════════════════════════════════════════════" "Cyan"
    Write-ColorOutput "  TempDB HIGH AVAILABILITY STATUS RAPPORT" "Cyan"
    Write-ColorOutput "════════════════════════════════════════════════════════════`n" "Cyan"
    
    # Hämta serverlista
    $servers = @()
    
    if ($PSCmdlet.ParameterSetName -eq 'CMS') {
        Write-ColorOutput "🔍 Hämtar servrar från CMS: $CMSServer" "Yellow"
        Write-ColorOutput "   Grupp: $CMSGroup" "Yellow"
        
        $cmsServers = Get-DbaRegisteredServer -SqlInstance $CMSServer -Group $CMSGroup
        $servers = $cmsServers.ServerName
        
        Write-ColorOutput "   Hittade $($servers.Count) servrar`n" "Green"
    }
    else {
        $servers = $SqlInstance
        Write-ColorOutput "🔍 Analyserar $($servers.Count) server(s)`n" "Yellow"
    }
    
    if ($servers.Count -eq 0) {
        Write-ColorOutput "❌ Inga servrar hittades!" "Red"
        return
    }
    
    # Samla resultat
    $allResults = @()
    $summaryResults = @()
    $errorResults = @()
    
    $counter = 0
    
    foreach ($server in $servers) {
        $counter++
        
        Write-ProgressBar -Current $counter -Total $servers.Count `
                         -Activity "Analyserar TempDB HA-status" `
                         -Status "Server: $server"
        
        Write-ColorOutput "[$counter/$($servers.Count)] 🖥️  Analyserar: $server" "Cyan"
        
        try {
            # Anslut till server
            $connectParams = @{
                SqlInstance = $server
                Database = 'master'
                EnableException = $true
            }
            
            if ($Credential) {
                $connectParams['SqlCredential'] = $Credential
            }
            
            # Hämta TempDB-information
            $tempDBFiles = Invoke-DbaQuery @connectParams -Query $tempDBQuery
            
            # Hämta CPU-information
            $cpuInfo = Invoke-DbaQuery @connectParams -Query $cpuQuery
            
            # Hämta HA-information
            $haInfo = Invoke-DbaQuery @connectParams -Query $haQuery
            
            # Best practices-analys
            $analysis = Test-TempDBBestPractices -TempDBFiles $tempDBFiles -CPUCount $cpuInfo.CPUCount
            
            # Bygg resultat för varje fil
            foreach ($file in $tempDBFiles) {
                $result = [PSCustomObject]@{
                    Server = $server
                    DatabaseName = $file.DatabaseName
                    FileName = $file.FileName
                    FileType = $file.FileType
                    PhysicalPath = $file.PhysicalPath
                    SizeMB = [Math]::Round($file.SizeMB, 2)
                    Growth = $file.Growth
                    IsPercentGrowth = $file.IsPercentGrowth
                    CPUCount = $cpuInfo.CPUCount
                    PhysicalCPUCount = $cpuInfo.PhysicalCPUCount
                    IsAlwaysOnEnabled = $haInfo.IsAlwaysOnEnabled
                    HasAvailabilityGroups = $haInfo.HasAvailabilityGroups
                    HasMirroring = $haInfo.HasMirroring
                    IsClustered = $haInfo.IsClustered
                    BestPracticeScore = $analysis.Score
                    Issues = ($analysis.Issues -join '; ')
                    Recommendations = ($analysis.Recommendations -join '; ')
                }
                $allResults += $result
            }
            
            # Summering per server
            $dataFileCount = ($tempDBFiles | Where-Object { $_.FileType -eq 'ROWS' }).Count
            $totalSizeMB = ($tempDBFiles | Where-Object { $_.FileType -eq 'ROWS' } | Measure-Object -Property SizeMB -Sum).Sum
            
            $summary = [PSCustomObject]@{
                Server = $server
                TempDBFileCount = $dataFileCount
                TotalSizeMB = [Math]::Round($totalSizeMB, 2)
                CPUCount = $cpuInfo.CPUCount
                RecommendedFileCount = [Math]::Min($cpuInfo.CPUCount, 8)
                IsAlwaysOnEnabled = $haInfo.IsAlwaysOnEnabled
                HasAvailabilityGroups = $haInfo.HasAvailabilityGroups
                IsClustered = $haInfo.IsClustered
                BestPracticeScore = $analysis.Score
                IssueCount = $analysis.Issues.Count
                Status = if ($analysis.Score -ge 80) { "✅ Bra" } elseif ($analysis.Score -ge 60) { "⚠️ Varning" } else { "❌ Kritisk" }
            }
            $summaryResults += $summary
            
            # Visa status
            $statusColor = if ($analysis.Score -ge 80) { "Green" } elseif ($analysis.Score -ge 60) { "Yellow" } else { "Red" }
            Write-ColorOutput "   $($summary.Status) - Score: $($analysis.Score)% - $dataFileCount TempDB-filer" $statusColor
            
            if ($analysis.Issues.Count -gt 0) {
                Write-ColorOutput "   ⚠️  Problem: $($analysis.Issues.Count)" "Yellow"
            }
        }
        catch {
            $errorResults += [PSCustomObject]@{
                Server = $server
                Error = $_.Exception.Message
                Timestamp = Get-Date
            }
            
            Write-ColorOutput "   ❌ Fel: $($_.Exception.Message)" "Red"
        }
    }
    
    Write-Progress -Activity "Analyserar TempDB HA-status" -Completed
    
    # Sammanfattning
    Write-ColorOutput "`n════════════════════════════════════════════════════════════" "Cyan"
    Write-ColorOutput "  SAMMANFATTNING" "Cyan"
    Write-ColorOutput "════════════════════════════════════════════════════════════`n" "Cyan"
    
    $successCount = $summaryResults.Count
    $errorCount = $errorResults.Count
    $totalServers = $servers.Count
    
    Write-ColorOutput "📊 Totalt antal servrar: $totalServers" "White"
    Write-ColorOutput "✅ Lyckade: $successCount" "Green"
    
    if ($errorCount -gt 0) {
        Write-ColorOutput "❌ Misslyckade: $errorCount" "Red"
    }
    
    # Statistik
    $avgScore = ($summaryResults | Measure-Object -Property BestPracticeScore -Average).Average
    $criticalServers = ($summaryResults | Where-Object { $_.BestPracticeScore -lt 60 }).Count
    $warningServers = ($summaryResults | Where-Object { $_.BestPracticeScore -ge 60 -and $_.BestPracticeScore -lt 80 }).Count
    $goodServers = ($summaryResults | Where-Object { $_.BestPracticeScore -ge 80 }).Count
    
    Write-ColorOutput "`n📈 Best Practice Score:" "White"
    Write-ColorOutput "   Genomsnitt: $([Math]::Round($avgScore, 1))%" "White"
    Write-ColorOutput "   ✅ Bra (80-100%): $goodServers servrar" "Green"
    
    if ($warningServers -gt 0) {
        Write-ColorOutput "   ⚠️  Varning (60-79%): $warningServers servrar" "Yellow"
    }
    
    if ($criticalServers -gt 0) {
        Write-ColorOutput "   ❌ Kritisk (<60%): $criticalServers servrar" "Red"
    }
    
    # HA-statistik
    $alwaysOnCount = ($summaryResults | Where-Object { $_.IsAlwaysOnEnabled -eq 1 }).Count
    $clusteredCount = ($summaryResults | Where-Object { $_.IsClustered -eq 1 }).Count
    
    Write-ColorOutput "`n🏢 High Availability:" "White"
    Write-ColorOutput "   Always On aktiverat: $alwaysOnCount servrar" "White"
    Write-ColorOutput "   Clustered: $clusteredCount servrar" "White"
    
    # Export
    if ($ExportPath) {
        Write-ColorOutput "`n📤 Exporterar till Excel: $ExportPath" "Yellow"
        
        # Kontrollera om ImportExcel finns
        $hasImportExcel = Get-Module -ListAvailable -Name ImportExcel
        
        if (-not $hasImportExcel) {
            Write-ColorOutput "WARNING: ImportExcel-modulen saknas. Installerar..." "Yellow"
            try {
                Install-Module -Name ImportExcel -Scope CurrentUser -Force -AllowClobber
                $hasImportExcel = $true
            }
            catch {
                Write-ColorOutput "   ⚠️  Kunde inte installera ImportExcel. Exporterar till CSV istället." "Yellow"
                $hasImportExcel = $false
            }
        }
        
        if ($hasImportExcel) {
            # Export till Excel med flera flikar
            $allResults | Export-Excel -Path $ExportPath `
                                       -WorksheetName "Detaljerad" `
                                       -AutoSize `
                                       -FreezeTopRow `
                                       -BoldTopRow `
                                       -ClearSheet
            
            Write-ColorOutput "   ✅ Detaljerad rapport exporterad ($($allResults.Count) rader)" "Green"
            
            $summaryResults | Export-Excel -Path $ExportPath `
                                          -WorksheetName "Server-summering" `
                                          -AutoSize `
                                          -FreezeTopRow `
                                          -BoldTopRow
            
            Write-ColorOutput "   ✅ Server-summering exporterad ($($summaryResults.Count) rader)" "Green"
            
            if ($errorResults.Count -gt 0) {
                $errorResults | Export-Excel -Path $ExportPath `
                                            -WorksheetName "Fel" `
                                            -AutoSize `
                                            -FreezeTopRow `
                                            -BoldTopRow
                
                Write-ColorOutput "   ⚠️  Fel-logg exporterad ($($errorResults.Count) rader)" "Yellow"
            }
            
            Write-ColorOutput "`n✅ Export klar!" "Green"
            Write-ColorOutput "📁 Fil: $ExportPath" "White"
            
            # Öppna Excel
            Write-ColorOutput "`n🚀 Öppnar Excel..." "Yellow"
            Start-Process -FilePath $ExportPath
        }
        else {
            # Fallback till CSV
            $csvPath = $ExportPath -replace '\.xlsx$', '_Detaljerad.csv'
            $summaryPath = $ExportPath -replace '\.xlsx$', '_Summering.csv'
            $errorPath = $ExportPath -replace '\.xlsx$', '_Fel.csv'
            
            $allResults | Export-Csv -Path $csvPath -NoTypeInformation -Encoding UTF8
            Write-ColorOutput "   ✅ Detaljerad rapport: $csvPath" "Green"
            
            $summaryResults | Export-Csv -Path $summaryPath -NoTypeInformation -Encoding UTF8
            Write-ColorOutput "   ✅ Server-summering: $summaryPath" "Green"
            
            if ($errorResults.Count -gt 0) {
                $errorResults | Export-Csv -Path $errorPath -NoTypeInformation -Encoding UTF8
                Write-ColorOutput "   ⚠️  Fel-logg: $errorPath" "Yellow"
            }
        }
    }
    
    Write-ColorOutput "`n════════════════════════════════════════════════════════════" "Cyan"
    Write-ColorOutput "  KLART!" "Cyan"
    Write-ColorOutput "════════════════════════════════════════════════════════════`n" "Cyan"
}
catch {
    Write-ColorOutput "`n❌ KRITISKT FEL: $($_.Exception.Message)" "Red"
    Write-ColorOutput $_.ScriptStackTrace "Red"
    throw
}
