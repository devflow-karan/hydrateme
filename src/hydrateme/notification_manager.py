# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import subprocess
import logging
import dbus
from PyQt6.QtWidgets import QMessageBox

logger = logging.getLogger("hydrateme")

class NotificationManager:
    """
    Coordinates reminder delivery using the fallback chain:
    1. Qt System Tray Message
    2. DBus Interface (org.freedesktop.Notifications)
    3. subprocess call to notify-send
    4. QMessageBox Dialog Popup
    """
    def __init__(self, tray_manager=None):
        self.tray_manager = tray_manager

    def send_notification(self, title: str, message: str, icon_path: str = "") -> bool:
        """
        Attempts to display a desktop notification following the prioritised chain.
        """
        logger.info(f"Delivering notification alert: {title} - {message}")

        # 1. Qt System Tray
        if self.tray_manager and self.tray_manager.is_tray_available():
            logger.info("Attempting notification via Qt System Tray...")
            try:
                self.tray_manager.show_message(title, message)
                logger.info("Notification displayed via System Tray.")
                return True
            except Exception as e:
                logger.warning(f"Qt System Tray showMessage failed: {e}")

        # 2. DBus
        try:
            logger.info("Attempting notification via Session DBus Interface...")
            bus = dbus.SessionBus()
            notif_obj = bus.get_object('org.freedesktop.Notifications', '/org/freedesktop/Notifications')
            notif_interface = dbus.Interface(notif_obj, 'org.freedesktop.Notifications')
            notif_interface.Notify(
                "HydrateMe",
                0,
                icon_path,
                title,
                message,
                [],
                {"urgency": dbus.Byte(2)},  # High/critical priority
                10000  # Duration: 10s
            )
            logger.info("Notification sent via DBus interface.")
            return True
        except Exception as e:
            logger.warning(f"DBus notification failed: {e}")

        # 3. notify-send CLI
        try:
            logger.info("Attempting notification via notify-send shell command...")
            cmd = ["notify-send", "-u", "critical", "-t", "10000"]
            if icon_path:
                cmd.extend(["-i", icon_path])
            cmd.extend([title, message])
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
            if res.returncode == 0:
                logger.info("Notification delivered via notify-send command.")
                return True
        except Exception as e:
            logger.warning(f"notify-send execution failed: {e}")

        # 4. QMessageBox Fallback Dialog
        try:
            logger.info("Attempting notification fallback via QMessageBox...")
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle(title)
            msg_box.setText(message)
            msg_box.exec()
            logger.info("Notification alert dismissed via fallback QMessageBox.")
            return True
        except Exception as e:
            logger.critical(f"All notification channels failed to execute: {e}")

        return False
