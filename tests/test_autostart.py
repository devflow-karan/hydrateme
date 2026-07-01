# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import os
import pytest
from unittest.mock import MagicMock
from hydrateme.utils import paths
from hydrateme.__main__ import main

def test_setup_autostart_desktop_file(tmp_path, monkeypatch):
    """
    Verifies that the autostart desktop entry is successfully created and deleted.
    """
    mock_autostart_dir = tmp_path / ".config" / "autostart"
    mock_autostart_file = mock_autostart_dir / "hydrateme.desktop"
    
    # Mock expanduser to redirect to tmp_path
    def mock_expanduser(path):
        if path.startswith("~/.config/autostart"):
            return str(mock_autostart_dir)
        return path
    monkeypatch.setattr("os.path.expanduser", mock_expanduser)
    
    # Create fake source desktop file
    mock_src_desktop = tmp_path / "hydrateme.desktop"
    mock_src_desktop.write_text("[Desktop Entry]\nExec=hydrateme\nName=HydrateMe")
    monkeypatch.setattr(paths, "get_asset_path", lambda path: str(mock_src_desktop))
    
    # Test creation/enable
    paths.setup_autostart_desktop_file(True)
    assert mock_autostart_file.exists()
    
    # Verify Exec line contains --autostart flag
    content = mock_autostart_file.read_text()
    assert "Exec=hydrateme --autostart" in content
    
    # Test deletion/disable
    paths.setup_autostart_desktop_file(False)
    assert not mock_autostart_file.exists()

def test_early_exit_on_autostart_disabled(monkeypatch):
    """
    Verifies that startup exits early when autostart is disabled in configuration.
    """
    mock_args = MagicMock(debug=False, verify=False, autostart=True)
    monkeypatch.setattr("hydrateme.__main__.parse_args", lambda: mock_args)
    
    mock_config = MagicMock()
    mock_config.autostart = False
    monkeypatch.setattr("hydrateme.settings_manager.Config", lambda: mock_config)
    
    monkeypatch.setattr("hydrateme.__main__.setup_logging", MagicMock())
    monkeypatch.setattr("hydrateme.__main__.setup_crash_reporter", MagicMock())
    monkeypatch.setattr("hydrateme.__main__.run_diagnostics", MagicMock())
    
    with pytest.raises(SystemExit) as excinfo:
        main()
    assert excinfo.value.code == 0
