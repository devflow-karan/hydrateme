# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QWidget

class CardWidget(QFrame):
    """
    A styled QFrame container representing a modern GNOME-style card.
    Uses parent styles for dynamic Dark/Light theme adaptation.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("CardWidget")
        
        self.card_layout = QVBoxLayout(self)
        self.card_layout.setContentsMargins(16, 12, 16, 12)
        self.card_layout.setSpacing(12)

    def add_row(self, left_widget: QWidget, right_widget: QWidget):
        """
        Helper to append a key-value settings layout row.
        """
        row_layout = QHBoxLayout()
        row_layout.addWidget(left_widget)
        row_layout.addStretch()
        row_layout.addWidget(right_widget)
        self.card_layout.addLayout(row_layout)
