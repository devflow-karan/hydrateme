# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import os
import logging
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
from hydrateme.ui.widgets.buttons import PrimaryButton
from hydrateme.ui.widgets.card import CardWidget
from hydrateme.ui.theme import get_theme_stylesheet, detect_system_dark_mode

logger = logging.getLogger("hydrateme")

class WaylandWarningDialog(QDialog):
    """
    Redesigned WaylandWarningDialog prompt matching visual language.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("System Tray Alert"))
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setFixedSize(420, 220)
        
        # Load stylesheet
        from hydrateme.settings_manager import Config
        config = Config()
        is_dark = detect_system_dark_mode() if config.theme == "auto" else (config.theme == "dark")
        self.setStyleSheet(get_theme_stylesheet(is_dark))
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        card = CardWidget()
        
        lbl_msg = QLabel(
            self.tr("<b>System Tray Unavailable:</b><br><br>"
                    "The application cannot initialize a tray icon because the desktop environment "
                    "does not support the StatusNotifierItem (SNI) protocol.<br><br>"
                    "HydrateMe will run in the background. Launching a new instance from the "
                    "applications list will pop up these Settings again.")
        )
        lbl_msg.setWordWrap(True)
        lbl_msg.setAccessibleName("Wayland system tray warning message")
        card.card_layout.addWidget(lbl_msg)
        layout.addWidget(card)
        
        btn_layout = QHBoxLayout()
        btn_ok = PrimaryButton(self.tr("&OK"))
        btn_ok.setAccessibleName("Acknowledge warning button")
        btn_ok.clicked.connect(self.accept)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_ok)
        layout.addLayout(btn_layout)


class UpdateDialog(QDialog):
    """
    Redesigned UpdateDialog alert matching visual language.
    """
    def __init__(self, latest_version: str, release_url: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("Update Available"))
        self.setFixedSize(440, 200)
        
        # Load stylesheet
        from hydrateme.settings_manager import Config
        config = Config()
        is_dark = detect_system_dark_mode() if config.theme == "auto" else (config.theme == "dark")
        self.setStyleSheet(get_theme_stylesheet(is_dark))
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        card = CardWidget()
        
        lbl_msg = QLabel(
            self.tr(f"A new version (v{latest_version}) of HydrateMe has been released!<br><br>"
                    f"Please visit the distribution channel or GitHub Releases to upgrade.<br>"
                    f"URL: <a href='{release_url}' style='color:#4EA8FF;'>{release_url}</a>")
        )
        lbl_msg.setOpenExternalLinks(True)
        lbl_msg.setWordWrap(True)
        lbl_msg.setAccessibleName("Application update notification text")
        card.card_layout.addWidget(lbl_msg)
        layout.addWidget(card)
        
        btn_layout = QHBoxLayout()
        btn_close = PrimaryButton(self.tr("&Close"))
        btn_close.setAccessibleName("Close update dialog button")
        btn_close.clicked.connect(self.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_close)
        layout.addLayout(btn_layout)
