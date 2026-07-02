# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import os
import subprocess
import logging

logger = logging.getLogger("hydrateme")

class ThemePalette:
    """
    Centralized color tokens for the modern application redesign.
    """
    # Base palette
    PRIMARY = "#2F80ED"
    ACCENT = "#4EA8FF"
    
    # Dark Mode Colors
    DARK_BACKGROUND = "#1E1E1E"
    DARK_SECONDARY_BG = "#252526"
    DARK_CARD = "#2D2D30"
    DARK_BORDER = "rgba(255, 255, 255, 0.08)"
    DARK_TEXT_PRIMARY = "#FFFFFF"
    DARK_TEXT_SECONDARY = "#C8C8C8"
    
    # Light Mode Colors
    LIGHT_BACKGROUND = "#F6F6F6"
    LIGHT_SECONDARY_BG = "#EFEFEF"
    LIGHT_CARD = "#FFFFFF"
    LIGHT_BORDER = "rgba(0, 0, 0, 0.08)"
    LIGHT_TEXT_PRIMARY = "#1E1E1E"
    LIGHT_TEXT_SECONDARY = "#555555"

    # Status Colors
    DANGER = "#E74C3C"
    SUCCESS = "#27AE60"
    WARNING = "#F2C94C"

def detect_system_dark_mode() -> bool:
    """
    Queries DBus / Portal settings or gsettings to detect system-wide dark theme preference.
    Falls back to Dark mode (True) on failure.
    """
    # 1. Try DBus Settings Portal (standard for modern GNOME/KDE and Flatpaks)
    try:
        import dbus
        bus = dbus.SessionBus()
        portal = bus.get_object("org.freedesktop.portal.Desktop", "/org/freedesktop/portal/desktop")
        settings = dbus.Interface(portal, "org.freedesktop.portal.Settings")
        # Returns 0: No Pref, 1: Dark, 2: Light
        scheme = settings.Read("org.freedesktop.appearance", "color-scheme")
        if int(scheme) == 1:
            logger.info("System dark mode detected via DBus Settings Portal.")
            return True
        elif int(scheme) == 2:
            logger.info("System light mode detected via DBus Settings Portal.")
            return False
    except Exception as e:
        logger.debug(f"DBus Portal Settings query skipped/failed: {e}")

    # 2. Try GSettings command fallback (standard GNOME Shell)
    try:
        res = subprocess.run(
            ["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"],
            capture_output=True, text=True, timeout=1
        )
        if res.returncode == 0:
            val = res.stdout.strip().strip("'")
            if "dark" in val.lower():
                logger.info("System dark mode detected via GSettings.")
                return True
            else:
                logger.info("System light mode detected via GSettings.")
                return False
    except Exception as e:
        logger.debug(f"GSettings query skipped/failed: {e}")

    # Fallback to Dark by default
    logger.info("Unable to detect system theme. Falling back to Dark mode.")
    return True

def get_theme_stylesheet(is_dark: bool) -> str:
    """
    Generates a global Qt stylesheet (QSS) based on the active color palette.
    """
    bg = ThemePalette.DARK_BACKGROUND if is_dark else ThemePalette.LIGHT_BACKGROUND
    sec_bg = ThemePalette.DARK_SECONDARY_BG if is_dark else ThemePalette.LIGHT_SECONDARY_BG
    card_bg = ThemePalette.DARK_CARD if is_dark else ThemePalette.LIGHT_CARD
    border = ThemePalette.DARK_BORDER if is_dark else ThemePalette.LIGHT_BORDER
    text_primary = ThemePalette.DARK_TEXT_PRIMARY if is_dark else ThemePalette.LIGHT_TEXT_PRIMARY
    text_secondary = ThemePalette.DARK_TEXT_SECONDARY if is_dark else ThemePalette.LIGHT_TEXT_SECONDARY
    
    primary = ThemePalette.PRIMARY
    accent = ThemePalette.ACCENT
    
    # Button colors
    btn_sec_bg = "rgba(255, 255, 255, 0.08)" if is_dark else "rgba(0, 0, 0, 0.05)"
    btn_sec_hover = "rgba(255, 255, 255, 0.15)" if is_dark else "rgba(0, 0, 0, 0.10)"
    btn_sec_pressed = "rgba(255, 255, 255, 0.20)" if is_dark else "rgba(0, 0, 0, 0.15)"
    
    return f"""
    QDialog {{
        background-color: {bg};
        color: {text_primary};
        font-family: 'Ubuntu', 'Noto Sans', sans-serif;
    }}
    
    QLabel {{
        color: {text_primary};
        font-size: 13px;
        border: none;
        background: transparent;
    }}
    
    QLabel#SectionTitle {{
        font-size: 16px;
        font-weight: bold;
        color: {text_primary};
        margin-bottom: 4px;
    }}
    
    QLabel#DescriptionLabel {{
        color: {text_secondary};
        font-size: 12px;
    }}
    
    QSpinBox {{
        background-color: {card_bg};
        color: {text_primary};
        border: 1px solid {border};
        border-radius: 6px;
        padding: 4px 8px;
        min-height: 24px;
    }}
    QSpinBox:focus {{
        border: 1px solid {primary};
    }}
    QSpinBox::up-button, QSpinBox::down-button {{
        width: 16px;
        border: none;
        background: transparent;
    }}
    
    QCheckBox {{
        color: {text_primary};
        spacing: 8px;
    }}
    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        border-radius: 4px;
        border: 1px solid {border};
        background-color: {card_bg};
    }}
    QCheckBox::indicator:checked {{
        background-color: {primary};
        border-color: {primary};
    }}
    
    /* Reusable Widget Styles */
    QFrame#CardWidget {{
        background-color: {card_bg};
        border: 1px solid {border};
        border-radius: 12px;
    }}
    
    QPushButton#PrimaryButton {{
        background-color: {primary};
        color: #FFFFFF;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-size: 13px;
        font-weight: bold;
    }}
    QPushButton#PrimaryButton:hover {{
        background-color: {accent};
    }}
    QPushButton#PrimaryButton:pressed {{
        background-color: #1E60B2;
    }}
    
    QPushButton#SecondaryButton {{
        background-color: {btn_sec_bg};
        color: {text_primary};
        border: 1px solid {border};
        border-radius: 6px;
        padding: 8px 16px;
        font-size: 13px;
    }}
    QPushButton#SecondaryButton:hover {{
        background-color: {btn_sec_hover};
    }}
    QPushButton#SecondaryButton:pressed {{
        background-color: {btn_sec_pressed};
    }}
    
    QPushButton#IconButton {{
        background-color: transparent;
        border: none;
        border-radius: 14px;
        padding: 4px;
        min-width: 28px;
        min-height: 28px;
    }}
    QPushButton#IconButton:hover {{
        background-color: {btn_sec_hover};
    }}
    QPushButton#IconButton:pressed {{
        background-color: {btn_sec_pressed};
    }}
    
    /* List / Sidebar styling */
    QListWidget {{
        background-color: {sec_bg};
        border: none;
        border-radius: 8px;
        padding: 4px;
    }}
    QListWidget::item {{
        color: {text_primary};
        padding: 8px 12px;
        border-radius: 6px;
    }}
    QListWidget::item:hover {{
        background-color: {btn_sec_hover};
    }}
    QListWidget::item:selected {{
        background-color: {primary};
        color: #FFFFFF;
    }}
    """
