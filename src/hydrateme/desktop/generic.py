# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import dbus
import logging

logger = logging.getLogger("hydrateme")

class DesktopEnvironment:
    """
    Polymorphic base class representing the current Linux desktop environment.
    """
    def get_name(self) -> str:
        return "Generic Linux"

    def is_locked(self) -> bool:
        """
        Default screensaver lock verification using DBus endpoints.
        """
        # Try generic freedesktop screensaver (KDE, Cinnamon, MATE, XFCE etc.)
        try:
            bus = dbus.SessionBus()
            screensaver = bus.get_object("org.freedesktop.ScreenSaver", "/ScreenSaver")
            is_active = screensaver.GetActive(dbus_interface="org.freedesktop.ScreenSaver")
            logger.debug(f"org.freedesktop.ScreenSaver returned lock active={is_active}")
            return bool(is_active)
        except Exception as e:
            logger.debug(f"Failed to query org.freedesktop.ScreenSaver: {e}")

        # Try GNOME screensaver
        try:
            bus = dbus.SessionBus()
            screensaver = bus.get_object("org.gnome.ScreenSaver", "/org/gnome/ScreenSaver")
            is_active = screensaver.GetActive(dbus_interface="org.gnome.ScreenSaver")
            logger.debug(f"org.gnome.ScreenSaver returned lock active={is_active}")
            return bool(is_active)
        except Exception as e:
            logger.debug(f"Failed to query org.gnome.ScreenSaver: {e}")

        return False
