# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import os
import sys
import logging
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt

logger = logging.getLogger("hydrateme")

class WaylandWarningDialog(QDialog):
    """
    Dialog prompt indicating that QSystemTrayIcon is unavailable,
    which commonly happens in native Wayland sessions lacking app-indicator shells.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("HydrateMe - System Tray Alert"))
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.resize(400, 180)
        
        layout = QVBoxLayout()
        
        label = QLabel(
            self.tr("<b>System Tray Unavailable:</b><br><br>"
                    "The application cannot initialize a tray icon because the desktop environment "
                    "does not support the StatusNotifierItem (SNI) protocol.<br><br>"
                    "HydrateMe will run in the background. Launching a new instance from the "
                    "applications list will pop up these Settings again.")
        )
        label.setWordWrap(True)
        label.setAccessibleName("Wayland system tray warning message")
        layout.addWidget(label)
        
        btn_layout = QHBoxLayout()
        btn_ok = QPushButton(self.tr("&OK"))
        btn_ok.setAccessibleName("Acknowledge warning button")
        btn_ok.clicked.connect(self.accept)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_ok)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)


class UpdateDialog(QDialog):
    """
    Dialog alert notifying the user of newer application version releases.
    """
    def __init__(self, latest_version: str, release_url: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("HydrateMe - Update Available"))
        self.resize(420, 160)
        
        layout = QVBoxLayout()
        
        label = QLabel(
            self.tr(f"A new version (v{latest_version}) of HydrateMe has been released!<br><br>"
                    "Please visit the distribution channel or GitHub Releases to upgrade.")
        )
        label.setWordWrap(True)
        label.setAccessibleName("Application update notification text")
        layout.addWidget(label)
        
        lbl_url = QLabel(f"<a href='{release_url}'>{release_url}</a>")
        lbl_url.setOpenExternalLinks(True)
        lbl_url.setAccessibleName("GitHub release external download URL")
        layout.addWidget(lbl_url)
        
        btn_layout = QHBoxLayout()
        btn_close = QPushButton(self.tr("&Close"))
        btn_close.setAccessibleName("Close update dialog button")
        btn_close.clicked.connect(self.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_close)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
