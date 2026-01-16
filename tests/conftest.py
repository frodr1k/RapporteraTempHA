"""Test configuration for RapporteraTempHA integration."""
import pytest
import sys
from pathlib import Path

# Add the custom_components directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def mock_hass():
    """Return a mock Home Assistant instance for tests that need it."""
    from unittest.mock import MagicMock
    
    mock = MagicMock()
    mock.config_entries = MagicMock()
    mock.data = {}
    return mock


@pytest.fixture
def mock_config_entry():
    """Return a mock config entry."""
    from unittest.mock import MagicMock
    
    entry = MagicMock()
    entry.entry_id = "test_entry_id"
    entry.data = {
        "hash_code": "test_hash_code",
        "sensor_entity_ids": ["sensor.test_temperature"],
        "aggregation_method": "min",
    }
    return entry
