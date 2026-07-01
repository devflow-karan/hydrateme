# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import pytest
from PyQt6.QtCore import QTimer
from hydrateme.settings_manager import Config
from hydrateme.scheduler import HydrationScheduler

def test_scheduler_init(clean_config_file, qtbot):
    """
    Verifies default timer states on startup.
    """
    config = Config()
    scheduler = HydrationScheduler(config)
    
    assert scheduler.config == config
    assert scheduler.timer.isActive() is False

def test_scheduler_start_stop(clean_config_file, qtbot):
    """
    Verifies start and stop timer actions.
    """
    config = Config()
    config.interval = 10
    scheduler = HydrationScheduler(config)
    
    scheduler.start()
    assert scheduler.timer.isActive() is True
    assert scheduler.timer.interval() == 10 * 60 * 1000
    
    scheduler.stop()
    assert scheduler.timer.isActive() is False

def test_scheduler_apply(clean_config_file, qtbot):
    """
    Verifies scheduler applies configuration changes.
    """
    config = Config()
    scheduler = HydrationScheduler(config)
    
    scheduler.start()
    assert scheduler.timer.interval() == 30 * 60 * 1000
    
    # Update settings
    config.interval = 60
    scheduler.apply()
    assert scheduler.timer.isActive() is True
    assert scheduler.timer.interval() == 60 * 60 * 1000
    scheduler.stop()

def test_scheduler_timeout_signal(clean_config_file, qtbot):
    """
    Verifies pyqtSignal emissions upon scheduler timeout.
    """
    config = Config()
    scheduler = HydrationScheduler(config)
    
    with qtbot.waitSignal(scheduler.timeout, timeout=1000):
        # Manually trigger execution
        scheduler._on_timeout()
