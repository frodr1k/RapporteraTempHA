"""Test config flow for RapporteraTempHA - Bronze minimum coverage."""
import json
from pathlib import Path

# Get project root
project_root = Path(__file__).parent.parent

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
    assert 'documentation' in manifest
    assert 'issue_tracker' in manifest
    assert 'codeowners' in manifest
    
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


def test_required_files_exist():
    """Test that all required files exist."""
    required_files = [
        'custom_components/rapportera_temp/__init__.py',
        'custom_components/rapportera_temp/manifest.json',
        'custom_components/rapportera_temp/const.py',
        'custom_components/rapportera_temp/config_flow.py',
        'custom_components/rapportera_temp/sensor.py',
        'custom_components/rapportera_temp/strings.json',
        'custom_components/rapportera_temp/translations/sv.json',
        'hacs.json',
        'README.md',
        'LICENSE',
    ]
    
    for file_path in required_files:
        full_path = project_root / file_path
        assert full_path.exists(), f"Required file {file_path} does not exist"


def test_hacs_json_valid():
    """Test that hacs.json is valid."""
    hacs_path = project_root / 'hacs.json'
    assert hacs_path.exists(), "hacs.json does not exist"
    
    with open(hacs_path, 'r', encoding='utf-8') as f:
        hacs = json.load(f)
    
    assert 'name' in hacs
    assert hacs['name'] == 'Rapportera Temperatur'
    assert 'render_readme' in hacs


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
    for part in parts:
        int_part = int(part)
        assert int_part >= 0, f"Version part {part} should be non-negative"
