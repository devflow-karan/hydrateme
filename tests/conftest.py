# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import os
import sys
import pytest
from unittest.mock import MagicMock

# Append source directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

@pytest.fixture(autouse=True)
def mock_dbus(monkeypatch):
    """
    Mocks dbus bindings to allow testing in headless environments.
    """
    mock_bus = MagicMock()
    mock_interface = MagicMock()
    
    # Mock screensaver behavior
    mock_screensaver = MagicMock()
    mock_screensaver.GetActive.return_value = False
    
    # Mock notification target
    mock_notify = MagicMock()
    
    def get_object(service, path):
        if service in ['org.gnome.ScreenSaver', 'org.freedesktop.ScreenSaver']:
            return mock_screensaver
        elif service == 'org.freedesktop.Notifications':
            return mock_notify
        return MagicMock()
        
    mock_bus.get_object = get_object
    
    monkeypatch.setattr("dbus.SessionBus", lambda: mock_bus)
    monkeypatch.setattr("dbus.Interface", lambda obj, name: mock_interface)
    
    return {
        "bus": mock_bus,
        "screensaver": mock_screensaver,
        "notify": mock_notify,
        "interface": mock_interface
    }

@pytest.fixture
def mock_subprocess(monkeypatch):
    """
    Mocks subprocess methods to intercept execution runs.
    """
    mock_run = MagicMock()
    mock_popen = MagicMock()
    
    mock_run.return_value.returncode = 0
    mock_popen.return_value.poll.return_value = None
    
    monkeypatch.setattr("subprocess.run", mock_run)
    monkeypatch.setattr("subprocess.Popen", mock_popen)
    
    return {
        "run": mock_run,
        "Popen": mock_popen
    }

@pytest.fixture
def clean_config_file(tmp_path, monkeypatch):
    """
    Directs config files to a temporary path.
    """
    temp_config_dir = tmp_path / "config"
    temp_config_file = temp_config_dir / "config.json"
    
    monkeypatch.setattr("hydrateme.utils.paths.get_config_dir", lambda: str(temp_config_dir))
    monkeypatch.setattr("hydrateme.utils.paths.get_config_file", lambda: str(temp_config_file))
    
    return temp_config_file

@pytest.fixture
def clean_state_dir(tmp_path, monkeypatch):
    """
    Directs logging and crash files to a temporary path.
    """
    temp_state_dir = tmp_path / "state"
    temp_log_file = temp_state_dir / "hydrateme.log"
    temp_crash_dir = temp_state_dir / "crash_reports"
    
    monkeypatch.setattr("hydrateme.utils.paths.get_state_dir", lambda: str(temp_state_dir))
    monkeypatch.setattr("hydrateme.utils.paths.get_log_file", lambda: str(temp_log_file))
    monkeypatch.setattr("hydrateme.utils.paths.get_crash_dir", lambda: str(temp_crash_dir))
    
    return {
        "dir": temp_state_dir,
        "log": temp_log_file,
        "crash": temp_crash_dir
    }

@pytest.fixture
def clean_lock_file(tmp_path, monkeypatch):
    """
    Directs lock files to a temporary path.
    """
    temp_lock_file = tmp_path / "hydrateme.lock"
    monkeypatch.setattr("hydrateme.utils.paths.get_lock_file", lambda: str(temp_lock_file))
    return temp_lock_file
