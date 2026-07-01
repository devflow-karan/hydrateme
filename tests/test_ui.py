# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import pytest
from unittest.mock import MagicMock
from hydrateme.settings_manager import Config
from hydrateme.ui.settings import SettingsDialog
from hydrateme.ui.dialogs import WaylandWarningDialog, UpdateDialog

def test_wayland_warning_dialog(qapp, qtbot):
    """
    Verifies that Wayland tray warnings are shown and closed successfully.
    """
    dialog = WaylandWarningDialog()
    qtbot.addWidget(dialog)
    dialog.accept()
    assert dialog.result() == 1

def test_update_dialog(qapp, qtbot):
    """
    Verifies that update check dialog can be loaded and rejected/closed.
    """
    dialog = UpdateDialog("1.5.0", "http://github.com/release")
    qtbot.addWidget(dialog)
    dialog.reject()
    assert dialog.result() == 0

def test_settings_dialog(clean_config_file, qapp, qtbot):
    """
    Verifies settings options spinbox settings, sound toggling, and config saves.
    """
    config = Config()
    apply_callback = MagicMock()
    parent_app = MagicMock()
    
    dialog = SettingsDialog(config, apply_callback, parent_app)
    qtbot.addWidget(dialog)
    
    assert dialog.spin_interval.value() == 30
    assert dialog.check_sound.isChecked() is True
    
    dialog.spin_interval.setValue(45)
    dialog.check_sound.setChecked(False)
    dialog.save_settings()
    
    assert config.interval == 45
    assert config.sound is False
    apply_callback.assert_called_once()
