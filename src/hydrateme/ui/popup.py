# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import os
import logging
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QGraphicsDropShadowEffect
from PyQt6.QtGui import QFont, QPixmap, QColor
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation
from hydrateme.utils.assets import get_themed_icon
from hydrateme.ui.widgets.card import CardWidget
from hydrateme.ui.widgets.buttons import PrimaryButton, SecondaryButton

logger = logging.getLogger("hydrateme")

class ReminderPopup(QDialog):
    """
    Redesigned modern centered hydration reminder popup window.
    Features rounded corners, soft drop shadow, high-res logo,
    fade-in animation, and Snooze support.
    """
    def __init__(self, parent_app):
        super().__init__()
        self.parent_app = parent_app
        
        self.setWindowTitle(self.tr("HydrateMe Reminder"))
        
        # Transparent background for the outer dialog to allow rendering drop shadows
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.Tool
        )
        
        # Set outer dimensions, adding margin for drop shadow spacing
        self.setFixedSize(440, 300)
        
        # Outer layout
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(16, 16, 16, 16)
        
        # Inner Card Widget
        self.card = CardWidget(self)
        # Apply specific style for the card in this popup
        self.card.setStyleSheet("""
            QFrame#CardWidget {
                background-color: #1E1E1E;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
            }
        """)
        outer_layout.addWidget(self.card)
        
        # Add soft drop shadow effect
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(16)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.shadow.setOffset(0, 4)
        self.card.setGraphicsEffect(self.shadow)
        
        # Card body layout
        card_layout = self.card.card_layout
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(12)
        
        # Droplet logo
        logo_layout = QHBoxLayout()
        self.lbl_logo = QLabel()
        from hydrateme.utils.paths import get_bundled_asset_path
        logo_path = get_bundled_asset_path("images/logo.png")
        if os.path.exists(logo_path):
            pix = QPixmap(logo_path).scaled(56, 56, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.lbl_logo.setPixmap(pix)
        else:
            icon = get_themed_icon("water")
            self.lbl_logo.setPixmap(icon.pixmap(56, 56))
            
        logo_layout.addStretch()
        logo_layout.addWidget(self.lbl_logo)
        logo_layout.addStretch()
        card_layout.addLayout(logo_layout)
        
        # Title
        self.lbl_title = QLabel(self.tr("Time to drink water!"))
        font_title = QFont("Ubuntu", 18)
        font_title.setBold(True)
        self.lbl_title.setFont(font_title)
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_title.setStyleSheet("color: #FFFFFF;")
        card_layout.addWidget(self.lbl_title)
        
        # Subtitle
        self.lbl_subtitle = QLabel(self.tr("Your body will thank you."))
        font_sub = QFont("Ubuntu", 11)
        self.lbl_subtitle.setFont(font_sub)
        self.lbl_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_subtitle.setStyleSheet("color: #C8C8C8;")
        card_layout.addWidget(self.lbl_subtitle)
        
        # Action Buttons Layout
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        self.btn_snooze = SecondaryButton(self.tr("Snooze (15 min)"))
        self.btn_snooze.clicked.connect(self.on_snooze)
        
        self.btn_done = PrimaryButton(self.tr("I drank water"))
        self.btn_done.clicked.connect(self.on_done)
        
        btn_layout.addWidget(self.btn_snooze)
        btn_layout.addWidget(self.btn_done)
        card_layout.addLayout(btn_layout)
        
        # Fade-in Animation (300ms)
        self.setWindowOpacity(0.0)
        self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_anim.setDuration(300)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.start()
        
        # Looping sound playing timer (trigger sound alert every 10 seconds)
        self.loop_timer = QTimer(self)
        self.loop_timer.timeout.connect(self.parent_app.trigger_sound)
        self.loop_timer.start(10000)
        
        logger.info("ReminderPopup window active; looping sound timer started.")

    def on_done(self):
        logger.info("Hydration acknowledgment clicked.")
        self.loop_timer.stop()
        self.accept()

    def on_snooze(self):
        logger.info("Hydration snooze clicked.")
        self.loop_timer.stop()
        # Close popup returning custom snooze dialog code (2)
        self.done(2)
