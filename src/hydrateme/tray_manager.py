# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import os
import logging
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction
from hydrateme.utils.paths import get_asset_path
from hydrateme.utils.assets import create_fallback_icon

logger = logging.getLogger("hydrateme")

class TrayManager:
    """
    Manages the application's system tray presence, icon fallbacks, and context menu.
    """
    def __init__(self, app, open_settings_callback, quit_callback):
        self.app = app
        self.open_settings_callback = open_settings_callback
        self.quit_callback = quit_callback
        self.tray = None

    def initialize(self) -> bool:
        """
        Attempts to initialize the tray icon. Returns True if successful, False otherwise.
        """
        if not QSystemTrayIcon.isSystemTrayAvailable():
            logger.warning("QSystemTrayIcon is not supported in this desktop context.")
            return False

        logger.info("Initializing system tray icon...")
        icon = self.load_icon()
        
        self.tray = QSystemTrayIcon(icon, self.app)
        self.tray.setToolTip("HydrateMe")
        
        # Build context menu actions
        menu = QMenu()
        settings_action = QAction("Settings", self.app)
        settings_action.triggered.connect(self.open_settings_callback)
        menu.addAction(settings_action)
        
        quit_action = QAction("Quit", self.app)
        quit_action.triggered.connect(self.quit_callback)
        menu.addAction(quit_action)
        
        self.tray.setContextMenu(menu)
        self.tray.show()
        
        logger.info("System tray icon loaded and shown.")
        return True

    def load_icon(self) -> QIcon:
        """
        Resolves and loads the application icon following a strict fallback chain:
        1. System Theme
        2. Scalable SVG asset
        3. Standard size PNG fallbacks
        4. Dynamically generated QIcon
        """
        # Helper to check if icon actually has a valid graphic
        def is_valid_icon(ico: QIcon) -> bool:
            return not ico.isNull() and not ico.pixmap(24, 24).isNull()

        # 1. System Theme
        icon = QIcon.fromTheme("hydrateme")
        if is_valid_icon(icon):
            logger.info("Loaded icon from system theme indicator.")
            return icon
            
        # 2. Bundled SVG
        svg_path = get_asset_path("/usr/share/icons/hicolor/scalable/apps/hydrateme.svg")
        if os.path.exists(svg_path):
            icon = QIcon(svg_path)
            if is_valid_icon(icon):
                logger.info(f"Loaded icon from scalable SVG asset: {svg_path}")
                return icon
                
        # 3. Bundled PNG fallback
        png_sizes = ["48x48", "32x32", "64x64", "128x128", "256x256"]
        for size in png_sizes:
            png_path = get_asset_path(f"/usr/share/icons/hicolor/{size}/apps/hydrateme.png")
            if os.path.exists(png_path):
                icon = QIcon(png_path)
                if is_valid_icon(icon):
                    logger.info(f"Loaded icon from PNG asset size {size}: {png_path}")
                    return icon
                    
        # 4. Generate Fallback Icon dynamically
        logger.warning("All icon files missing or invalid. Building fallback icon.")
        return create_fallback_icon()

    def is_tray_available(self) -> bool:
        """
        Checks if system tray is active.
        """
        return self.tray is not None and self.tray.isVisible()

    def show_message(self, title: str, message: str):
        """
        Displays a notification bubble from the tray icon.
        """
        if self.tray:
            self.tray.showMessage(
                title,
                message,
                QSystemTrayIcon.MessageIcon.Information,
                10000
            )
