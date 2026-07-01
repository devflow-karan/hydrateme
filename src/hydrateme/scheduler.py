# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import logging
from PyQt6.QtCore import QTimer, QObject, pyqtSignal

logger = logging.getLogger("hydrateme")

class HydrationScheduler(QObject):
    """
    Manages the periodic hydration reminder timer loop using PyQt QTimer.
    Emits a timeout signal when the interval completes.
    """
    timeout = pyqtSignal()

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._on_timeout)

    def start(self):
        """
        Starts the countdown timer based on the current configuration.
        """
        interval_ms = self.config.interval * 60 * 1000
        logger.info(f"Starting scheduler timer: {self.config.interval} minutes ({interval_ms} ms)")
        self.timer.start(interval_ms)

    def stop(self):
        """
        Stops the scheduler timer.
        """
        logger.info("Stopping scheduler timer.")
        self.timer.stop()

    def apply(self):
        """
        Applies configuration changes by resetting the active timer.
        """
        self.stop()
        self.start()

    def _on_timeout(self):
        logger.info("Scheduler interval completed.")
        self.timeout.emit()
