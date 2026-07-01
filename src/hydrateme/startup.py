# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import os
import sys
import platform
import logging
import argparse
import shutil
from PyQt6.QtCore import QT_VERSION_STR

logger = logging.getLogger("hydrateme")

def run_diagnostics():
    """
    Prints system information and dependency states to logging targets.
    """
    logger.info("================ Startup Diagnostics ================")
    logger.info(f"Python Version: {sys.version}")
    logger.info(f"PyQt6 Qt Version: {QT_VERSION_STR}")
    logger.info(f"Platform: {platform.system()} {platform.release()} ({platform.version()})")
    
    desktop = os.environ.get("XDG_CURRENT_DESKTOP", "Unknown")
    session = os.environ.get("DESKTOP_SESSION", "Unknown")
    session_type = os.environ.get("XDG_SESSION_TYPE", "Unknown")
    logger.info(f"Desktop: {desktop} (Session: {session}, Type: {session_type})")
    
    logger.info(f"DISPLAY: {os.environ.get('DISPLAY', 'Not set')}")
    logger.info(f"WAYLAND_DISPLAY: {os.environ.get('WAYLAND_DISPLAY', 'Not set')}")
    
    has_paplay = shutil.which("paplay") is not None
    has_pwplay = shutil.which("pw-play") is not None
    has_aplay = shutil.which("aplay") is not None
    
    from hydrateme.services.sound import QT_MULTIMEDIA_AVAILABLE
    logger.info(f"Sound engines: paplay={has_paplay}, pw-play={has_pwplay}, aplay={has_aplay}, QtMultimedia={QT_MULTIMEDIA_AVAILABLE}")
    logger.info("=====================================================")

def parse_args() -> argparse.Namespace:
    """
    Parses CLI flags.
    """
    parser = argparse.ArgumentParser(description="HydrateMe - drink water reminder desktop application.")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging.")
    parser.add_argument("--verify", action="store_true", help="CI validation verify and exit.")
    parser.add_argument("--autostart", action="store_true", help="Indicates the app was started via system autostart.")
    return parser.parse_args()
