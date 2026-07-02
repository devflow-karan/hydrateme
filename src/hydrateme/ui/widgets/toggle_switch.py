# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

from PyQt6.QtWidgets import QAbstractButton
from PyQt6.QtGui import QPainter, QColor, QBrush
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, pyqtProperty

class ToggleSwitch(QAbstractButton):
    """
    A custom modern iOS/GNOME-style sliding toggle switch.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setFixedSize(50, 26)
        self._thumb_position = 3.0
        self._animation = QPropertyAnimation(self, b"thumb_position", self)
        self._animation.setDuration(120)
        self.toggled.connect(self._on_toggled)

    @pyqtProperty(float)
    def thumb_position(self) -> float:
        return self._thumb_position

    @thumb_position.setter
    def thumb_position(self, pos: float):
        self._thumb_position = pos
        self.update()

    def _on_toggled(self, checked: bool):
        self._animation.stop()
        if checked:
            self._animation.setEndValue(27.0)
        else:
            self._animation.setEndValue(3.0)
        self._animation.start()

    def sizeHint(self) -> QSize:
        return QSize(50, 26)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Greenish success or primary accent when checked, dark grey when unchecked
        if self.isChecked():
            bg_color = QColor("#2F80ED")
        else:
            bg_color = QColor("#444446")
            
        thumb_color = QColor("#FFFFFF")
        
        # Draw background track
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 13, 13)
        
        # Draw slider thumb
        painter.setBrush(QBrush(thumb_color))
        painter.drawEllipse(int(self._thumb_position), 3, 20, 20)
        painter.end()
