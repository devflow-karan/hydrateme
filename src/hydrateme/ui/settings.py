# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import os
import logging
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QCheckBox, QPushButton, QFileDialog
)
from PyQt6.QtCore import Qt

logger = logging.getLogger("hydrateme")

class SettingsDialog(QDialog):
    """
    Settings interface widget for editing reminder intervals, toggling sound options,
    selecting custom sound files, and saving configuration settings.
    """
    def __init__(self, config, apply_callback, parent_app):
        super().__init__()
        self.config = config
        self.apply_callback = apply_callback
        self.parent_app = parent_app
        
        self.setWindowTitle(self.tr("HydrateMe Settings"))
        self.resize(380, 240)
        
        layout = QVBoxLayout()
        
        # Interval setting
        hlayout = QHBoxLayout()
        lbl_interval = QLabel(self.tr("Reminder &Interval (minutes):"))
        self.spin_interval = QSpinBox()
        lbl_interval.setBuddy(self.spin_interval)
        self.spin_interval.setRange(1, 240)
        self.spin_interval.setValue(self.config.interval)
        self.spin_interval.setAccessibleName(self.tr("Reminder Interval Spinbox"))
        
        hlayout.addWidget(lbl_interval)
        hlayout.addWidget(self.spin_interval)
        layout.addLayout(hlayout)
        
        # Sound setting
        self.check_sound = QCheckBox(self.tr("Play &sound with reminder"))
        self.check_sound.setChecked(self.config.sound)
        self.check_sound.setAccessibleName(self.tr("Sound Notification Enabled Checkbox"))
        layout.addWidget(self.check_sound)
        
        # Autostart setting
        self.check_autostart = QCheckBox(self.tr("Launch on &startup"))
        self.check_autostart.setChecked(self.config.autostart)
        self.check_autostart.setAccessibleName(self.tr("Launch Application on System Startup Checkbox"))
        layout.addWidget(self.check_autostart)
        
        self.custom_sound_path = self.config.custom_sound_path
        
        # Custom sound UI
        sound_file_layout = QHBoxLayout()
        self.btn_select_sound = QPushButton(self.tr("&Select Custom Sound"))
        self.btn_select_sound.setAccessibleName(self.tr("Select Custom Audio Path Button"))
        self.btn_select_sound.clicked.connect(self.select_custom_sound)
        
        self.btn_clear_sound = QPushButton(self.tr("&Clear"))
        self.btn_clear_sound.setAccessibleName(self.tr("Reset Sound to Default Button"))
        self.btn_clear_sound.clicked.connect(self.clear_custom_sound)
        
        sound_file_layout.addWidget(QLabel(self.tr("Custom Sound:")))
        sound_file_layout.addWidget(self.btn_select_sound)
        sound_file_layout.addWidget(self.btn_clear_sound)
        layout.addLayout(sound_file_layout)
        
        self.lbl_sound_path = QLabel(self.custom_sound_path if self.custom_sound_path else self.tr("Default sound"))
        self.lbl_sound_path.setWordWrap(True)
        self.lbl_sound_path.setAccessibleName(self.tr("Current Audio Path Display"))
        layout.addWidget(self.lbl_sound_path)
        
        # Action Buttons
        btn_layout = QHBoxLayout()
        btn_test = QPushButton(self.tr("&Test Reminder"))
        btn_test.setAccessibleName(self.tr("Trigger a Hydration Test Reminder"))
        btn_test.clicked.connect(self.test_reminder)
        
        btn_save = QPushButton(self.tr("&Save"))
        btn_save.setAccessibleName(self.tr("Save Configuration settings"))
        btn_save.clicked.connect(self.save_settings)
        
        btn_layout.addWidget(btn_test)
        btn_layout.addWidget(btn_save)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
        # Configure tab indices
        self.setTabOrder(self.spin_interval, self.check_sound)
        self.setTabOrder(self.check_sound, self.check_autostart)
        self.setTabOrder(self.check_autostart, self.btn_select_sound)
        self.setTabOrder(self.btn_select_sound, self.btn_clear_sound)
        self.setTabOrder(self.btn_clear_sound, btn_test)
        self.setTabOrder(btn_test, btn_save)

    def select_custom_sound(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, self.tr("Select Audio File"), "", self.tr("Audio Files (*.ogg *.wav *.flac);;All Files (*)")
        )
        if file_path:
            logger.info(f"Custom audio selected: {file_path}")
            self.custom_sound_path = file_path
            self.lbl_sound_path.setText(self.custom_sound_path)

    def clear_custom_sound(self):
        logger.info("Custom sound path cleared.")
        self.custom_sound_path = ""
        self.lbl_sound_path.setText(self.tr("Default sound"))

    def save_settings(self):
        logger.info("Settings save initiated.")
        self.config.interval = self.spin_interval.value()
        self.config.sound = self.check_sound.isChecked()
        self.config.autostart = self.check_autostart.isChecked()
        self.config.custom_sound_path = self.custom_sound_path
        self.config.save()
        self.apply_callback()
        self.accept()

    def test_reminder(self):
        logger.info("Test reminder triggered from dialog UI.")
        self.parent_app.show_reminder()
