# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import pytest
from unittest.mock import MagicMock
from PyQt6.QtCore import Qt
from hydrateme.ui.popup import ReminderPopup

def test_reminder_popup_init(clean_config_file, qtbot):
    """
    Verifies window properties, styles, and alarm loops on creation.
    """
    mock_app = MagicMock()
    popup = ReminderPopup(mock_app)
    qtbot.addWidget(popup)
    
    flags = popup.windowFlags()
    assert bool(flags & Qt.WindowType.WindowStaysOnTopHint)
    assert bool(flags & Qt.WindowType.FramelessWindowHint)
    assert bool(flags & Qt.WindowType.Tool)
    
    assert popup.loop_timer.isActive() is True
    assert popup.loop_timer.interval() == 10000

def test_reminder_popup_acknowledge(clean_config_file, qtbot):
    """
    Verifies user dialog acknowledgments stop timers.
    """
    mock_app = MagicMock()
    popup = ReminderPopup(mock_app)
    qtbot.addWidget(popup)
    
    with qtbot.waitSignal(popup.accepted, timeout=1000):
        popup.on_done()
        
    assert popup.loop_timer.isActive() is False
