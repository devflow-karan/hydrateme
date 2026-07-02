# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import os
import logging
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QPushButton, QFileDialog,
    QListWidget, QStackedWidget, QWidget, QComboBox
)
from PyQt6.QtCore import Qt, QSize
from hydrateme.utils.assets import get_themed_icon
from hydrateme.ui.widgets.toggle_switch import ToggleSwitch
from hydrateme.ui.widgets.card import CardWidget
from hydrateme.ui.widgets.buttons import PrimaryButton, SecondaryButton
from hydrateme.ui.theme import get_theme_stylesheet, detect_system_dark_mode
from hydrateme.ui.about import AboutWidget

logger = logging.getLogger("hydrateme")

class SettingsDialog(QDialog):
    """
    Redesigned settings dialog with a modern left sidebar (selections) and
    stacked right panels using card containers, toggle switches, and themed icons.
    """
    def __init__(self, config, apply_callback, parent_app):
        super().__init__()
        self.config = config
        self.apply_callback = apply_callback
        self.parent_app = parent_app
        
        self.setWindowTitle(self.tr("HydrateMe Settings"))
        self.resize(650, 480)
        self.setMinimumSize(600, 420)
        
        # Apply theme stylesheet dynamically
        is_dark = detect_system_dark_mode() if self.config.theme == "auto" else (self.config.theme == "dark")
        self.setStyleSheet(get_theme_stylesheet(is_dark))
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)
        
        # Body containing sidebar list and stacked panels
        body_layout = QHBoxLayout()
        body_layout.setSpacing(16)
        
        # Left Sidebar (QListWidget)
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(180)
        self.sidebar.setIconSize(QSize(18, 18))
        self.sidebar.currentRowChanged.connect(self.switch_tab)
        
        # Right Stacked Panels
        self.stacked_panels = QStackedWidget()
        
        body_layout.addWidget(self.sidebar)
        body_layout.addWidget(self.stacked_panels)
        main_layout.addLayout(body_layout)
        
        # Add Sheets
        self.setup_general_sheet()
        self.setup_sound_sheet()
        self.setup_notifications_sheet()
        self.setup_advanced_sheet()
        self.setup_about_sheet()
        
        # Set default tab select
        self.sidebar.setCurrentRow(0)
        
        # Bottom Action Bar
        action_layout = QHBoxLayout()
        self.btn_save = PrimaryButton(self.tr("&Save"))
        self.btn_save.clicked.connect(self.save_settings)
        self.btn_cancel = SecondaryButton(self.tr("&Cancel"))
        self.btn_cancel.clicked.connect(self.reject)
        
        action_layout.addWidget(self.btn_save)
        action_layout.addStretch()
        action_layout.addWidget(self.btn_cancel)
        main_layout.addLayout(action_layout)

    def switch_tab(self, row: int):
        self.stacked_panels.setCurrentIndex(row)

    def setup_general_sheet(self):
        # 1. General Panel
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        
        lbl_title = QLabel(self.tr("General Settings"))
        lbl_title.setObjectName("SectionTitle")
        layout.addWidget(lbl_title)
        
        card = CardWidget()
        
        # Reminder Interval
        lbl_interval = QLabel(self.tr("<b>Reminder Interval</b><br>How often the app alerts you to drink water"))
        lbl_interval.setObjectName("DescriptionLabel")
        self.spin_interval = QSpinBox()
        self.spin_interval.setRange(1, 240)
        self.spin_interval.setValue(self.config.interval)
        self.spin_interval.setFixedWidth(80)
        card.add_row(lbl_interval, self.spin_interval)
        
        # Launch on startup
        lbl_autostart = QLabel(self.tr("<b>Launch on Startup</b><br>Automatically start the app at session login"))
        lbl_autostart.setObjectName("DescriptionLabel")
        self.switch_autostart = ToggleSwitch()
        self.switch_autostart.setChecked(self.config.autostart)
        self.check_autostart = self.switch_autostart
        card.add_row(lbl_autostart, self.switch_autostart)
        
        # Theme dropdown
        lbl_theme = QLabel(self.tr("<b>Application Theme</b><br>Choose color appearance style preference"))
        lbl_theme.setObjectName("DescriptionLabel")
        self.combo_theme = QComboBox()
        self.combo_theme.addItems([self.tr("Auto (System)"), self.tr("Dark Theme"), self.tr("Light Theme")])
        self.combo_theme.setFixedWidth(140)
        if self.config.theme == "auto":
            self.combo_theme.setCurrentIndex(0)
        elif self.config.theme == "dark":
            self.combo_theme.setCurrentIndex(1)
        else:
            self.combo_theme.setCurrentIndex(2)
        card.add_row(lbl_theme, self.combo_theme)
        
        layout.addWidget(card)
        layout.addStretch()
        
        self.stacked_panels.addWidget(widget)
        self.sidebar.addItem(self.tr("General"))
        self.sidebar.item(self.sidebar.count() - 1).setIcon(get_themed_icon("settings"))

    def setup_sound_sheet(self):
        # 2. Sound Panel
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        
        lbl_title = QLabel(self.tr("Sound Configuration"))
        lbl_title.setObjectName("SectionTitle")
        layout.addWidget(lbl_title)
        
        card = CardWidget()
        
        # Play alert sound toggle
        lbl_sound = QLabel(self.tr("<b>Play alert sound</b><br>Triggers hydration reminder audio clip loops"))
        lbl_sound.setObjectName("DescriptionLabel")
        self.switch_sound = ToggleSwitch()
        self.switch_sound.setChecked(self.config.sound)
        self.check_sound = self.switch_sound
        card.add_row(lbl_sound, self.switch_sound)
        
        # Sound file picker
        self.custom_sound_path = self.config.custom_sound_path
        lbl_file = QLabel(self.tr("<b>Custom Reminder Audio File</b><br>Path: ") + 
                           (self.custom_sound_path if self.custom_sound_path else self.tr("Default")))
        lbl_file.setObjectName("DescriptionLabel")
        lbl_file.setWordWrap(True)
        
        btn_select = SecondaryButton(self.tr("Select"))
        btn_select.clicked.connect(self.select_custom_sound)
        
        card.add_row(lbl_file, btn_select)
        
        # Test Reminder Button
        lbl_test = QLabel(self.tr("<b>Verify Settings</b><br>Test playback configurations visually and audibly"))
        lbl_test.setObjectName("DescriptionLabel")
        btn_test = SecondaryButton(self.tr("Test Alert"))
        btn_test.clicked.connect(self.test_reminder)
        card.add_row(lbl_test, btn_test)
        
        layout.addWidget(card)
        layout.addStretch()
        
        self.stacked_panels.addWidget(widget)
        self.sidebar.addItem(self.tr("Sound"))
        self.sidebar.item(self.sidebar.count() - 1).setIcon(get_themed_icon("sound"))
        
        self.lbl_sound_path = lbl_file  # hold reference to update label text

    def setup_notifications_sheet(self):
        # 3. Notifications Panel
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        
        lbl_title = QLabel(self.tr("Notifications Settings"))
        lbl_title.setObjectName("SectionTitle")
        layout.addWidget(lbl_title)
        
        card = CardWidget()
        
        lbl_notif_status = QLabel(self.tr("<b>Native Desktop Alerts</b><br>Integrates with desktop notifications portal"))
        lbl_notif_status.setObjectName("DescriptionLabel")
        lbl_val = QLabel(self.tr("Enabled"))
        lbl_val.setStyleSheet("font-weight: bold; color: #27AE60;")
        card.add_row(lbl_notif_status, lbl_val)
        
        lbl_lock = QLabel(self.tr("<b>Lock Screen Behavior</b><br>Falls back to notifications if session screen is locked"))
        lbl_lock.setObjectName("DescriptionLabel")
        lbl_val_lock = QLabel(self.tr("Active"))
        lbl_val_lock.setStyleSheet("font-weight: bold; color: #2F80ED;")
        card.add_row(lbl_lock, lbl_val_lock)
        
        layout.addWidget(card)
        layout.addStretch()
        
        self.stacked_panels.addWidget(widget)
        self.sidebar.addItem(self.tr("Notifications"))
        self.sidebar.item(self.sidebar.count() - 1).setIcon(get_themed_icon("bell"))

    def setup_advanced_sheet(self):
        # 4. Advanced Panel
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        
        lbl_title = QLabel(self.tr("Advanced Settings"))
        lbl_title.setObjectName("SectionTitle")
        layout.addWidget(lbl_title)
        
        card = CardWidget()
        
        lbl_session = QLabel(self.tr("<b>XDG Windowing Backend</b><br>Detects and optimizes for Wayland or X11"))
        lbl_session.setObjectName("DescriptionLabel")
        
        sess_type = os.environ.get("XDG_SESSION_TYPE", "X11/unknown").upper()
        lbl_val = QLabel(sess_type)
        lbl_val.setStyleSheet("font-weight: bold;")
        card.add_row(lbl_session, lbl_val)
        
        lbl_dbus = QLabel(self.tr("<b>D-Bus Integration</b><br>Binds lock screen and notification handlers"))
        lbl_dbus.setObjectName("DescriptionLabel")
        lbl_dbus_val = QLabel(self.tr("Running"))
        lbl_dbus_val.setStyleSheet("font-weight: bold; color: #27AE60;")
        card.add_row(lbl_dbus, lbl_dbus_val)
        
        layout.addWidget(card)
        layout.addStretch()
        
        self.stacked_panels.addWidget(widget)
        self.sidebar.addItem(self.tr("Advanced"))
        self.sidebar.item(self.sidebar.count() - 1).setIcon(get_themed_icon("timer"))

    def setup_about_sheet(self):
        # 5. About Panel
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        
        lbl_title = QLabel(self.tr("About Application"))
        lbl_title.setObjectName("SectionTitle")
        layout.addWidget(lbl_title)
        
        # Embed AboutWidget directly
        about_content = AboutWidget(show_close_button=False, parent=widget)
        layout.addWidget(about_content)
        layout.addStretch()
        
        self.stacked_panels.addWidget(widget)
        self.sidebar.addItem(self.tr("About"))
        self.sidebar.item(self.sidebar.count() - 1).setIcon(get_themed_icon("about"))

    def select_custom_sound(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, self.tr("Select Audio File"), "", self.tr("Audio Files (*.ogg *.wav *.flac);;All Files (*)")
        )
        if file_path:
            logger.info(f"Custom audio selected: {file_path}")
            self.custom_sound_path = file_path
            self.lbl_sound_path.setText(self.tr("<b>Custom Reminder Audio File</b><br>Path: ") + self.custom_sound_path)

    def test_reminder(self):
        logger.info("Test reminder triggered from SettingsDialog.")
        self.parent_app.show_reminder()

    def save_settings(self):
        logger.info("Settings save initiated.")
        self.config.interval = self.spin_interval.value()
        self.config.sound = self.switch_sound.isChecked()
        self.config.autostart = self.switch_autostart.isChecked()
        self.config.custom_sound_path = self.custom_sound_path
        
        theme_index = self.combo_theme.currentIndex()
        if theme_index == 0:
            self.config.theme = "auto"
        elif theme_index == 1:
            self.config.theme = "dark"
        else:
            self.config.theme = "light"
            
        self.config.save()
        
        # Apply updated theme stylesheet globally
        is_dark = detect_system_dark_mode() if self.config.theme == "auto" else (self.config.theme == "dark")
        self.parent_app.qapp.setStyleSheet(get_theme_stylesheet(is_dark))
        
        self.apply_callback()
        self.accept()
