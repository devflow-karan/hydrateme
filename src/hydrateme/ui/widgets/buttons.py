# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize

class PrimaryButton(QPushButton):
    """
    Styled primary action button (e.g. Save, Confirm).
    """
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setObjectName("PrimaryButton")


class SecondaryButton(QPushButton):
    """
    Styled secondary action button (e.g. Clear, Cancel).
    """
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setObjectName("SecondaryButton")


class IconButton(QPushButton):
    """
    Pre-styled icon-only button with hover background circular indicators.
    """
    def __init__(self, icon: QIcon, text: str = "", parent=None):
        if text:
            super().__init__(icon, text, parent)
        else:
            super().__init__(parent)
            self.setIcon(icon)
            self.setIconSize(QSize(20, 20))
        self.setObjectName("IconButton")
