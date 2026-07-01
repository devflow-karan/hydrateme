# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import os
from unittest.mock import MagicMock
from hydrateme.desktop import get_desktop_environment
from hydrateme.desktop.generic import DesktopEnvironment
from hydrateme.desktop.gnome import GnomeBackend
from hydrateme.desktop.kde import KDEBackend
from hydrateme.desktop.xfce import XFCEBackend

def test_desktop_detection(monkeypatch):
    """
    Verifies detection of current desktop session environments.
    """
    monkeypatch.setenv("XDG_CURRENT_DESKTOP", "GNOME")
    de = get_desktop_environment()
    assert isinstance(de, GnomeBackend)
    assert de.get_name() == "GNOME"
    
    monkeypatch.setenv("XDG_CURRENT_DESKTOP", "KDE")
    de = get_desktop_environment()
    assert isinstance(de, KDEBackend)
    assert de.get_name() == "KDE Plasma"
    
    monkeypatch.setenv("XDG_CURRENT_DESKTOP", "XFCE")
    de = get_desktop_environment()
    assert isinstance(de, XFCEBackend)
    assert de.get_name() == "XFCE"
    
    monkeypatch.delenv("XDG_CURRENT_DESKTOP", raising=False)
    monkeypatch.delenv("DESKTOP_SESSION", raising=False)
    de = get_desktop_environment()
    assert isinstance(de, DesktopEnvironment)
    assert de.get_name() == "Generic Linux"

def test_screensaver_locked(mock_dbus):
    """
    Verifies lock check hooks on mock screensaver services.
    """
    de = DesktopEnvironment()
    assert de.is_locked() is False
    
    mock_dbus["screensaver"].GetActive.return_value = True
    assert de.is_locked() is True
