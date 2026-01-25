# Rapportera Temperatur till Temperatur.nu

En Home Assistant-integration för automatisk temperaturrapportering till Temperatur.nu med stöd för flera sensorer och intelligent aggregering.

## Konfiguration

Efter installation via HACS:

1. Gå till **Inställningar** → **Enheter & tjänster**
2. Klicka på **+ LÄGG TILL INTEGRATION**
3. Sök efter "Rapportera Temperatur"
4. Ange din hash-kod från Temperatur.nu
5. Välj 1-3 temperatursensorer
6. Välj aggregeringsmetod (minimum eller medelvärde)
7. Ange rapporteringsintervall (1-60 minuter)

## Funktioner

**Multi-sensor support (v1.3.0)**
- Välj upp till 3 temperatursensorer samtidigt
- Minimum-aggregering: Garanterar skuggtemperatur genom att använda lägsta värdet
- Medelvärde-aggregering: Beräknar genomsnittlig temperatur

**Sensorer**
- Statussensor: Visar rapporteringsstatus och individuella sensortemperaturer
- Temperatursensor: Aggregerad temperatur tillgänglig för automationer och grafer

**Konfiguration**
- GUI-baserad setup via config flow
- Konfigurerbart rapporteringsintervall (1-60 minuter)
- Inga YAML-filer krävs

**Felhantering (v1.3.1)**
- Robust hantering av saknade eller felaktiga sensorvärden
- Automatisk övergång mellan gamla och nya konfigurationer
- Förbättrad loggning vid konfigurationsfel

## Version

Nuvarande version: 1.3.1 (2026-01-18)

Se [CHANGELOG.md](https://github.com/frodr1k/RapporteraTempHA/blob/main/CHANGELOG.md) för fullständig versionshistorik.

## Support

Rapportera problem på [GitHub Issues](https://github.com/frodr1k/RapporteraTempHA/issues)
