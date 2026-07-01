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
