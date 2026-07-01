# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

from unittest.mock import MagicMock
from hydrateme.notification_manager import NotificationManager

def test_notification_priority_tray():
    """
    Verifies that system tray messages are used if active.
    """
    mock_tray = MagicMock()
    mock_tray.is_tray_available.return_value = True
    
    nm = NotificationManager(mock_tray)
    assert nm.send_notification("Title", "Message") is True
    mock_tray.show_message.assert_called_once_with("Title", "Message")

def test_notification_priority_dbus(mock_dbus, monkeypatch):
    """
    Verifies fallback to DBus interface if tray is unavailable.
    """
    nm = NotificationManager(tray_manager=None)
    assert nm.send_notification("Title", "Message", "/tmp/icon.svg") is True
    mock_dbus["interface"].Notify.assert_called_once()

def test_notification_priority_subprocess(monkeypatch):
    """
    Verifies fallback to notify-send subprocess if DBus fails.
    """
    mock_run = MagicMock()
    mock_run.return_value.returncode = 0
    monkeypatch.setattr("subprocess.run", mock_run)
    
    def raise_dbus_err():
        raise Exception("DBus Connection Failure")
    monkeypatch.setattr("dbus.SessionBus", raise_dbus_err)
    
    nm = NotificationManager(tray_manager=None)
    assert nm.send_notification("Title", "Message") is True
    mock_run.assert_called_once()
    args = mock_run.call_args[0][0]
    assert args[0] == "notify-send"
