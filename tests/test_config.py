# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import os
import json
from hydrateme.settings_manager import Config
from hydrateme.utils.paths import get_config_file, validate_audio_file

def test_config_defaults(clean_config_file):
    """
    Verifies default settings are loaded when no config exists.
    """
    config = Config()
    assert config.interval == 30
    assert config.sound is True
    assert config.custom_sound_path == ""
    assert config.autostart is True
    assert config.version == 3
    assert os.path.exists(get_config_file())

def test_config_save_load(clean_config_file):
    """
    Verifies config values can be customized and persists on disk.
    """
    config = Config()
    config.interval = 45
    config.sound = False
    config.custom_sound_path = "/tmp/fake.wav"
    config.autostart = False
    config.save()
    
    # Load settings from a new class instance
    new_config = Config()
    assert new_config.interval == 45
    assert new_config.sound is False
    assert new_config.custom_sound_path == "/tmp/fake.wav"
    assert new_config.autostart is False
    assert new_config.version == 3

def test_config_migration(clean_config_file):
    """
    Verifies configuration updates schema to current version.
    """
    # Write version 1 config file manually
    old_data = {
        "interval": 20,
        "sound": False
    }
    os.makedirs(os.path.dirname(get_config_file()), exist_ok=True)
    with open(get_config_file(), "w") as f:
        json.dump(old_data, f)
        
    config = Config()
    assert config.interval == 20
    assert config.sound is False
    assert config.custom_sound_path == ""
    assert config.autostart is True
    assert config.version == 3
    
    with open(get_config_file(), "r") as f:
        saved_data = json.load(f)
    assert saved_data["version"] == 3
    assert saved_data["custom_sound_path"] == ""
    assert saved_data["autostart"] is True

def test_config_migration_v2_to_v3(clean_config_file):
    """
    Verifies migration from schema version 2 to 3.
    """
    v2_data = {
        "version": 2,
        "interval": 45,
        "sound": False,
        "custom_sound_path": "/tmp/custom.wav"
    }
    os.makedirs(os.path.dirname(get_config_file()), exist_ok=True)
    with open(get_config_file(), "w") as f:
        json.dump(v2_data, f)
        
    config = Config()
    assert config.interval == 45
    assert config.sound is False
    assert config.custom_sound_path == "/tmp/custom.wav"
    assert config.autostart is True
    assert config.version == 3
    
    with open(get_config_file(), "r") as f:
        saved_data = json.load(f)
    assert saved_data["version"] == 3
    assert saved_data["autostart"] is True

def test_validate_audio_file(tmp_path):
    """
    Verifies audio path validation checks file attributes.
    """
    assert validate_audio_file("") is False
    assert validate_audio_file("/non/existent/path/sound.wav") is False
    
    # Safe wav file
    valid_file = tmp_path / "test.wav"
    valid_file.write_text("dummy")
    assert validate_audio_file(str(valid_file)) is True
    
    # Unsafe extension
    invalid_ext = tmp_path / "test.txt"
    invalid_ext.write_text("dummy")
    assert validate_audio_file(str(invalid_ext)) is False
