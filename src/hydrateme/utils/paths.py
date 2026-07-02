# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import os
import sys
import getpass
import logging

logger = logging.getLogger("hydrateme")

def get_config_dir() -> str:
    """
    Returns the config directory following XDG specification.
    """
    xdg_config = os.environ.get("XDG_CONFIG_HOME")
    if xdg_config:
        path = os.path.join(xdg_config, "hydrateme")
    else:
        path = os.path.expanduser("~/.config/hydrateme")
    return os.path.abspath(path)

def get_config_file() -> str:
    """
    Returns the path to the config JSON file.
    """
    return os.path.join(get_config_dir(), "config.json")

def get_state_dir() -> str:
    """
    Returns the state/log directory following XDG specification.
    """
    xdg_state = os.environ.get("XDG_STATE_HOME")
    if xdg_state:
        path = os.path.join(xdg_state, "hydrateme")
    else:
        path = os.path.expanduser("~/.local/state/hydrateme")
    return os.path.abspath(path)

def get_log_file() -> str:
    """
    Returns the path to the main application log file.
    """
    return os.path.join(get_state_dir(), "hydrateme.log")

def get_crash_dir() -> str:
    """
    Returns the directory path for crash reports.
    """
    return os.path.join(get_state_dir(), "crash_reports")

def get_lock_file() -> str:
    """
    Returns a user-isolated lock file path to prevent multi-user collisions.
    """
    xdg_runtime = os.environ.get("XDG_RUNTIME_DIR")
    if xdg_runtime:
        path = os.path.join(xdg_runtime, "hydrateme.lock")
        try:
            if os.path.exists(xdg_runtime) and os.access(xdg_runtime, os.W_OK):
                return os.path.abspath(path)
        except Exception:
            pass
    # Fallback to user-specific /tmp file
    username = getpass.getuser()
    return os.path.abspath(f"/tmp/hydrateme-{username}.lock")

def get_asset_path(path: str) -> str:
    """
    Resolves the assets path, accounting for Snap environment mounts.
    """
    snap_dir = os.environ.get("SNAP")
    if snap_dir and path.startswith("/usr/"):
        return os.path.abspath(os.path.join(snap_dir, path.lstrip("/")))
    return os.path.abspath(path)

def validate_audio_file(file_path: str) -> bool:
    """
    Validates that the file exists, is readable, and is a safe audio format.
    """
    if not file_path:
        return False
    try:
        abs_path = os.path.abspath(file_path)
        if os.path.exists(abs_path) and os.path.isfile(abs_path) and os.access(abs_path, os.R_OK):
            ext = os.path.splitext(abs_path)[1].lower()
            if ext in [".wav", ".ogg", ".flac", ".mp3"]:
                return True
    except Exception as e:
        logger.warning(f"Audio file validation error: {e}")
    return False

def setup_autostart_desktop_file(enabled: bool):
    """
    Manages local user autostart desktop entries.
    Copies system-wide desktop launcher to ~/.config/autostart/hydrateme.desktop,
    modifying Exec to include the --autostart flag.
    If disabled is True, removes the file.
    """
    autostart_dir = os.path.expanduser("~/.config/autostart")
    autostart_file = os.path.join(autostart_dir, "hydrateme.desktop")
    
    if not enabled:
        if os.path.exists(autostart_file):
            try:
                os.remove(autostart_file)
                logger.info(f"Removed user autostart entry: {autostart_file}")
            except Exception as e:
                logger.error(f"Failed to remove autostart entry: {e}")
        return

    # Check if autostart directory exists, if not create it
    try:
        os.makedirs(autostart_dir, exist_ok=True)
    except Exception as e:
        logger.error(f"Failed to create autostart directory {autostart_dir}: {e}")
        return

    # Source desktop file paths
    # 1. System path
    src_desktop = get_asset_path("/usr/share/applications/hydrateme.desktop")
    # 2. Local workspace checkout path fallback (for dev/local tests)
    if not os.path.exists(src_desktop):
        local_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..", "usr", "share", "applications", "hydrateme.desktop")
        )
        if os.path.exists(local_path):
            src_desktop = local_path

    if not os.path.exists(src_desktop):
        logger.warning(f"Source desktop launcher not found at {src_desktop}. Cannot create autostart entry.")
        return

    try:
        # Read the source desktop entry
        with open(src_desktop, "r") as f:
            lines = f.readlines()

        # Modify the Exec line to include the --autostart CLI flag
        modified_lines = []
        for line in lines:
            if line.startswith("Exec="):
                exec_val = line.split("=", 1)[1].strip()
                # If --autostart is not already in exec, add it
                if "--autostart" not in exec_val:
                    line = f"Exec={exec_val} --autostart\n"
            modified_lines.append(line)

        # Write to local user autostart folder
        with open(autostart_file, "w") as f:
            f.writelines(modified_lines)
            
        # Ensure executable permissions
        os.chmod(autostart_file, 0o755)
        logger.info(f"Registered user autostart desktop entry at: {autostart_file}")
    except Exception as e:
        logger.error(f"Failed to copy and configure autostart entry: {e}")

def get_bundled_asset_path(relative_path: str) -> str:
    """
    Resolves asset path dynamically relative to this source file, which supports
    development, deb, snap and flatpak layouts cleanly.
    """
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "assets", relative_path.lstrip("/"))
    )

