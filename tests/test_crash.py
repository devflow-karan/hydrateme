# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import os
import sys
import pytest
from unittest.mock import MagicMock
from hydrateme.services import crash

def test_packaging_type(monkeypatch, tmp_path):
    """
    Verifies detection of current application confinement types.
    """
    monkeypatch.setenv("SNAP", "/snap/hydrateme")
    assert crash.get_packaging_type() == "snap"
    
    monkeypatch.delenv("SNAP")
    monkeypatch.setenv("FLATPAK_ID", "org.hydrateme.HydrateMe")
    assert crash.get_packaging_type() == "flatpak"
    
    monkeypatch.delenv("FLATPAK_ID")
    monkeypatch.setenv("APPIMAGE", "/path/to.AppImage")
    assert crash.get_packaging_type() == "AppImage"

def test_write_crash_report(monkeypatch, tmp_path):
    """
    Verifies formatting and file writes of system exceptions.
    """
    monkeypatch.setattr("hydrateme.utils.paths.get_crash_dir", lambda: str(tmp_path))
    monkeypatch.setattr("hydrateme.utils.paths.get_config_file", lambda: str(tmp_path / "config.json"))
    
    # Write empty config
    with open(tmp_path / "config.json", "w") as f:
        f.write("{}")
        
    try:
        raise ValueError("Simulated Exception")
    except ValueError as e:
        exctype, value, tb = sys.exc_info()
        report_file = crash.write_crash_report(exctype, value, tb)
        
    assert os.path.exists(report_file)
    with open(report_file, "r") as f:
        content = f.read()
    assert "Simulated Exception" in content
    assert "ValueError" in content

def test_setup_crash_reporter(monkeypatch):
    """
    Verifies that system exception hooks can be registered.
    """
    mock_hook = MagicMock()
    monkeypatch.setattr("sys.excepthook", mock_hook)
    crash.setup_crash_reporter()
    assert sys.excepthook is not mock_hook
