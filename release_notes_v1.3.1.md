# Release Notes - v1.3.1

**Release Date:** 2026-01-18

## 🐛 Bug Fix Release

This release fixes a critical issue that could prevent sensor creation in certain configurations.

## Fixed Issues

### KeyError in Sensor Initialization
- **Fixed:** KeyError when creating sensors if `sensor_entity_id` is missing from configuration
- **Fixed:** Safe access for `hash_code` configuration parameter to prevent crashes
- **Fixed:** Improved backward compatibility between old (single sensor) and new (multiple sensors) configurations
- **Fixed:** Added proper error logging when hash_code is missing

## Improvements

- Enhanced error handling in sensor initialization
- Improved robustness of configuration data access throughout the codebase
- Better migration support from v1.2.x to v1.3.x configurations

## Compatibility

✅ **No Breaking Changes** - All existing configurations will continue to work.

The integration now properly handles:
- Migration from v1.2.x configurations (single `sensor_entity_id`)
- New v1.3.x configurations (multiple `sensor_entity_ids`)
- Missing or incomplete configuration data

## Upgrade Instructions

**No action required from users.** Simply update the integration through HACS or manually, and restart Home Assistant. The integration will automatically handle both old and new configurations.

### Via HACS (Recommended)
1. Open HACS → Integrations
2. Find "Report Temperature to Temperatur.nu"
3. Click "Update"
4. Restart Home Assistant

### Manual Installation
1. Download the latest release from [GitHub](https://github.com/frodr1k/RapporteraTempHA/releases/tag/v1.3.1)
2. Extract to `custom_components/rapportera_temp/`
3. Restart Home Assistant

## Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete details.

## Support

If you encounter any issues, please report them on [GitHub Issues](https://github.com/frodr1k/RapporteraTempHA/issues).
