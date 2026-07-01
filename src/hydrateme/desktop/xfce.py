# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

from hydrateme.desktop.generic import DesktopEnvironment

class XFCEBackend(DesktopEnvironment):
    """
    Backend tailored for XFCE sessions.
    """
    def get_name(self) -> str:
        return "XFCE"
