# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import logging
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QBrush, QColor, QFont
from PyQt6.QtCore import Qt

logger = logging.getLogger("hydrateme")

def create_fallback_icon() -> QIcon:
    """
    Generates a fallback icon programmatically using QPainter.
    Useful when assets are missing or system themes do not contain the app icon.
    """
    logger.info("Generating dynamic fallback icon using QPainter.")
    try:
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw blue droplet/circle representing hydration
        painter.setBrush(QBrush(QColor("#3498db")))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(8, 8, 48, 48)
        
        # Draw text inside
        painter.setPen(QColor("#ffffff"))
        font = QFont()
        font.setBold(True)
        font.setPointSize(28)
        painter.setFont(font)
        
        # Draw the letter 'H' in the center
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "H")
        painter.end()
        
        return QIcon(pixmap)
    except Exception as e:
        logger.error(f"Failed to generate fallback icon dynamically: {e}")
        return QIcon()
