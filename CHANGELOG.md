# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.1] - 2026-01-18

### Fixed
- Fixed KeyError when creating sensors if `sensor_entity_id` is missing from configuration
- Added safe access for `hash_code` configuration parameter to prevent crashes
- Improved backward compatibility between old (single sensor) and new (multiple sensors) configurations
- Added proper error logging when hash_code is missing

### Changed
- Improved error handling in sensor initialization
- Enhanced robustness of configuration data access throughout the codebase

### Technical Details
This is a **bug fix release** with no breaking changes. The integration now properly handles:
- Migration from v1.2.x configurations (single sensor_entity_id)
- New v1.3.x configurations (multiple sensor_entity_ids)
- Missing or incomplete configuration data

**No action required from users** - the integration will automatically handle both old and new configurations.

## [1.3.0] - Previous Release

### Added
- Support for multiple temperature sensors (up to 3)
- Aggregation methods: minimum (recommended) and mean
- Separate temperature sensor entity
- Enhanced status tracking with individual sensor temperatures

### Changed
- Configuration moved from YAML to GUI-based config flow
- Updated to support sensor_entity_ids (list) instead of sensor_entity_id (single)

