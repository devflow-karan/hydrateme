# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import os
import logging
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QBrush, QColor, QFont, QPen, QPainterPath
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
        
        # Draw blue droplet representing hydration
        painter.setBrush(QBrush(QColor("#2F80ED")))
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

def draw_custom_icon(icon_name: str, color_hex: str = "#2F80ED") -> QIcon:
    """
    Draws custom vector fallback icons programmatically.
    """
    try:
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        color = QColor(color_hex)
        painter.setPen(QPen(color, 4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        
        if icon_name == "settings":
            painter.drawEllipse(22, 22, 20, 20)
            for i in range(8):
                angle = i * 45
                painter.save()
                painter.translate(32, 32)
                painter.rotate(angle)
                painter.drawLine(0, -10, 0, -16)
                painter.restore()
        elif icon_name == "sound":
            path = QPainterPath()
            path.moveTo(16, 24)
            path.lineTo(24, 24)
            path.lineTo(34, 14)
            path.lineTo(34, 50)
            path.lineTo(24, 40)
            path.lineTo(16, 40)
            path.closeSubpath()
            painter.setBrush(QBrush(color))
            painter.drawPath(path)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawArc(26, 12, 24, 40, -60 * 16, 120 * 16)
        elif icon_name == "bell":
            path = QPainterPath()
            path.moveTo(32, 12)
            path.cubicTo(20, 16, 20, 44, 16, 48)
            path.lineTo(48, 48)
            path.cubicTo(48, 44, 48, 16, 32, 12)
            painter.setBrush(QBrush(color))
            painter.drawPath(path)
            painter.drawEllipse(28, 48, 8, 4)
        elif icon_name == "water":
            path = QPainterPath()
            path.moveTo(32, 10)
            path.cubicTo(32, 10, 14, 30, 14, 44)
            path.cubicTo(14, 54, 50, 54, 50, 44)
            path.cubicTo(50, 30, 32, 10, 32, 10)
            path.closeSubpath()
            painter.setBrush(QBrush(color))
            painter.drawPath(path)
        elif icon_name == "timer":
            painter.drawEllipse(12, 12, 40, 40)
            painter.drawLine(32, 32, 32, 20)
            painter.drawLine(32, 32, 42, 32)
        elif icon_name == "folder":
            path = QPainterPath()
            path.moveTo(10, 16)
            path.lineTo(24, 16)
            path.lineTo(30, 22)
            path.lineTo(54, 22)
            path.lineTo(54, 48)
            path.lineTo(10, 48)
            path.closeSubpath()
            painter.setBrush(QBrush(color))
            painter.drawPath(path)
        elif icon_name == "about":
            painter.drawEllipse(12, 12, 40, 40)
            painter.setBrush(QBrush(color))
            painter.drawEllipse(30, 20, 4, 4)
            painter.drawLine(32, 28, 32, 42)
        elif icon_name == "quit":
            painter.drawArc(16, 16, 32, 32, -45 * 16, 270 * 16)
            painter.drawLine(32, 10, 32, 28)
        elif icon_name == "pause":
            painter.setBrush(QBrush(color))
            painter.drawRect(20, 16, 6, 32)
            painter.drawRect(38, 16, 6, 32)
        elif icon_name == "play":
            path = QPainterPath()
            path.moveTo(20, 14)
            path.lineTo(48, 32)
            path.lineTo(20, 50)
            path.closeSubpath()
            painter.setBrush(QBrush(color))
            painter.drawPath(path)
        elif icon_name == "save":
            path = QPainterPath()
            path.moveTo(14, 14)
            path.lineTo(42, 14)
            path.lineTo(50, 22)
            path.lineTo(50, 50)
            path.lineTo(14, 50)
            path.closeSubpath()
            painter.setBrush(QBrush(color))
            painter.drawPath(path)
        elif icon_name == "cancel":
            painter.drawLine(18, 18, 46, 46)
            painter.drawLine(46, 18, 18, 46)
        else:
            painter.drawRect(16, 16, 32, 32)
            
        painter.end()
        return QIcon(pixmap)
    except Exception as e:
        logger.error(f"Failed to draw custom icon '{icon_name}': {e}")
        return QIcon()

def get_themed_icon(icon_name: str, color_hex: str = "#2F80ED") -> QIcon:
    """
    Resolves an icon using system theme, local bundled files, or dynamic painter fallbacks.
    """
    # 1. System Theme mapping
    theme_mapping = {
        "settings": ["preferences-system", "settings"],
        "sound": ["audio-volume-high", "sound"],
        "bell": ["notification-properties", "bell"],
        "water": ["water", "droplet"],
        "timer": ["alarm-clock", "timer"],
        "folder": ["folder-open", "folder"],
        "about": ["help-about", "info"],
        "quit": ["application-exit", "exit"],
        "pause": ["media-playback-pause", "pause"],
        "play": ["media-playback-start", "play"],
        "save": ["document-save", "save"],
        "cancel": ["window-close", "cancel"]
    }
    
    names = theme_mapping.get(icon_name, [icon_name])
    for name in names:
        icon = QIcon.fromTheme(name)
        if not icon.isNull() and not icon.pixmap(24, 24).isNull():
            return icon
            
    # 2. Check local bundled files inside src/hydrateme/assets/icons/
    try:
        from hydrateme.utils.paths import get_bundled_asset_path
        icon_path = get_bundled_asset_path(f"icons/{icon_name}.png")
        if os.path.exists(icon_path):
            icon = QIcon(icon_path)
            if not icon.isNull() and not icon.pixmap(24, 24).isNull():
                return icon
    except Exception:
        pass
        
    # 3. Dynamic programmatic fallback drawing
    return draw_custom_icon(icon_name, color_hex)
