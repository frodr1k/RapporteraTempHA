# Rapportera Temperatur till Temperatur.nu

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

En Home Assistant-integration för att automatiskt rapportera temperatur till Temperatur.nu.

## Installation via HACS

1. Öppna HACS i Home Assistant
2. Klicka på "Integrations"
3. Klicka på menyn längst upp till höger (tre prickar)
4. Välj "Custom repositories"
5. Lägg till URL:en: `https://github.com/frodr1k/RapporteraTempHA`
6. Välj kategori: "Integration"
7. Klicka "Add"
8. Hitta "Rapportera Temperatur" i listan och klicka "Download"
9. Starta om Home Assistant

## Konfiguration

1. Gå till **Inställningar** → **Enheter & tjänster**
2. Klicka på **+ LÄGG TILL INTEGRATION**
3. Sök efter "Rapportera Temperatur"
4. Följ instruktionerna:
   - Ange din hash-kod från Temperatur.nu
   - Välj temperatursensor från dropdown
   - Ange rapporteringsintervall (minuter)

## Funktioner

- ✅ GUI-baserad konfiguration
- ✅ Välj valfri temperatursensor från dropdown
- ✅ Konfigurerbar hash-kod
- ✅ Automatisk rapportering med konfigurerbart intervall
- ✅ Status och felhantering

## Support

Om du har problem eller förslag, skapa ett issue på [GitHub](https://github.com/frodr1k/RapporteraTempHA/issues).

## Licens

MIT License
