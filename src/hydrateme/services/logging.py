# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import os
import sys
import logging
import logging.handlers
from hydrateme.utils import paths

def setup_logging(debug: bool = False):
    """
    Sets up application logging with RotatingFileHandler and Console output.
    """
    log_file = paths.get_log_file()
    state_dir = paths.get_state_dir()
    os.makedirs(state_dir, exist_ok=True)

    root_logger = logging.getLogger("hydrateme")
    root_logger.setLevel(logging.DEBUG if debug else logging.INFO)
    
    # Remove existing handlers to avoid duplicates
    for handler in list(root_logger.handlers):
        root_logger.removeHandler(handler)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s:%(filename)s:%(lineno)d] - %(message)s"
    )

    # 1. Rotating File Handler (max 5MB, keep 3 backups)
    try:
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=1024 * 1024 * 5, backupCount=3, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG if debug else logging.INFO)
        root_logger.addHandler(file_handler)
    except Exception as e:
        sys.stderr.write(f"Failed to configure file logging: {e}\n")

    # 2. Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    root_logger.addHandler(console_handler)

    root_logger.info("Logging system configured successfully.")
    if debug:
        root_logger.debug("Debug logs are enabled.")
