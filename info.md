# Rapportera Temperatur till Temperatur.nu

Denna integration gör det möjligt att automatiskt rapportera temperatur från valfri sensor i Home Assistant till Temperatur.nu.

## Konfiguration

Efter installation via HACS:

1. Gå till **Inställningar** → **Enheter & tjänster**
2. Klicka på **+ LÄGG TILL INTEGRATION**
3. Sök efter "Rapportera Temperatur"
4. Ange din hash-kod från Temperatur.nu
5. Välj den temperatursensor du vill rapportera från
6. Välj rapporteringsintervall (standard är 5 minuter)

## Funktioner

- **GUI-first**: All konfiguration sker via Home Assistants GUI
- **Flexibel sensorval**: Välj valfri temperatursensor från dropdown
- **Konfigurerbart intervall**: Välj hur ofta temperaturen ska rapporteras (1-60 minuter)
- **Statussensor**: En sensor skapas som visar status för rapporteringen
- **Loggar**: All aktivitet loggas i Home Assistant-loggen

## Support

Rapportera problem på [GitHub Issues](https://github.com/frodr1k/RapporteraTempHA/issues)
