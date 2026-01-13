# Release v1.0.1 - Critical Fix

## 🐛 Critical Bug Fix

### Fixed Integration Not Appearing in Home Assistant
- **Fixed `strings.json` language** - Changed from Swedish to English (required by Home Assistant)
  - Home Assistant requires `strings.json` to be in English as the base language
  - Swedish translations remain available in `translations/sv.json`
  - This fix allows the integration to be properly discovered and added in Home Assistant

### What was the problem?
If you downloaded the integration via HACS but couldn't add it under **Settings → Devices & Services**, this was because `strings.json` was in Swedish instead of English. Home Assistant couldn't register the integration properly.

## ✅ What's included

All functionality from v1.0.0b plus the critical fix:

- ✅ Automatic temperature reporting to Temperatur.nu
- ✅ GUI-based configuration
- ✅ Entity selector for sensor selection
- ✅ Configurable reporting interval
- ✅ Full status tracking with attributes
- ✅ Dynamic status icons
- ✅ Error handling and logging
- ✅ Bilingual documentation (English/Swedish)
- ✅ **NOW WORKS**: Integration appears in Home Assistant after HACS installation

## 📋 Requirements

- Home Assistant 2023.1.0 or newer
- Temperature sensor in Home Assistant
- Internet connection to Temperatur.nu
- Hash code from Temperatur.nu

## 🚀 Installation & Update

### New Installation via HACS

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the menu in top right corner (three dots)
4. Select "Custom repositories"
5. Add URL: `https://github.com/frodr1k/RapporteraTempHA`
6. Select category: "Integration"
7. Click "Add"
8. Find "Report Temperature" and click "Download"
9. **Restart Home Assistant**
10. Go to Settings → Devices & Services → Add Integration
11. Search for "Report Temperature"

### Updating from v1.0.0 or v1.0.0b

1. Open HACS → Integrations
2. Find "Rapportera Temperatur" / "Report Temperature"
3. Click the three dots → "Redownload" or update to v1.0.1
4. **Restart Home Assistant**
5. Now you can add the integration under Settings → Devices & Services

## 📖 Documentation

Full bilingual documentation (English/Swedish) available in the [README](README.md).

Includes detailed instructions for:
- Creating an account at Temperatur.nu
- Finding your hash code
- Installation and configuration
- Troubleshooting

## 🙏 Credits

Developed for reporting temperature data to [Temperatur.nu](http://www.temperatur.nu)

## 📝 License

MIT License - See LICENSE file for details
