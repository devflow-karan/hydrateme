# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import os
import shutil
import pytest
from unittest.mock import MagicMock
from hydrateme.settings_manager import Config
from hydrateme.services.sound import SoundManager

def test_sound_disabled(clean_config_file, mock_subprocess):
    """
    Verifies that no subprocesses are started if sound is muted in configs.
    """
    config = Config()
    config.sound = False
    manager = SoundManager(config)
    
    manager.play_reminder_sound()
    mock_subprocess["Popen"].assert_not_called()

def test_sound_play_priority(clean_config_file, mock_subprocess, monkeypatch):
    """
    Verifies priority routing cascades: Pulse (paplay) -> PipeWire (pw-play) -> ALSA (aplay).
    """
    config = Config()
    config.sound = True
    manager = SoundManager(config)
    
    # Mock file existence checks
    monkeypatch.setattr("os.path.exists", lambda path: True)

    # 1. Test paplay selection
    monkeypatch.setattr(shutil, "which", lambda cmd: cmd == "paplay")
    manager.play_reminder_sound()
    mock_subprocess["Popen"].assert_called_once()
    args = mock_subprocess["Popen"].call_args[0][0]
    assert args[0] == "paplay"
    
    # 2. Test pw-play fallback
    mock_subprocess["Popen"].reset_mock()
    monkeypatch.setattr(shutil, "which", lambda cmd: cmd == "pw-play")
    manager.play_reminder_sound()
    mock_subprocess["Popen"].assert_called_once()
    args = mock_subprocess["Popen"].call_args[0][0]
    assert args[0] == "pw-play"
    
    # 3. Test aplay fallback
    mock_subprocess["Popen"].reset_mock()
    monkeypatch.setattr(shutil, "which", lambda cmd: cmd == "aplay")
    manager.play_reminder_sound()
    mock_subprocess["Popen"].assert_called_once()
    args = mock_subprocess["Popen"].call_args[0][0]
    assert args[0] == "aplay"

def test_sound_stop(clean_config_file, mock_subprocess, monkeypatch):
    """
    Verifies that calling stop halts any active player subprocesses.
    """
    config = Config()
    config.sound = True
    manager = SoundManager(config)
    
    mock_process = MagicMock()
    mock_process.poll.return_value = None  # Running state
    manager.process = mock_process
    
    manager.stop_sound()
    mock_process.terminate.assert_called_once()
    assert manager.process is None
