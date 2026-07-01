# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import pytest
from unittest.mock import MagicMock
from PyQt6.QtWidgets import QSystemTrayIcon
from hydrateme.tray_manager import TrayManager

def test_tray_initialization_failure(clean_config_file, monkeypatch):
    """
    Verifies initialization fails gracefully if QSystemTrayIcon is not supported.
    """
    monkeypatch.setattr(QSystemTrayIcon, "isSystemTrayAvailable", lambda: False)
    
    mock_app = MagicMock()
    tray_manager = TrayManager(mock_app, None, None)
    
    assert tray_manager.initialize() is False

def test_tray_initialization_success(clean_config_file, monkeypatch, qapp):
    """
    Verifies tray setup, menu mappings, and icon generation.
    """
    monkeypatch.setattr(QSystemTrayIcon, "isSystemTrayAvailable", lambda: True)
    
    open_settings = MagicMock()
    quit_app = MagicMock()
    
    tray_manager = TrayManager(qapp, open_settings, quit_app)
    
    # Prevent GUI rendering errors by mocking QSystemTrayIcon methods
    monkeypatch.setattr(QSystemTrayIcon, "show", MagicMock())
    
    assert tray_manager.initialize() is True
    assert tray_manager.tray is not None
    assert not tray_manager.tray.icon().isNull()

def test_tray_load_fallback_icon(clean_config_file, monkeypatch):
    """
    Verifies that system fallbacks are triggered when asset files are missing.
    """
    mock_app = MagicMock()
    tray_manager = TrayManager(mock_app, None, None)
    
    # Force fallback icon generation by mocking os.path.exists
    monkeypatch.setattr("os.path.exists", lambda path: False)
    
    icon = tray_manager.load_icon()
    assert not icon.isNull()
