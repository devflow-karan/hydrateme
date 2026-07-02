# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import os
import json
import logging
from hydrateme.utils import paths

logger = logging.getLogger("hydrateme")

CURRENT_CONFIG_VERSION = 3
DEFAULT_INTERVAL = 30
DEFAULT_SOUND = True

class MigrationManager:
    """
    Manages schemas updates for user configuration files.
    """
    @staticmethod
    def migrate(data: dict) -> dict:
        version = data.get("version", 1)
        if version == 1:
            logger.info("Upgrading configuration schema: version 1 -> 2")
            data["version"] = 2
            if "interval" not in data:
                data["interval"] = DEFAULT_INTERVAL
            if "sound" not in data:
                data["sound"] = DEFAULT_SOUND
            if "custom_sound_path" not in data:
                data["custom_sound_path"] = ""
            version = 2
        if version == 2:
            logger.info("Upgrading configuration schema: version 2 -> 3")
            data["version"] = 3
            if "autostart" not in data:
                data["autostart"] = True
            version = 3
        return data

class Config:
    """
    Handles loading, saving, and checking configuration values.
    """
    def __init__(self):
        self.interval = DEFAULT_INTERVAL
        self.sound = DEFAULT_SOUND
        self.custom_sound_path = ""
        self.autostart = True
        self.theme = "auto"
        self.version = CURRENT_CONFIG_VERSION
        self.load()

    def load(self):
        config_file = paths.get_config_file()
        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    data = json.load(f)
                
                # Apply migration
                if data.get("version", 1) < CURRENT_CONFIG_VERSION:
                    data = MigrationManager.migrate(data)
                    self.interval = data.get("interval", DEFAULT_INTERVAL)
                    self.sound = data.get("sound", DEFAULT_SOUND)
                    self.custom_sound_path = data.get("custom_sound_path", "")
                    self.autostart = data.get("autostart", True)
                    self.theme = data.get("theme", "auto")
                    self.version = data.get("version", CURRENT_CONFIG_VERSION)
                    self.save()
                else:
                    self.interval = data.get("interval", DEFAULT_INTERVAL)
                    self.sound = data.get("sound", DEFAULT_SOUND)
                    self.custom_sound_path = data.get("custom_sound_path", "")
                    self.autostart = data.get("autostart", True)
                    self.theme = data.get("theme", "auto")
                    self.version = data.get("version", CURRENT_CONFIG_VERSION)
                logger.info(f"Config loaded: version={self.version}, interval={self.interval}, sound={self.sound}, autostart={self.autostart}, theme={self.theme}")
            except Exception as e:
                logger.error(f"Failed to parse config file: {e}")
        else:
            logger.info("No config file found. Generating default settings.")
            self.save()

    def save(self):
        config_file = paths.get_config_file()
        config_dir = paths.get_config_dir()
        try:
            os.makedirs(config_dir, exist_ok=True)
            with open(config_file, "w") as f:
                json.dump({
                    "version": self.version,
                    "interval": self.interval,
                    "sound": self.sound,
                    "custom_sound_path": self.custom_sound_path,
                    "autostart": self.autostart,
                    "theme": self.theme
                }, f, indent=2)
            logger.info(f"Config successfully written to: {config_file}")
            
            # Setup autostart desktop file (handled via paths)
            try:
                paths.setup_autostart_desktop_file(self.autostart)
            except Exception as ex:
                logger.error(f"Failed to sync autostart file: {ex}")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
