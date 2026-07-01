# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import os
import logging
from hydrateme.desktop.generic import DesktopEnvironment
from hydrateme.desktop.gnome import GnomeBackend
from hydrateme.desktop.kde import KDEBackend
from hydrateme.desktop.xfce import XFCEBackend

logger = logging.getLogger("hydrateme")

def get_desktop_environment() -> DesktopEnvironment:
    """
    Detects the current desktop session and resolves the appropriate backend.
    """
    desktop = os.environ.get("XDG_CURRENT_DESKTOP", "").upper()
    session = os.environ.get("DESKTOP_SESSION", "").upper()

    logger.info(f"Desktop detection triggers: XDG_CURRENT_DESKTOP='{desktop}', DESKTOP_SESSION='{session}'")

    if "GNOME" in desktop or "GNOME" in session:
        return GnomeBackend()
    elif "KDE" in desktop or "KDE" in session:
        return KDEBackend()
    elif "XFCE" in desktop or "XFCE" in session:
        return XFCEBackend()
    else:
        return DesktopEnvironment()
