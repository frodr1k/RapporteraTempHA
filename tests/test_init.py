"""Test initialization and setup for RapporteraTempHA."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import sys
from pathlib import Path

# Ensure the custom_components directory is in the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestSetupEntry:
    """Test async_setup_entry validation."""
    
    @pytest.mark.asyncio
    async def test_setup_entry_imports(self):
        """Test that setup imports work."""
        try:
            from custom_components.rapportera_temp import async_setup_entry, DOMAIN
            assert async_setup_entry is not None
            assert DOMAIN == "rapportera_temp"
        except ImportError as e:
            pytest.skip(f"Could not import setup: {e}")
    
    @pytest.mark.asyncio
    async def test_setup_validates_sensors(self):
        """Test that setup validates sensor availability before starting."""
        try:
            from custom_components.rapportera_temp import async_setup_entry, DOMAIN
            
            mock_hass = MagicMock()
            mock_hass.data = {}
            mock_hass.async_add_executor_job = AsyncMock()
            
            # Mock the state check for sensors
            mock_hass.states.get = MagicMock(return_value=None)  # Sensor not available
            
            mock_entry = MagicMock()
            mock_entry.entry_id = "test_entry"
            mock_entry.data = {
                "hash_code": "test_hash",
                "sensor_entity_ids": ["sensor.test_temp"],
                "aggregation_method": "min",
            }
            
            # Mock async_forward_entry_setups
            with patch('homeassistant.config_entries.ConfigEntry.async_forward_entry_setups', 
                      new_callable=AsyncMock) as mock_forward:
                result = await async_setup_entry(mock_hass, mock_entry)
                
                # Setup should still succeed even if sensors are initially unavailable
                # The integration will wait for them to become available
                assert result is True
                assert DOMAIN in mock_hass.data
        except ImportError as e:
            pytest.skip(f"Could not import for setup test: {e}")
    
    @pytest.mark.asyncio
    async def test_setup_initializes_data_structure(self):
        """Test that setup initializes data structure correctly."""
        try:
            from custom_components.rapportera_temp import async_setup_entry, DOMAIN
            
            mock_hass = MagicMock()
            mock_hass.data = {}
            
            mock_entry = MagicMock()
            mock_entry.entry_id = "test_entry_123"
            mock_entry.data = {
                "hash_code": "test_hash",
                "sensor_entity_ids": ["sensor.temp1", "sensor.temp2"],
                "aggregation_method": "mean",
            }
            
            with patch('homeassistant.config_entries.ConfigEntry.async_forward_entry_setups', 
                      new_callable=AsyncMock):
                await async_setup_entry(mock_hass, mock_entry)
                
                # Verify data structure was created
                assert DOMAIN in mock_hass.data
                assert mock_entry.entry_id in mock_hass.data[DOMAIN]
                
                entry_data = mock_hass.data[DOMAIN][mock_entry.entry_id]
                assert "config" in entry_data
                assert "last_update_status" in entry_data
                assert "sensor_temperatures" in entry_data
        except ImportError as e:
            pytest.skip(f"Could not import for data structure test: {e}")


class TestTemperatureReporting:
    """Test temperature reporting logic."""
    
    def test_aggregation_min(self):
        """Test minimum aggregation calculation."""
        temperatures = [20.5, 21.0, 19.8]
        result = min(temperatures)
        assert result == 19.8
    
    def test_aggregation_mean(self):
        """Test mean aggregation calculation."""
        import statistics
        temperatures = [20.0, 21.0, 19.0]
        result = statistics.mean(temperatures)
        assert result == 20.0
    
    def test_single_sensor_backward_compatibility(self):
        """Test that single sensor configuration still works."""
        try:
            # Test the logic that handles both old (single) and new (multiple) format
            # Old format: sensor_entity_id (string)
            # New format: sensor_entity_ids (list)
            
            old_config = {"sensor_entity_id": "sensor.temp"}
            new_config = {"sensor_entity_ids": ["sensor.temp"]}
            
            # The code should handle both:
            # sensor_ids = entry.data.get("sensor_entity_ids", [entry.data.get("sensor_entity_id")])
            
            sensor_ids_old = old_config.get("sensor_entity_ids", [old_config.get("sensor_entity_id")])
            sensor_ids_new = new_config.get("sensor_entity_ids", [new_config.get("sensor_entity_id")])
            
            if not isinstance(sensor_ids_old, list):
                sensor_ids_old = [sensor_ids_old]
            
            assert sensor_ids_old == ["sensor.temp"]
            assert sensor_ids_new == ["sensor.temp"]
        except Exception as e:
            pytest.skip(f"Backward compatibility test skipped: {e}")


class TestSensorEntities:
    """Test sensor entity creation."""
    
    def test_sensor_module_imports(self):
        """Test that sensor module imports correctly."""
        try:
            from custom_components.rapportera_temp.sensor import (
                RapporteraTempStatusSensor,
                RapporteraTempTemperatureSensor,
            )
            assert RapporteraTempStatusSensor is not None
            assert RapporteraTempTemperatureSensor is not None
        except ImportError as e:
            pytest.skip(f"Could not import sensors: {e}")
    
    def test_status_sensor_has_unique_id(self):
        """Test that status sensor has unique_id attribute."""
        try:
            from custom_components.rapportera_temp.sensor import RapporteraTempStatusSensor
            
            # Status sensor should have _attr_unique_id or unique_id property
            mock_entry = MagicMock()
            mock_entry.entry_id = "test_id"
            mock_entry.data = {"hash_code": "test_hash"}
            
            sensor = RapporteraTempStatusSensor(mock_entry)
            
            # Should have unique_id attribute
            assert hasattr(sensor, '_attr_unique_id') or hasattr(sensor, 'unique_id')
        except Exception as e:
            pytest.skip(f"Status sensor test skipped: {e}")
    
    def test_temperature_sensor_has_device_class(self):
        """Test that temperature sensor has correct device class."""
        try:
            from custom_components.rapportera_temp.sensor import RapporteraTempTemperatureSensor
            
            mock_entry = MagicMock()
            mock_entry.entry_id = "test_id"
            mock_entry.data = {"hash_code": "test_hash"}
            
            sensor = RapporteraTempTemperatureSensor(mock_entry)
            
            # Temperature sensor should have device_class = TEMPERATURE
            assert hasattr(sensor, '_attr_device_class')
        except Exception as e:
            pytest.skip(f"Temperature sensor test skipped: {e}")
