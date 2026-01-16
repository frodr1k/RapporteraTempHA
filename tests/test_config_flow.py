"""Test config flow for RapporteraTempHA - Bronze minimum coverage."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import sys
from pathlib import Path
import json

# Ensure the custom_components directory is in the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

DOMAIN = "rapportera_temp"


def test_manifest_valid():
    """Test that manifest.json is valid and has required fields."""
    manifest_path = project_root / 'custom_components' / 'rapportera_temp' / 'manifest.json'
    assert manifest_path.exists(), "manifest.json does not exist"
    
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    
    assert manifest['domain'] == DOMAIN
    assert manifest['name'] == 'Rapportera Temperatur'
    assert 'version' in manifest
    
    # Verify version format (X.Y.Z)
    version_parts = manifest['version'].split('.')
    assert len(version_parts) >= 2, "Version should be in format X.Y or X.Y.Z"
    for part in version_parts:
        assert part.isdigit(), f"Version part '{part}' should be numeric"


def test_strings_json_valid():
    """Test that strings.json is valid and has config flow structure."""
    strings_path = project_root / 'custom_components' / 'rapportera_temp' / 'strings.json'
    assert strings_path.exists(), "strings.json does not exist"
    
    with open(strings_path, 'r', encoding='utf-8') as f:
        strings = json.load(f)
    
    # Verify config flow structure
    assert 'config' in strings
    assert 'step' in strings['config']
    assert 'user' in strings['config']['step']
    assert 'data' in strings['config']['step']['user']
    
    # Verify required fields exist in strings
    user_data = strings['config']['step']['user']['data']
    assert 'hash_code' in user_data
    assert 'sensor_entity_ids' in user_data
    assert 'aggregation_method' in user_data


def test_translations_exist():
    """Test that Swedish translations exist."""
    translations_path = project_root / 'custom_components' / 'rapportera_temp' / 'translations' / 'sv.json'
    assert translations_path.exists(), "sv.json does not exist"
    
    with open(translations_path, 'r', encoding='utf-8') as f:
        translations = json.load(f)
    
    assert 'config' in translations


def test_config_flow_class_exists():
    """Test that ConfigFlow class exists and has required methods."""
    from custom_components.rapportera_temp.config_flow import RapporteraTempConfigFlow
    from custom_components.rapportera_temp import DOMAIN as imported_domain
    
    assert imported_domain == DOMAIN
    assert RapporteraTempConfigFlow is not None
    assert hasattr(RapporteraTempConfigFlow, 'async_step_user')
    assert callable(getattr(RapporteraTempConfigFlow, 'async_step_user'))


def test_version_format_consistent():
    """Test that version in manifest matches expected format for releases."""
    manifest_path = project_root / 'custom_components' / 'rapportera_temp' / 'manifest.json'
    
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    
    version = manifest['version']
    parts = version.split('.')
    
    # Should have at least major.minor, optionally major.minor.patch
    assert len(parts) in [2, 3], f"Version {version} should have 2 or 3 parts"
    
    # All parts should be integers
    for i, part in enumerate(parts):
        try:
            int_part = int(part)
            assert int_part >= 0, f"Version part {part} should be non-negative"
        except ValueError:
            pytest.fail(f"Version part '{part}' is not a valid integer")

