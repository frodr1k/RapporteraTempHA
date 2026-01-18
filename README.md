# Report Temperature to Temperatur.nu

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub release](https://img.shields.io/github/v/release/frodr1k/RapporteraTempHA)](https://github.com/frodr1k/RapporteraTempHA/releases)

A Home Assistant integration for automatically reporting temperature to Temperatur.nu with support for multiple sensors and intelligent aggregation.

_🇸🇪 [Swedish version below](#rapportera-temperatur-till-temperaturnu---svensk-version) / Svenska beskrivning nedan_

## Latest Release - v1.3.1 (2026-01-18)

**Bug Fix Release** - Fixed critical issue preventing sensor creation in some configurations. See [CHANGELOG.md](CHANGELOG.md) for details.

✅ No breaking changes - all existing configurations will continue to work.

## Create an Account at Temperatur.nu

Before you can use this integration, you need an account at Temperatur.nu:

1. Go to [www.temperatur.nu](http://www.temperatur.nu)
2. Click **"Create account"** or **"Register"**
3. Fill in the form with username, email, password, and location
4. Verify your account via email
5. Log in and find your **hash code** in account/reporting settings
6. Copy the hash code - you'll need it to configure the integration

## Installation via HACS

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the menu in top right corner (three dots)
4. Select "Custom repositories"
5. Add URL: `https://github.com/frodr1k/RapporteraTempHA`
6. Select category: "Integration"
7. Click "Add"
8. Find "Report Temperature" in the list and click "Download"
9. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **+ ADD INTEGRATION**
3. Search for "Report Temperature"
4. Follow the instructions:
   - Enter your hash code from Temperatur.nu
   - Select 1-3 temperature sensors
   - Choose aggregation method (minimum or mean)
   - Enter reporting interval (minutes)

## Features

- ✅ **Multiple sensor support** - Select up to 3 temperature sensors
- ✅ **Smart aggregation** - Choose minimum (recommended) or mean value
- ✅ **Shade temperature guarantee** - Using multiple sensors with minimum value ensures you're always reporting shade temperature, not sun-exposed readings
- ✅ **Temperature sensor** - The aggregated temperature is available as a separate sensor for use in automations
- ✅ **GUI-based configuration** - Easy setup through Home Assistant UI
- ✅ **Automatic reporting** - Configurable interval between 1-60 minutes
- ✅ **Status tracking** - Monitor last report status and individual sensor temperatures

### Why Multiple Sensors?

Using 2-3 sensors with minimum aggregation virtually guarantees that you're reporting the true shade temperature. Since different sensors may be exposed to sun at different times, the lowest reading will almost always be the one in shade. This is especially important for accurate weather reporting.

## Entities Created

The integration creates two sensors:

1. **Status Sensor** - Shows reporting status with attributes including:
   - Individual sensor temperatures
   - Aggregation method
   - Last reported temperature
   - Update status and messages

2. **Temperature Sensor** - The aggregated temperature value that can be used in:
   - Automations
   - Graphs and history
   - Other integrations
   - Mean temperature calculations over time

## Support

If you have problems or suggestions, create an issue on [GitHub](https://github.com/frodr1k/RapporteraTempHA/issues).

## License

MIT License

---

# Rapportera Temperatur till Temperatur.nu - Svensk version

En Home Assistant-integration för att automatiskt rapportera temperatur till Temperatur.nu med stöd för flera sensorer och intelligent aggregering.

## Skapa konto på Temperatur.nu

Innan du kan använda denna integration behöver du ett konto på Temperatur.nu:

1. Gå till [www.temperatur.nu](http://www.temperatur.nu)
2. Klicka på **"Skapa konto"** eller **"Registrera dig"**
3. Fyll i formuläret med användarnamn, e-post, lösenord och plats
4. Verifiera ditt konto via e-post
5. Logga in och hitta din **hash-kod** under kontoinställningar
6. Kopiera hash-koden - du behöver den för konfigurationen

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
   - Välj 1-3 temperatursensorer
   - Välj aggregeringsmetod (minimum eller medelvärde)
   - Ange rapporteringsintervall (minuter)

## Funktioner

- ✅ **Stöd för flera sensorer** - Välj upp till 3 temperatursensorer
- ✅ **Smart aggregering** - Välj minimum (rekommenderat) eller medelvärde
- ✅ **Skuggtemperatur-garanti** - Genom att använda flera sensorer med minimum-värde säkerställer du att du alltid rapporterar skuggtemperatur, inte solexponerad avläsning
- ✅ **Temperatursensor** - Den aggregerade temperaturen finns tillgänglig som en separat sensor för användning i automationer
- ✅ **GUI-baserad konfiguration** - Enkel setup genom Home Assistant UI
- ✅ **Automatisk rapportering** - Konfigurerbart intervall mellan 1-60 minuter
- ✅ **Statusövervakning** - Se senaste rapporteringsstatus och individuella sensortemperaturer

### Varför flera sensorer?

Att använda 2-3 sensorer med minimum-aggregering garanterar nästan alltid att du rapporterar den sanna skuggtemperaturen. Eftersom olika sensorer kan exponeras för sol vid olika tidpunkter kommer den lägsta avläsningen nästan alltid vara den som står i skugga. Detta är särskilt viktigt för korrekt väderrapportering.

## Skapade entiteter

Integrationen skapar två sensorer:

1. **Statussensor** - Visar rapporteringsstatus med attribut som inkluderar:
   - Individuella sensortemperaturer
   - Aggregeringsmetod
   - Senast rapporterade temperatur
   - Uppdateringsstatus och meddelanden

2. **Temperatursensor** - Det aggregerade temperaturvärdet som kan användas i:
   - Automationer
   - Grafer och historik
   - Andra integrationer
   - Medeltemperatur-beräkningar över tid

## Support

Om du har problem eller förslag, skapa ett issue på [GitHub](https://github.com/frodr1k/RapporteraTempHA/issues).

## Licens

MIT License
