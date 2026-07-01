# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import logging
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer

logger = logging.getLogger("hydrateme")

class ReminderPopup(QDialog):
    """
    Frameless, modal alert dialog that displays on top of all windows
    to remind the user to drink water. Runs a looping timer for sound playing.
    """
    def __init__(self, parent_app):
        super().__init__()
        self.parent_app = parent_app
        
        self.setWindowTitle(self.tr("HydrateMe Reminder"))
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.Tool
        )
        self.setStyleSheet(
            "background-color: #1e1e2e; color: #cdd6f4; border: 2px solid #89b4fa; border-radius: 12px;"
        )
        
        layout = QVBoxLayout()
        
        label = QLabel(self.tr("💧 Time to Drink Water! 💧"))
        font = QFont()
        font.setPointSize(22)
        font.setBold(True)
        label.setFont(font)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setAccessibleName(self.tr("Drink water reminder title text"))
        layout.addWidget(label)
        
        btn_done = QPushButton(self.tr("&I drank water"))
        btn_done.setStyleSheet(
            "background-color: #89b4fa; color: #11111b; padding: 10px; border-radius: 6px; font-weight: bold; font-size: 15px;"
        )
        btn_done.setAccessibleName(self.tr("Acknowledge drinking water button"))
        btn_done.clicked.connect(self.on_done)
        layout.addWidget(btn_done)
        
        self.setLayout(layout)
        self.setFixedSize(400, 200)
        
        # Periodic alarm loop
        self.loop_timer = QTimer(self)
        self.loop_timer.timeout.connect(self.parent_app.trigger_sound)
        self.loop_timer.start(10000)
        
        logger.info("ReminderPopup window active; looping sound timer started.")

    def on_done(self):
        """
        Invoked when the user confirms hydration. Stops alarm loops and closes popup.
        """
        logger.info("Hydration acknowledgment clicked.")
        self.loop_timer.stop()
        self.accept()
