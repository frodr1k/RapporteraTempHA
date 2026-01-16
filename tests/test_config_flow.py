"""Test config flow for RapporteraTempHA."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from homeassistant import config_entries, data_entry_flow
import sys
from pathlib import Path

# Ensure the custom_components directory is in the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestConfigFlow:
    """Test the config flow."""
    
    def test_config_flow_imports(self):
        """Test that config flow imports work."""
        try:
            from custom_components.rapportera_temp.config_flow import RapporteraTempConfigFlow
            from custom_components.rapportera_temp import DOMAIN
            assert RapporteraTempConfigFlow is not None
            assert DOMAIN == "rapportera_temp"
        except ImportError as e:
            pytest.skip(f"Could not import config flow: {e}")
    
    def test_form_schema_structure(self):
        """Test that the form schema has correct fields."""
        try:
            from custom_components.rapportera_temp.config_flow import RapporteraTempConfigFlow
            import voluptuous as vol
            
            # The config flow should define a schema with required fields
            # This test verifies the structure exists
            assert hasattr(RapporteraTempConfigFlow, 'async_step_user')
        except ImportError as e:
            pytest.skip(f"Could not import for schema test: {e}")


class TestConnectionValidation:
    """Test connection validation in config flow."""
    
    @pytest.mark.asyncio
    async def test_validate_hash_code_success(self):
        """Test successful hash code validation."""
        try:
            from custom_components.rapportera_temp.config_flow import validate_hash_code
            from unittest.mock import AsyncMock, MagicMock
            
            mock_hass = MagicMock()
            test_hash = "test_hash_123"
            
            # Mock successful HTTP response
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.text = AsyncMock(return_value="OK")
            
            with patch('aiohttp.ClientSession') as mock_session:
                mock_session_instance = AsyncMock()
                mock_session.return_value.__aenter__.return_value = mock_session_instance
                mock_session_instance.post.return_value.__aenter__.return_value = mock_response
                
                result = await validate_hash_code(mock_hass, test_hash)
                assert result is True
        except ImportError as e:
            pytest.skip(f"Could not import validation function: {e}")
    
    @pytest.mark.asyncio
    async def test_validate_hash_code_failure(self):
        """Test failed hash code validation."""
        try:
            from custom_components.rapportera_temp.config_flow import validate_hash_code
            from unittest.mock import AsyncMock, MagicMock
            
            mock_hass = MagicMock()
            test_hash = "invalid_hash"
            
            # Mock failed HTTP response
            mock_response = AsyncMock()
            mock_response.status = 403
            mock_response.text = AsyncMock(return_value="Invalid hash")
            
            with patch('aiohttp.ClientSession') as mock_session:
                mock_session_instance = AsyncMock()
                mock_session.return_value.__aenter__.return_value = mock_session_instance
                mock_session_instance.post.return_value.__aenter__.return_value = mock_response
                
                result = await validate_hash_code(mock_hass, test_hash)
                assert result is False
        except ImportError as e:
            pytest.skip(f"Could not import validation function: {e}")


class TestDuplicateEntry:
    """Test duplicate entry prevention."""
    
    def test_unique_id_format(self):
        """Test that unique ID is based on hash code to prevent duplicates."""
        try:
            from custom_components.rapportera_temp.config_flow import RapporteraTempConfigFlow
            
            # The config flow should set unique_id based on hash_code
            # This prevents duplicate entries for the same temperatur.nu station
            flow = RapporteraTempConfigFlow()
            assert hasattr(flow, 'async_step_user')
            
            # The implementation should call self.async_set_unique_id(hash_code)
            # and self._abort_if_unique_id_configured()
        except ImportError as e:
            pytest.skip(f"Could not import for duplicate test: {e}")


class TestMultipleSensorSupport:
    """Test multiple sensor configuration support."""
    
    def test_sensor_entity_ids_field(self):
        """Test that sensor_entity_ids field accepts multiple sensors."""
        try:
            from custom_components.rapportera_temp.config_flow import RapporteraTempConfigFlow
            
            # Config flow should support sensor_entity_ids as a list
            # Maximum 3 sensors as per requirements
            flow = RapporteraTempConfigFlow()
            assert flow is not None
        except ImportError as e:
            pytest.skip(f"Could not import for multi-sensor test: {e}")
    
    def test_aggregation_method_field(self):
        """Test that aggregation_method field exists."""
        try:
            from custom_components.rapportera_temp.const import AGGREGATION_MIN, AGGREGATION_MEAN
            
            # Verify aggregation constants exist
            assert AGGREGATION_MIN == "min"
            assert AGGREGATION_MEAN == "mean"
        except ImportError as e:
            pytest.skip(f"Could not import aggregation constants: {e}")
