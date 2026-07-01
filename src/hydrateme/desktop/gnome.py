# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

from hydrateme.desktop.generic import DesktopEnvironment

class GnomeBackend(DesktopEnvironment):
    """
    Backend tailored for GNOME desktop sessions.
    """
    def get_name(self) -> str:
        return "GNOME"
