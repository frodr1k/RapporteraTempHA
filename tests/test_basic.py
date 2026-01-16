"""Basic unit tests for RapporteraTempHA integration."""
import pytest
import os
import sys
from pathlib import Path

# Ensure the custom_components directory is in the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestBasicFunctionality:
    """Test basic functionality without Home Assistant dependencies."""
    
    def test_domain_constant(self):
        """Test that DOMAIN constant is defined."""
        try:
            from custom_components.rapportera_temp import DOMAIN
            assert DOMAIN == "rapportera_temp"
        except ImportError as e:
            pytest.skip(f"Could not import module: {e}")
    
    def test_manifest_exists(self):
        """Test that manifest.json exists and is valid."""
        import json
        manifest_path = project_root / 'custom_components' / 'rapportera_temp' / 'manifest.json'
        
        assert manifest_path.exists(), "manifest.json does not exist"
        
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        assert manifest['domain'] == 'rapportera_temp'
        assert manifest['name'] == 'Rapportera Temperatur'
        # Check version format is valid (e.g., "1.3.0")
        assert 'version' in manifest
        version_parts = manifest['version'].split('.')
        assert len(version_parts) >= 2, "Version should be in format X.Y or X.Y.Z"
        assert 'requirements' in manifest
    
    def test_strings_file_exists(self):
        """Test that strings.json exists and is valid."""
        import json
        strings_path = project_root / 'custom_components' / 'rapportera_temp' / 'strings.json'
        
        assert strings_path.exists(), "strings.json does not exist"
        
        with open(strings_path, 'r', encoding='utf-8') as f:
            strings = json.load(f)
        
        assert 'config' in strings
        assert 'step' in strings['config']
        # Verify user step has correct field names
        assert 'user' in strings['config']['step']
        assert 'data' in strings['config']['step']['user']
        assert 'hash_code' in strings['config']['step']['user']['data']
        assert 'sensor_entity_ids' in strings['config']['step']['user']['data']
        assert 'aggregation_method' in strings['config']['step']['user']['data']
    
    def test_translations_exist(self):
        """Test that Swedish translations exist."""
        import json
        translations_path = project_root / 'custom_components' / 'rapportera_temp' / 'translations' / 'sv.json'
        
        assert translations_path.exists(), "sv.json does not exist"
        
        with open(translations_path, 'r', encoding='utf-8') as f:
            translations = json.load(f)
        
        assert 'config' in translations


class TestCodeQuality:
    """Test code quality and structure."""
    
    def test_all_required_files_exist(self):
        """Test that all required files exist."""
        required_files = [
            'custom_components/rapportera_temp/__init__.py',
            'custom_components/rapportera_temp/manifest.json',
            'custom_components/rapportera_temp/const.py',
            'custom_components/rapportera_temp/config_flow.py',
            'custom_components/rapportera_temp/sensor.py',
            'custom_components/rapportera_temp/strings.json',
            'custom_components/rapportera_temp/translations/sv.json',
        ]
        
        for file_path in required_files:
            full_path = project_root / file_path
            assert full_path.exists(), f"Required file {file_path} does not exist"
    
    def test_no_syntax_errors(self):
        """Test that Python files have no syntax errors."""
        import py_compile
        import glob
        
        pattern = str(project_root / 'custom_components' / 'rapportera_temp' / '**' / '*.py')
        python_files = glob.glob(pattern, recursive=True)
        
        assert len(python_files) > 0, "No Python files found"
        
        for file_path in python_files:
            try:
                py_compile.compile(file_path, doraise=True)
            except py_compile.PyCompileError as e:
                pytest.fail(f"Syntax error in {file_path}: {e}")
    
    def test_const_file_structure(self):
        """Test that const.py has required constants."""
        try:
            from custom_components.rapportera_temp.const import (
                AGGREGATION_MIN,
                AGGREGATION_MEAN,
            )
            assert AGGREGATION_MIN == "min"
            assert AGGREGATION_MEAN == "mean"
        except ImportError as e:
            pytest.skip(f"Could not import constants: {e}")


class TestConfigFlowStructure:
    """Test config flow structure and validation."""
    
    def test_config_flow_class_exists(self):
        """Test that ConfigFlow class exists."""
        try:
            from custom_components.rapportera_temp.config_flow import RapporteraTempConfigFlow
            assert RapporteraTempConfigFlow is not None
        except ImportError as e:
            pytest.skip(f"Could not import ConfigFlow: {e}")
    
    def test_config_flow_has_required_methods(self):
        """Test that ConfigFlow has required methods."""
        try:
            from custom_components.rapportera_temp.config_flow import RapporteraTempConfigFlow
            
            # Check for required async methods
            assert hasattr(RapporteraTempConfigFlow, 'async_step_user')
            assert callable(getattr(RapporteraTempConfigFlow, 'async_step_user'))
        except ImportError as e:
            pytest.skip(f"Could not import ConfigFlow: {e}")
