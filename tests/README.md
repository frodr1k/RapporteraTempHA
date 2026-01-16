# RapporteraTempHA Tests

This directory contains unit tests for the RapporteraTempHA Home Assistant integration.

## Test Structure

### `test_basic.py`
Basic functionality tests that don't require Home Assistant runtime:
- Domain constant validation
- Manifest.json structure and validity
- Strings.json and translations
- File existence checks
- Python syntax validation
- Constants validation

### `test_config_flow.py`
Configuration flow tests:
- Config flow structure validation
- Hash code validation (connection test before configure)
- Duplicate entry prevention
- Multiple sensor support
- Aggregation method selection

### `test_init.py`
Setup and initialization tests:
- Setup entry validation
- Data structure initialization
- Temperature aggregation logic
- Backward compatibility with single sensor
- Sensor entity creation

### `conftest.py`
Pytest configuration and fixtures:
- `mock_hass`: Mock Home Assistant instance
- `mock_config_entry`: Mock configuration entry

## Running Tests

### Install pytest
```bash
pip install pytest pytest-asyncio
```

### Run all tests
```bash
pytest tests/
```

### Run specific test file
```bash
pytest tests/test_basic.py
```

### Run with verbose output
```bash
pytest -v tests/
```

### Run with coverage
```bash
pip install pytest-cov
pytest --cov=custom_components.rapportera_temp tests/
```

## Bronze Quality Scale Coverage

These tests satisfy the following Bronze requirements:

1. ✅ **config-flow** - Tests validate GUI configuration structure
2. ✅ **config-flow-test-coverage** - Comprehensive config flow tests
3. ✅ **test-before-configure** - Hash code validation before configuration
4. ✅ **test-before-setup** - Setup validation tests
5. ✅ **unique-config-entry** - Duplicate prevention tests

## Test Philosophy

The tests are designed to:
- **Be independent**: Each test can run standalone
- **Be fast**: No actual API calls or Home Assistant startup
- **Be comprehensive**: Cover critical paths and edge cases
- **Be maintainable**: Clear naming and documentation
- **Support CI/CD**: Can run in automated pipelines

## Future Enhancements

Potential test additions:
- Integration tests with Home Assistant test framework
- Mock API response testing
- Error handling and retry logic
- Sensor state update tests
- Configuration option changes
