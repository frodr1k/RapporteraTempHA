# Report Temperature to Temperatur.nu

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

A Home Assistant integration for automatically reporting temperature to Temperatur.nu.

_🇸🇪 [Swedish version below](#rapportera-temperatur-till-temperaturnu---svensk-version) / Svenska beskrivning nedan_

## Create an Account at Temperatur.nu

Before you can use this integration, you need an account at Temperatur.nu:

1. Go to [www.temperatur.nu](http://www.temperatur.nu)
2. Click **"Create account"** or **"Register"**
3. Fill in the form with:
   - Username
   - Email address
   - Password
   - Location information (city, country)
4. Verify your account via the email you receive
5. Log in to your new account
6. Find your **hash code** in your account settings or reporting settings
   - The hash code is a unique code used to identify your station
   - It looks something like: `abc123def456...`
7. Copy the hash code - you'll need it to configure the integration

**Tip:** Save your hash code in a secure place, you'll need it every time you configure the integration.

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
   - Select temperature sensor from dropdown
   - Enter reporting interval (minutes)

## Features

- ✅ GUI-based configuration
- ✅ Select any temperature sensor from dropdown
- ✅ Configurable hash code
- ✅ Automatic reporting with configurable interval
- ✅ Status tracking and error handling

## Support

If you have problems or suggestions, create an issue on [GitHub](https://github.com/frodr1k/RapporteraTempHA/issues).

## License

MIT License

---

# Rapportera Temperatur till Temperatur.nu - Svensk version

En Home Assistant-integration för att automatiskt rapportera temperatur till Temperatur.nu.

## Skapa konto på Temperatur.nu

Innan du kan använda denna integration behöver du ett konto på Temperatur.nu:

1. Gå till [www.temperatur.nu](http://www.temperatur.nu)
2. Klicka på **"Skapa konto"** eller **"Registrera dig"**
3. Fyll i formuläret med:
   - Användarnamn
   - E-postadress
   - Lösenord
   - Platsinformation (stad, land)
4. Verifiera ditt konto via e-postmeddelandet du får
5. Logga in på ditt nya konto
6. Hitta din **hash-kod** under dina kontoinställningar eller rapporteringsinställningar
   - Hash-koden är en unik kod som används för att identifiera din station
   - Den ser ut ungefär som: `abc123def456...`
7. Kopiera hash-koden - du behöver den för att konfigurera integrationen

**Tips:** Spara din hash-kod på ett säkert ställe, du kommer behöva den varje gång du konfigurerar integrationen.

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
