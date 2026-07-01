# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import os
import sys
import logging
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, QObject
from hydrateme.settings_manager import Config
from hydrateme.scheduler import HydrationScheduler
from hydrateme.services.sound import SoundManager
from hydrateme.tray_manager import TrayManager
from hydrateme.notification_manager import NotificationManager
from hydrateme.desktop import get_desktop_environment
from hydrateme.ui.settings import SettingsDialog
from hydrateme.ui.popup import ReminderPopup
from hydrateme.ui.dialogs import WaylandWarningDialog, UpdateDialog

logger = logging.getLogger("hydrateme")

class HydrateMeApplication(QObject):
    """
    Coordinates application lifecycle, binding configuration settings, schedulers,
    notifications, screensaver states, and user dialog interfaces.
    """
    def __init__(self, qapp, args, parent=None):
        super().__init__(parent)
        self.qapp = qapp
        self.args = args
        self.config = Config()
        self.settings_dialog = None
        self.reminder_popup = None
        
        # Prevent auto-exit when all dialogs are closed (runs in background)
        self.qapp.setQuitOnLastWindowClosed(False)
        
        # Setup helpers
        self.sound_manager = SoundManager(self.config)
        self.desktop_env = get_desktop_environment()
        
        # Connect managers
        self.tray_manager = TrayManager(
            self.qapp, 
            open_settings_callback=self.open_settings, 
            quit_callback=self.quit_app
        )
        self.notification_manager = NotificationManager(self.tray_manager)
        
        # Connect timer loops
        self.scheduler = HydrationScheduler(self.config, self)
        self.scheduler.timeout.connect(self.show_reminder)

    def start(self):
        """
        Starts scheduler timers and binds system tray.
        """
        logger.info("Initializing application startup sequence...")
        
        # Bind QSystemTrayIcon
        tray_ok = self.tray_manager.initialize()
        
        # Start timer scheduler
        self.scheduler.start()
        
        # Wayland system tray warning fallback trigger
        if not tray_ok:
            logger.warning("System tray is not available. Launching Wayland fallback mode.")
            QTimer.singleShot(100, self.handle_wayland_fallback)
        else:
            # standard launch settings display
            QTimer.singleShot(100, self.open_settings)
            
        QTimer.singleShot(2000, self.check_for_updates)

    def handle_wayland_fallback(self):
        """
        Pops up helper instruction alerts on system tray absence.
        """
        warning_dlg = WaylandWarningDialog()
        warning_dlg.exec()
        self.open_settings()

    def open_settings(self):
        """
        Raises the Settings dialog panel to focus.
        """
        if not self.settings_dialog:
            self.settings_dialog = SettingsDialog(self.config, self.apply_settings, self)
        self.settings_dialog.show()
        self.settings_dialog.activateWindow()
        self.settings_dialog.raise_()
        logger.info("SettingsDialog rendered to view.")

    def apply_settings(self):
        """
        Callback triggered on configuration adjustments.
        """
        logger.info("Applying updated reminder interval timers.")
        self.scheduler.apply()

    def trigger_sound(self):
        """
        Executes active sound players.
        """
        self.sound_manager.play_reminder_sound()

    def show_reminder(self):
        """
        Triggered when timer scheduler countdown reaches target.
        """
        logger.info("Hydration scheduler interval met. Checking lock screen state.")
        self.scheduler.stop()
        
        if self.desktop_env.is_locked():
            logger.info("Lock screen active. Broadcasting notification updates.")
            self.trigger_sound()
            
            from hydrateme.utils.paths import get_asset_path
            icon_path = get_asset_path("/usr/share/icons/hicolor/scalable/apps/hydrateme.svg")
            
            self.notification_manager.send_notification(
                self.tr("HydrateMe"), 
                self.tr("Time to drink water!"),
                icon_path=icon_path
            )
            # Restart background timer immediately
            self.scheduler.start()
        else:
            logger.info("Desktop unlocked. Launching ReminderPopup dialog modal.")
            self.trigger_sound()
            
            self.reminder_popup = ReminderPopup(self)
            self.reminder_popup.exec()
            
            # Stop loops
            self.sound_manager.stop_sound()
            self.reminder_popup = None
            
            # Restart countdown timer
            self.scheduler.start()

    def check_for_updates(self):
        """
        Performs release check checks.
        """
        logger.info("Starting background update release inspection.")

    def quit_app(self):
        """
        Closes players, releases timers, and requests application quit.
        """
        logger.info("System quit request registered. Releasing hooks.")
        self.sound_manager.stop_sound()
        self.scheduler.stop()
        self.qapp.quit()
