# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import os
import sys
import datetime
import traceback
import platform
import logging
import threading
import subprocess
from PyQt6.QtWidgets import QMessageBox, QApplication
from hydrateme.utils import paths

logger = logging.getLogger("hydrateme")

APP_VERSION = "1.4.0"

def get_packaging_type() -> str:
    """
    Determines the packaging format the application is running under.
    """
    if os.environ.get("SNAP"):
        return "snap"
    elif os.environ.get("FLATPAK_ID"):
        return "flatpak"
    elif os.environ.get("APPIMAGE"):
        return "AppImage"
    elif os.path.exists("/usr/share/hydrateme/hydrateme.py") or os.path.exists("/usr/share/applications/hydrateme.desktop"):
        return "deb"
    else:
        return "local/source"

def get_git_commit() -> str:
    """
    Attempts to retrieve the current git commit hash.
    """
    try:
        res = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, timeout=1)
        if res.returncode == 0:
            return res.stdout.strip()
    except Exception:
        pass
    return "unknown"

def write_crash_report(exctype, value, tb) -> str:
    """
    Generates a log file containing system environment diagnostics and stack traces.
    """
    crash_dir = paths.get_crash_dir()
    os.makedirs(crash_dir, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    report_file = os.path.join(crash_dir, f"crash-{timestamp}.log")
    
    config_str = "Unknown configuration state"
    try:
        config_file = paths.get_config_file()
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                config_str = f.read().strip()
    except Exception as e:
        config_str = f"Error reading config: {e}"
        
    os_info = f"{platform.system()} {platform.release()} ({platform.version()})"
    python_info = sys.version
    desktop = os.environ.get("XDG_CURRENT_DESKTOP", "Unknown")
    desktop_session = os.environ.get("DESKTOP_SESSION", "Unknown")
    
    tb_lines = traceback.format_exception(exctype, value, tb)
    tb_str = "".join(tb_lines)
    
    env_vars = {
        "PATH": os.environ.get("PATH", ""),
        "DISPLAY": os.environ.get("DISPLAY", ""),
        "WAYLAND_DISPLAY": os.environ.get("WAYLAND_DISPLAY", ""),
        "XAUTHORITY": os.environ.get("XAUTHORITY", ""),
        "QT_QPA_PLATFORM": os.environ.get("QT_QPA_PLATFORM", "")
    }
    env_str = "\n".join([f"  {k}={v}" for k, v in env_vars.items()])
    
    content = f"""HydrateMe Crash Report
======================
Timestamp: {datetime.datetime.now().isoformat()}
Application Version: {APP_VERSION}
Python Version: {python_info}
OS Version: {os_info}
Desktop Environment: {desktop} (Session: {desktop_session})
Packaging Type: {get_packaging_type()}
Git Commit: {get_git_commit()}

Environment Variables:
{env_str}

Configuration File Contents:
{config_str}

Stack Trace:
{tb_str}
"""
    try:
        with open(report_file, "w") as f:
            f.write(content)
        logger.critical(f"Crash report written to: {report_file}")
    except Exception as e:
        logger.error(f"Failed to write crash report file: {e}")
        
    return report_file

def show_crash_dialog(report_file: str):
    """
    Shows a PyQt dialog asking the user whether to restart the application.
    """
    app = QApplication.instance()
    if not app:
        app = QApplication([])
        
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Critical)
    msg_box.setWindowTitle("HydrateMe - Unexpected Error")
    msg_box.setText("HydrateMe encountered an unexpected error.")
    msg_box.setInformativeText(
        f"A crash report has been saved to:\n{report_file}\n\nWould you like to restart the application?"
    )
    msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    msg_box.setDefaultButton(QMessageBox.StandardButton.Yes)
    
    ret = msg_box.exec()
    if ret == QMessageBox.StandardButton.Yes:
        logger.info("Restarting application...")
        try:
            subprocess.Popen([sys.executable] + sys.argv)
        except Exception as e:
            logger.error(f"Failed to restart application: {e}")
        sys.exit(1)
    else:
        sys.exit(1)

def exception_handler(exctype, value, tb):
    """
    Invoked upon uncaught exceptions.
    """
    if issubclass(exctype, SystemExit):
        sys.__excepthook__(exctype, value, tb)
        return
        
    try:
        logger.critical("Uncaught Exception occurred!", exc_info=(exctype, value, tb))
        report_file = write_crash_report(exctype, value, tb)
        show_crash_dialog(report_file)
    except Exception as e:
        sys.stderr.write(f"Error in exception handler: {e}\n")
        traceback.print_exception(exctype, value, tb, file=sys.stderr)
        sys.exit(1)

def setup_crash_reporter():
    """
    Registers exception hooks.
    """
    sys.excepthook = exception_handler
    
    def thread_exception_handler(args):
        exception_handler(args.exc_type, args.exc_value, args.exc_traceback)
        
    threading.excepthook = thread_exception_handler
    logger.info("Crash hooks set up successfully.")
