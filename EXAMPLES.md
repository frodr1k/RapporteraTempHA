# Exempel - Get-TempDBHAStatus.ps1

Detta dokument innehåller praktiska exempel på hur du använder `Get-TempDBHAStatus.ps1` i olika scenarier.

## Grundläggande Användning

### Exempel 1: Analysera en enskild server

```powershell
.\Get-TempDBHAStatus.ps1 -SqlInstance "SERVER01"
```

**Output:**
```
════════════════════════════════════════════════════════════
  TempDB HIGH AVAILABILITY STATUS RAPPORT
════════════════════════════════════════════════════════════

🔍 Analyserar 1 server(s)

[1/1] 🖥️  Analyserar: SERVER01
   ✅ Bra - Score: 100% - 8 TempDB-filer

════════════════════════════════════════════════════════════
  SAMMANFATTNING
════════════════════════════════════════════════════════════

📊 Totalt antal servrar: 1
✅ Lyckade: 1

📈 Best Practice Score:
   Genomsnitt: 100%
   ✅ Bra (80-100%): 1 servrar
```

### Exempel 2: Flera servrar samtidigt

```powershell
.\Get-TempDBHAStatus.ps1 -SqlInstance "SERVER01","SERVER02","SERVER03"
```

### Exempel 3: Med SQL Server-autentisering

```powershell
$cred = Get-Credential
.\Get-TempDBHAStatus.ps1 -SqlInstance "SERVER01" -Credential $cred
```

## CMS-integration

### Exempel 4: Analysera hela CMS-grupp

```powershell
.\Get-TempDBHAStatus.ps1 -CMSServer "DBACMS" -CMSGroup "active\prod"
```

### Exempel 5: Olika CMS-grupper

```powershell
# Produktionsservrar
.\Get-TempDBHAStatus.ps1 -CMSServer "DBACMS" -CMSGroup "active\prod" -ExportPath "C:\Rapporter\Prod_TempDB.xlsx"

# Test-servrar
.\Get-TempDBHAStatus.ps1 -CMSServer "DBACMS" -CMSGroup "active\test" -ExportPath "C:\Rapporter\Test_TempDB.xlsx"

# Icke-prod
.\Get-TempDBHAStatus.ps1 -CMSServer "DBACMS" -CMSGroup "active\ickeprod" -ExportPath "C:\Rapporter\IckeProd_TempDB.xlsx"
```

## Export och Rapportering

### Exempel 6: Export till Excel

```powershell
.\Get-TempDBHAStatus.ps1 `
    -CMSServer "DBACMS" `
    -CMSGroup "active\prod" `
    -ExportPath "C:\Rapporter\TempDB_$(Get-Date -Format 'yyyy-MM-dd').xlsx"
```

**Excel-filen innehåller:**
- **Detaljerad** - All information om TempDB-filer
- **Server-summering** - Översikt per server
- **Fel** - Eventuella fel som uppstod

### Exempel 7: Schemalagd rapport

```powershell
# Skapa schemalagt task som körs varje måndag kl 08:00
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 8am
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" `
    -Argument "-File C:\Scripts\Get-TempDBHAStatus.ps1 -CMSServer DBACMS -CMSGroup 'active\prod' -ExportPath C:\Rapporter\TempDB_Weekly.xlsx"

Register-ScheduledTask -TaskName "TempDB HA Status - Veckorapport" `
    -Trigger $trigger `
    -Action $action `
    -Description "Veckovis TempDB HA-statusrapport"
```

## Avancerade Scenarier

### Exempel 8: Filtrera servrar med problem

```powershell
# Kör analys
.\Get-TempDBHAStatus.ps1 -CMSServer "DBACMS" -CMSGroup "active\prod" -ExportPath "C:\Temp\TempDB.xlsx"

# Läs Excel och filtrera servrar med låg score
Install-Module ImportExcel -Scope CurrentUser
$data = Import-Excel -Path "C:\Temp\TempDB.xlsx" -WorksheetName "Server-summering"
$problemServers = $data | Where-Object { $_.BestPracticeScore -lt 80 }

# Visa servrar med problem
$problemServers | Format-Table Server, BestPracticeScore, Status, IssueCount
```

### Exempel 9: Jämföra flera miljöer

```powershell
# Analysera alla miljöer
$environments = @(
    @{ Name = "Prod"; Group = "active\prod" }
    @{ Name = "Test"; Group = "active\test" }
    @{ Name = "Dev"; Group = "active\dev" }
)

foreach ($env in $environments) {
    Write-Host "`nAnalyserar $($env.Name)..." -ForegroundColor Cyan
    
    .\Get-TempDBHAStatus.ps1 `
        -CMSServer "DBACMS" `
        -CMSGroup $env.Group `
        -ExportPath "C:\Rapporter\TempDB_$($env.Name)_$(Get-Date -Format 'yyyy-MM-dd').xlsx"
}
```

### Exempel 10: Automatisk åtgärd vid problem

```powershell
# Kör analys
.\Get-TempDBHAStatus.ps1 -SqlInstance "SERVER01" -ExportPath "C:\Temp\TempDB.xlsx"

# Läs resultat
$summary = Import-Excel -Path "C:\Temp\TempDB.xlsx" -WorksheetName "Server-summering"

# Skicka email om problem
if ($summary.BestPracticeScore -lt 80) {
    $mailParams = @{
        To = "dba-team@company.com"
        From = "monitoring@company.com"
        Subject = "⚠️ TempDB Problem - $($summary.Server)"
        Body = @"
Server: $($summary.Server)
Best Practice Score: $($summary.BestPracticeScore)%
Antal problem: $($summary.IssueCount)

Se bifogad rapport för detaljer.
"@
        Attachments = "C:\Temp\TempDB.xlsx"
        SmtpServer = "smtp.company.com"
    }
    
    Send-MailMessage @mailParams
}
```

### Exempel 11: PowerShell Pipeline

```powershell
# Hämta servrar från CMS och analysera en i taget
Get-DbaRegisteredServer -SqlInstance "DBACMS" -Group "active\prod" |
    ForEach-Object {
        Write-Host "Analyserar $($_.ServerName)..."
        .\Get-TempDBHAStatus.ps1 -SqlInstance $_.ServerName
    }
```

### Exempel 12: Endast visa kritiska servrar

```powershell
# Kör analys och spara output
$output = .\Get-TempDBHAStatus.ps1 -CMSServer "DBACMS" -CMSGroup "active\prod" -ExportPath "C:\Temp\TempDB.xlsx" 

# Importera och filtrera
$data = Import-Excel -Path "C:\Temp\TempDB.xlsx" -WorksheetName "Server-summering"
$critical = $data | Where-Object { $_.BestPracticeScore -lt 60 }

if ($critical.Count -gt 0) {
    Write-Host "`n🚨 KRITISKA SERVRAR:" -ForegroundColor Red
    $critical | Format-Table Server, BestPracticeScore, IssueCount, Status -AutoSize
}
```

## Felsökning

### Exempel 13: Testa anslutning först

```powershell
# Testa om du kan ansluta till server
Test-DbaConnection -SqlInstance "SERVER01"

# Om det fungerar, kör analysen
if (Test-DbaConnection -SqlInstance "SERVER01") {
    .\Get-TempDBHAStatus.ps1 -SqlInstance "SERVER01"
} else {
    Write-Warning "Kan inte ansluta till SERVER01"
}
```

### Exempel 14: Debug-läge

```powershell
# Kör med verbose output
.\Get-TempDBHAStatus.ps1 -SqlInstance "SERVER01" -Verbose

# Eller med debug
.\Get-TempDBHAStatus.ps1 -SqlInstance "SERVER01" -Debug
```

### Exempel 15: Hantera fel

```powershell
try {
    .\Get-TempDBHAStatus.ps1 -CMSServer "DBACMS" -CMSGroup "active\prod" -ExportPath "C:\Rapporter\TempDB.xlsx"
}
catch {
    Write-Error "Analys misslyckades: $($_.Exception.Message)"
    
    # Logga fel
    $errorLog = @{
        Timestamp = Get-Date
        Error = $_.Exception.Message
        StackTrace = $_.ScriptStackTrace
    }
    
    $errorLog | Export-Csv -Path "C:\Logs\TempDB_Errors.csv" -Append -NoTypeInformation
}
```

## Best Practices för Regelbunden Övervakning

### Exempel 16: Komplett övervakningslösning

```powershell
# Script: Monitor-TempDB.ps1
param(
    [string]$ReportPath = "C:\Rapporter",
    [string]$CMSServer = "DBACMS",
    [string[]]$Groups = @("active\prod", "active\test")
)

$timestamp = Get-Date -Format "yyyy-MM-dd_HHmm"
$results = @()

foreach ($group in $Groups) {
    $groupName = $group -replace '\\', '_'
    $excelPath = Join-Path $ReportPath "TempDB_${groupName}_${timestamp}.xlsx"
    
    Write-Host "`nAnalyserar grupp: $group" -ForegroundColor Cyan
    
    .\Get-TempDBHAStatus.ps1 -CMSServer $CMSServer -CMSGroup $group -ExportPath $excelPath
    
    # Spara resultat för sammanställning
    $summary = Import-Excel -Path $excelPath -WorksheetName "Server-summering"
    $results += $summary
}

# Skapa sammanställd rapport
$consolidatedPath = Join-Path $ReportPath "TempDB_AllEnvironments_${timestamp}.xlsx"
$results | Export-Excel -Path $consolidatedPath -WorksheetName "Sammanställning" -AutoSize -BoldTopRow

Write-Host "`n✅ Alla rapporter klara!" -ForegroundColor Green
Write-Host "📁 Sammanställd rapport: $consolidatedPath" -ForegroundColor White
```

---

## Tips och Tricks

1. **Använd alltid absoluta sökvägar** för exportfiler
2. **Schemalägg rapporter** för regelbunden övervakning
3. **Kombinera med andra dbatools-cmdlets** för komplett analys
4. **Spara historiska rapporter** för trendanalys
5. **Integrera med ITSM-system** för automatisk ärendehantering

## Relaterade Cmdlets

```powershell
# Komplettera med andra dbatools-cmdlets
Get-DbaTempdbUsage -SqlInstance "SERVER01"
Test-DbaTempdbConfiguration -SqlInstance "SERVER01"
Set-DbaTempdbConfig -SqlInstance "SERVER01"
```

---

**💡 Har du fler användbara exempel? Bidra gärna med en Pull Request!**
