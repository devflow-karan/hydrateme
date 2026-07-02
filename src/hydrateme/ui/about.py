# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import os
import platform
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from hydrateme.utils.assets import get_themed_icon
from hydrateme.ui.widgets.buttons import PrimaryButton, SecondaryButton
from hydrateme.ui.widgets.card import CardWidget

class AboutWidget(QWidget):
    """
    A reusable widget presenting the diagnostic information and branding of HydrateMe.
    Can be embedded inside Settings Dialog pages or wrapped by a standalone Dialog.
    """
    def __init__(self, show_close_button: bool = False, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        
        # Header layout (Icon + Title/Version)
        header_layout = QHBoxLayout()
        header_layout.setSpacing(16)
        
        lbl_logo = QLabel()
        from hydrateme.utils.paths import get_bundled_asset_path
        logo_path = get_bundled_asset_path("images/logo.png")
        if os.path.exists(logo_path):
            pix = QPixmap(logo_path).scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            lbl_logo.setPixmap(pix)
        else:
            icon = get_themed_icon("water")
            lbl_logo.setPixmap(icon.pixmap(64, 64))
            
        header_layout.addWidget(lbl_logo)
        
        title_layout = QVBoxLayout()
        lbl_title = QLabel(self.tr("<b>HydrateMe</b>"))
        lbl_title.setStyleSheet("font-size: 20px; font-weight: bold;")
        
        from hydrateme.services.crash import APP_VERSION
        lbl_ver = QLabel(f"Version {APP_VERSION}")
        lbl_ver.setStyleSheet("font-size: 13px; color: #888888;")
        
        title_layout.addWidget(lbl_title)
        title_layout.addWidget(lbl_ver)
        title_layout.addStretch()
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Details Card
        card = CardWidget()
        
        from hydrateme.desktop import get_desktop_environment
        de = get_desktop_environment()
        de_name = f"{de.get_name()} (Wayland)" if os.environ.get("WAYLAND_DISPLAY") else f"{de.get_name()} (X11)"
        
        from PyQt6.QtCore import QT_VERSION_STR
        qt_ver = QT_VERSION_STR
        py_ver = f"{platform.python_version()}"
        
        lbl_author_key = QLabel(self.tr("Author:"))
        lbl_author_val = QLabel("Karan Kumar")
        lbl_author_val.setStyleSheet("font-weight: bold;")
        card.add_row(lbl_author_key, lbl_author_val)
        
        lbl_github_key = QLabel(self.tr("GitHub:"))
        lbl_github_val = QLabel("<a href='https://github.com/devflow-karan/hydrateme' style='color:#4EA8FF;'>devflow-karan/hydrateme</a>")
        lbl_github_val.setOpenExternalLinks(True)
        card.add_row(lbl_github_key, lbl_github_val)
        
        lbl_lic_key = QLabel(self.tr("License:"))
        lbl_lic_val = QLabel("MIT")
        card.add_row(lbl_lic_key, lbl_lic_val)
        
        lbl_de_key = QLabel(self.tr("Desktop:"))
        lbl_de_val = QLabel(de_name)
        card.add_row(lbl_de_key, lbl_de_val)
        
        lbl_qt_key = QLabel(self.tr("Qt Version:"))
        lbl_qt_val = QLabel(qt_ver)
        card.add_row(lbl_qt_key, lbl_qt_val)
        
        lbl_py_key = QLabel(self.tr("Python Version:"))
        lbl_py_val = QLabel(py_ver)
        card.add_row(lbl_py_key, lbl_py_val)
        
        layout.addWidget(card)
        
        # Action Buttons
        btn_layout = QHBoxLayout()
        self.btn_update = SecondaryButton(self.tr("&Check Updates"))
        self.btn_update.clicked.connect(self.check_updates)
        btn_layout.addWidget(self.btn_update)
        
        if show_close_button:
            btn_layout.addStretch()
            self.btn_close = PrimaryButton(self.tr("&Close"))
            btn_layout.addWidget(self.btn_close)
        else:
            self.btn_update.setMinimumWidth(150)
            
        layout.addLayout(btn_layout)

    def check_updates(self):
        logger.info("Manual update check triggered from About Page.")
        try:
            # Climb parents to find coordinate context or dialog parent
            curr = self.parent()
            while curr:
                if hasattr(curr, "parent_app") and curr.parent_app:
                    curr.parent_app.check_for_updates()
                    break
                curr = curr.parent()
        except Exception as e:
            logger.warning(f"Failed to pass updates request: {e}")


class AboutDialog(QDialog):
    """
    Dialog wrapper for AboutWidget to support modular popup checks.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(self.tr("About HydrateMe"))
        self.setFixedSize(450, 420)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        
        self.widget = AboutWidget(show_close_button=True, parent=self)
        self.widget.btn_close.clicked.connect(self.accept)
        layout.addWidget(self.widget)
