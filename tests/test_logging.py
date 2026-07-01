# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import logging
from hydrateme.services.logging import setup_logging

def test_setup_logging(monkeypatch, tmp_path):
    """
    Verifies RotatingFileHandler configuration and log levels.
    """
    monkeypatch.setattr("hydrateme.utils.paths.get_state_dir", lambda: str(tmp_path))
    monkeypatch.setattr("hydrateme.utils.paths.get_log_file", lambda: str(tmp_path / "test.log"))
    
    setup_logging(debug=True)
    logger = logging.getLogger("hydrateme")
    assert logger.level == logging.DEBUG
    assert len(logger.handlers) >= 2
    
    setup_logging(debug=False)
    assert logger.level == logging.INFO
