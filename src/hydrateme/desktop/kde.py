# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

from hydrateme.desktop.generic import DesktopEnvironment

class KDEBackend(DesktopEnvironment):
    """
    Backend tailored for KDE Plasma sessions.
    """
    def get_name(self) -> str:
        return "KDE Plasma"
