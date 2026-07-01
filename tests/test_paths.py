# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import os
from hydrateme.utils import paths

def test_path_resolutions(monkeypatch, tmp_path):
    """
    Verifies XDG paths and custom asset location mappings.
    """
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_RUNTIME_DIR", str(tmp_path / "runtime"))
    os.makedirs(str(tmp_path / "runtime"), exist_ok=True)
    
    assert paths.get_config_dir().endswith("config/hydrateme")
    assert paths.get_config_file().endswith("config/hydrateme/config.json")
    assert paths.get_state_dir().endswith("state/hydrateme")
    assert paths.get_log_file().endswith("state/hydrateme/hydrateme.log")
    assert paths.get_crash_dir().endswith("state/hydrateme/crash_reports")
    
    # Lock file inside XDG_RUNTIME_DIR
    assert paths.get_lock_file().endswith("runtime/hydrateme.lock")
    
    # Asset path under snap
    monkeypatch.setenv("SNAP", "/snap/hydrateme/current")
    assert paths.get_asset_path("/usr/share/sound.wav") == "/snap/hydrateme/current/usr/share/sound.wav"
    
    # Asset path fallback when SNAP is not present
    monkeypatch.delenv("SNAP", raising=False)
    assert paths.get_asset_path("/usr/share/sound.wav") == "/usr/share/sound.wav"

def test_setup_autostart_missing_source(tmp_path, monkeypatch):
    """
    Verifies that autostart file creation exits cleanly when source desktop is missing.
    """
    mock_autostart_dir = tmp_path / "autostart"
    monkeypatch.setattr("os.path.expanduser", lambda p: str(mock_autostart_dir) if p.startswith("~") else p)
    
    # Intercept os.path.exists to return False for source desktop path checks
    real_exists = os.path.exists
    def mock_exists(path):
        if "autostart" not in str(path) and str(path).endswith(".desktop"):
            return False
        return real_exists(path)
    monkeypatch.setattr(os.path, "exists", mock_exists)
    
    monkeypatch.setattr(paths, "get_asset_path", lambda p: "/non/existent/desktop.desktop")
    
    paths.setup_autostart_desktop_file(True)
    assert not (mock_autostart_dir / "hydrateme.desktop").exists()
