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

def test_tray_load_icon_null_pixmap_fallback(clean_config_file, monkeypatch, qapp):
    """
    Verifies that load_icon skips icons that exist but have null pixmaps (e.g. missing SVG reader).
    """
    tray_manager = TrayManager(qapp, None, None)
    
    # Mock os.path.exists to return True for the SVG path
    monkeypatch.setattr("os.path.exists", lambda path: True)
    
    # Mock QIcon to return an icon whose isNull() is False, but pixmap(24, 24).isNull() is True
    mock_icon = MagicMock()
    mock_icon.isNull.return_value = False
    mock_pixmap = MagicMock()
    mock_pixmap.isNull.return_value = True
    mock_icon.pixmap.return_value = mock_pixmap
    
    mock_qicon_class = MagicMock()
    mock_qicon_class.fromTheme.return_value = MagicMock(isNull=lambda: True)
    mock_qicon_class.side_effect = lambda *args: mock_icon if args else MagicMock()
    
    monkeypatch.setattr("hydrateme.tray_manager.QIcon", mock_qicon_class)
    
    # Verify that load_icon falls back to dynamic icon (since SVG has null pixmap)
    icon = tray_manager.load_icon()
    assert not icon.isNull()
