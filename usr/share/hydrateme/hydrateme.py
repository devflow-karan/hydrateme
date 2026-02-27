#!/usr/bin/env python3
import sys
import json
import os
import subprocess
import dbus
import fcntl
import signal
from PyQt6.QtWidgets import (
    QApplication, QSystemTrayIcon, QMenu, QDialog, QVBoxLayout,
    QLabel, QPushButton, QHBoxLayout, QSpinBox, QCheckBox, QWidget,
    QFileDialog
)
from PyQt6.QtGui import QIcon, QFont, QAction
from PyQt6.QtCore import QTimer, Qt, QSocketNotifier


def get_asset_path(path):
    snap_dir = os.environ.get("SNAP")
    if snap_dir and path.startswith("/usr/"):
        # Strip leading slash to join correctly with snap_dir
        return os.path.join(snap_dir, path.lstrip("/"))
    return path

CONFIG_FILE = os.path.expanduser("~/.config/hydrateme.json")
# Default interval 30 minutes
DEFAULT_INTERVAL = 30
DEFAULT_SOUND = True

class Config:
    def __init__(self):
        self.interval = DEFAULT_INTERVAL
        self.sound = DEFAULT_SOUND
        self.custom_sound_path = ""
        self.load()

    def load(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    data = json.load(f)
                    self.interval = data.get("interval", DEFAULT_INTERVAL)
                    self.sound = data.get("sound", DEFAULT_SOUND)
                    self.custom_sound_path = data.get("custom_sound_path", "")
            except Exception as e:
                print("Error loading config:", e)

    def save(self):
        try:
            os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
            with open(CONFIG_FILE, "w") as f:
                json.dump({
                    "interval": self.interval,
                    "sound": self.sound,
                    "custom_sound_path": self.custom_sound_path
                }, f)
        except Exception as e:
            print("Error saving config:", e)

class SettingsDialog(QDialog):
    def __init__(self, config, apply_callback, parent_app):
        super().__init__()
        self.config = config
        self.apply_callback = apply_callback
        self.parent_app = parent_app
        self.setWindowTitle("HydrateMe Settings")
        
        layout = QVBoxLayout()
        
        # Interval setting
        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Reminder Interval (minutes):"))
        self.spin_interval = QSpinBox()
        self.spin_interval.setRange(1, 240)
        self.spin_interval.setValue(self.config.interval)
        hlayout.addWidget(self.spin_interval)
        layout.addLayout(hlayout)
        
        # Sound setting
        self.check_sound = QCheckBox("Play sound with reminder")
        self.check_sound.setChecked(self.config.sound)
        layout.addWidget(self.check_sound)
        
        self.custom_sound_path = self.config.custom_sound_path
        
        # Custom sound UI
        sound_file_layout = QHBoxLayout()
        self.btn_select_sound = QPushButton("Select Custom Sound")
        self.btn_select_sound.clicked.connect(self.select_custom_sound)
        self.btn_clear_sound = QPushButton("Clear")
        self.btn_clear_sound.clicked.connect(self.clear_custom_sound)
        
        sound_file_layout.addWidget(QLabel("Custom Sound:"))
        sound_file_layout.addWidget(self.btn_select_sound)
        sound_file_layout.addWidget(self.btn_clear_sound)
        layout.addLayout(sound_file_layout)
        
        self.lbl_sound_path = QLabel(self.custom_sound_path if self.custom_sound_path else "Default sound")
        self.lbl_sound_path.setWordWrap(True)
        layout.addWidget(self.lbl_sound_path)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_save = QPushButton("Save")
        btn_save.clicked.connect(self.save_settings)
        btn_test = QPushButton("Test Reminder")
        btn_test.clicked.connect(self.test_reminder)
        btn_layout.addWidget(btn_test)
        btn_layout.addWidget(btn_save)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def select_custom_sound(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Audio File", "", "Audio Files (*.ogg *.wav *.flac);;All Files (*)"
        )
        if file_path:
            self.custom_sound_path = file_path
            self.lbl_sound_path.setText(self.custom_sound_path)

    def clear_custom_sound(self):
        self.custom_sound_path = ""
        self.lbl_sound_path.setText("Default sound")

    def save_settings(self):
        self.config.interval = self.spin_interval.value()
        self.config.sound = self.check_sound.isChecked()
        self.config.custom_sound_path = self.custom_sound_path
        self.config.save()
        self.apply_callback()
        self.accept()

    def test_reminder(self):
        self.parent_app.show_reminder()

def is_screen_locked():
    try:
        bus = dbus.SessionBus()
        screensaver = bus.get_object('org.gnome.ScreenSaver', '/org/gnome/ScreenSaver')
        is_active = screensaver.GetActive(dbus_interface='org.gnome.ScreenSaver')
        return bool(is_active)
    except Exception as e:
        print("Could not get lock status, assuming unlocked.", e)
        return False

class ReminderPopup(QDialog):
    def __init__(self, parent_app):
        super().__init__()
        self.parent_app = parent_app
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setStyleSheet("background-color: #2b2b2b; color: #ffffff; border: 2px solid #3498db; border-radius: 10px;")
        
        layout = QVBoxLayout()
        label = QLabel("💧 Time to Drink Water! 💧")
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        label.setFont(font)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
        btn_done = QPushButton("I drank water")
        btn_done.setStyleSheet("background-color: #3498db; color: white; padding: 10px; border-radius: 5px; font-weight: bold; font-size: 16px;")
        btn_done.clicked.connect(self.on_done)
        layout.addWidget(btn_done)
        
        self.setLayout(layout)
        self.setFixedSize(400, 200)
        
        self.loop_timer = QTimer()
        self.loop_timer.timeout.connect(self.parent_app.trigger_sound)
        self.loop_timer.start(10000)

    def on_done(self):
        self.loop_timer.stop()
        self.accept()


class HydrateMeApp:
    def __init__(self, app):
        self.app = app
        self.config = Config()
        self.app.setQuitOnLastWindowClosed(False)
        self.settings_dialog = None
        
        # Get path to icon file
        self.icon_path = get_asset_path("/usr/share/icons/hicolor/scalable/apps/hydrateme.svg")
        if not os.path.exists(self.icon_path):
            self.icon_path = os.path.join(os.path.dirname(__file__), "hydrateme.svg") # local fallback
            
        icon = QIcon(self.icon_path) if os.path.exists(self.icon_path) else QIcon.fromTheme("video-display")
        
        self.tray = QSystemTrayIcon(icon, self.app)
        self.tray.setToolTip("HydrateMe")
        
        menu = QMenu()
        settings_action = QAction("Settings", self.app)
        settings_action.triggered.connect(self.open_settings)
        menu.addAction(settings_action)
        
        quit_action = QAction("Quit", self.app)
        quit_action.triggered.connect(self.quit_app)
        menu.addAction(quit_action)
        
        self.tray.setContextMenu(menu)
        self.tray.show()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_reminder)
        self.apply_timer()
        
        # Show settings window on startup to provide visual feedback
        # that the app is running (especially useful on Wayland/Ubuntu 24)
        QTimer.singleShot(100, self.show_initial_settings)

    def open_settings(self):
        if not self.settings_dialog:
            self.settings_dialog = SettingsDialog(self.config, self.apply_timer, self)
        self.settings_dialog.show()
        self.settings_dialog.activateWindow()
        self.settings_dialog.raise_()

    def show_initial_settings(self):
        self.open_settings()

    def apply_timer(self):
        self.timer.stop()
        self.timer.start(self.config.interval * 60 * 1000)

    def trigger_sound(self):
        if self.config.sound:
            sound_file = self.config.custom_sound_path if self.config.custom_sound_path else get_asset_path("/usr/share/sounds/paani.wav")
            subprocess.Popen(["paplay", sound_file])

    def show_reminder(self):
        # Stop timer to ensure full 30min begins only after clicking 'I drank water'
        self.timer.stop()
        if is_screen_locked():
            # Send notification
            subprocess.run(["notify-send", "-u", "critical", "-A", "drank=I Drank Water!", "HydrateMe", "Time to drink water!"])
            self.trigger_sound()
            # If screen locked, assuming notification either keeps them informed or they dismiss it.
            # Restart timer so background notifications continue
            self.apply_timer()
        else:
            self.trigger_sound()
            popup = ReminderPopup(self)
            popup.exec()
            # User clicked 'I drank water', restart the timer
            self.apply_timer()

    def quit_app(self):
        self.app.quit()

    def setup_signal_handler(self):
        # Create a socket pair to safely pass signals to Qt's event loop
        import socket
        self.sig_rsock, self.sig_wsock = socket.socketpair()
        self.sig_wsock.setblocking(False)
        self.sig_rsock.setblocking(False)
        
        # Tell Python to write to wsock when SIGUSR1 is received
        def handle_sigusr1(signum, frame):
            try:
                self.sig_wsock.send(b'x')
            except BlockingIOError:
                pass
        
        signal.signal(signal.SIGUSR1, handle_sigusr1)
        
        # Tell Qt to listen to rsock
        self.sig_notifier = QSocketNotifier(self.sig_rsock.fileno(), QSocketNotifier.Type.Read)
        self.sig_notifier.activated.connect(self.on_signal_received)

    def on_signal_received(self, fd):
        # Clear the socket
        try:
            self.sig_rsock.recv(1024)
        except BlockingIOError:
            pass
        # Pop the settings window!
        self.open_settings()


if __name__ == "__main__":
    lock_file = "/tmp/hydrateme.lock"
    import signal
    try:
        lock_fd = os.open(lock_file, os.O_RDWR | os.O_CREAT, 0o666)
        lock_fp = os.fdopen(lock_fd, "r+")
        fcntl.lockf(lock_fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
        # We got the lock, save our PID
        lock_fp.truncate(0)
        lock_fp.seek(0)
        lock_fp.write(str(os.getpid()))
        lock_fp.flush()
    except IOError:
        print("Another instance of HydrateMe is already running.")
        try:
            with open(lock_file, "r") as f:
                pid_str = f.read().strip()
            if pid_str:
                pid = int(pid_str)
                print(f"Sending SIGUSR1 to PID {pid} to open settings...")
                os.kill(pid, signal.SIGUSR1)
        except Exception as e:
            print("Failed to notify running instance:", e)
        sys.exit(0)
        
    os.environ["QT_QPA_PLATFORM"] = "xcb"
    app = QApplication(sys.argv)
    app.setApplicationName("HydrateMe")
    hydrate_me = HydrateMeApp(app)
    hydrate_me.setup_signal_handler()
    sys.exit(app.exec())
