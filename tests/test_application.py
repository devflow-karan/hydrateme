# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import pytest
from unittest.mock import MagicMock
from hydrateme.application import HydrateMeApplication

def test_application_start_with_tray(clean_config_file, monkeypatch, qapp):
    """
    Verifies scheduler initialization states under standard startup conditions.
    """
    monkeypatch.setattr("PyQt6.QtWidgets.QSystemTrayIcon.isSystemTrayAvailable", lambda: True)
    monkeypatch.setattr("PyQt6.QtWidgets.QSystemTrayIcon.show", MagicMock())
    
    args = MagicMock(debug=False)
    app = HydrateMeApplication(qapp, args)
    
    # Force tray setup checks
    monkeypatch.setattr(app.tray_manager, "initialize", lambda: True)
    
    app.start()
    assert app.scheduler.timer.isActive() is True

def test_application_reminder_unlocked(clean_config_file, monkeypatch, qapp):
    """
    Verifies that unlocked sessions prompt the ReminderPopup modal attention dialog.
    """
    args = MagicMock(debug=False)
    app = HydrateMeApplication(qapp, args)
    
    app.desktop_env.is_locked = MagicMock(return_value=False)
    app.sound_manager.play_reminder_sound = MagicMock()
    app.sound_manager.stop_sound = MagicMock()
    
    mock_popup = MagicMock()
    monkeypatch.setattr("hydrateme.application.ReminderPopup", lambda parent: mock_popup)
    
    app.show_reminder()
    
    app.sound_manager.play_reminder_sound.assert_called_once()
    mock_popup.exec.assert_called_once()
    app.sound_manager.stop_sound.assert_called_once()
    assert app.scheduler.timer.isActive() is True

def test_application_reminder_locked(clean_config_file, monkeypatch, qapp):
    """
    Verifies that locked sessions bypass popups and trigger DBus fallback notifications.
    """
    args = MagicMock(debug=False)
    app = HydrateMeApplication(qapp, args)
    
    app.desktop_env.is_locked = MagicMock(return_value=True)
    app.sound_manager.play_reminder_sound = MagicMock()
    app.notification_manager.send_notification = MagicMock()
    
    app.show_reminder()
    
    app.sound_manager.play_reminder_sound.assert_called_once()
    app.notification_manager.send_notification.assert_called_once()
    assert app.scheduler.timer.isActive() is True
