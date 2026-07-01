# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import os
import sys
import logging
from PyQt6.QtWidgets import QApplication
from hydrateme.startup import parse_args, run_diagnostics
from hydrateme.services.logging import setup_logging
from hydrateme.services.crash import setup_crash_reporter
from hydrateme.services.ipc import IPCLock
from hydrateme.application import HydrateMeApplication

logger = logging.getLogger("hydrateme")

def main():
    """
    Main entry point for executing the HydrateMe application.
    """
    args = parse_args()
    
    # Configure logs
    setup_logging(args.debug)
    
    # Setup exceptions hook
    setup_crash_reporter()
    
    # Diagnostics check
    run_diagnostics()
    
    # CI Dry run validation check
    if args.verify:
        logger.info("Verification dry-run success.")
        print("Dry-run verification success")
        sys.exit(0)

    # Check lock file
    lock = IPCLock()
    if not lock.acquire():
        # Signal running instance
        notified = lock.notify_existing_instance()
        if notified:
            logger.info("Running instance notified. Closing duplicate launch.")
        else:
            logger.warning("Lock acquisition rejected and running instance could not be contacted.")
        sys.exit(0)

    # Setup display platform variables for Wayland sessions
    if os.environ.get("XDG_SESSION_TYPE") == "wayland":
        if "QT_QPA_PLATFORM" not in os.environ:
            os.environ["QT_QPA_PLATFORM"] = "wayland;xcb"
            logger.info("Setting QT_QPA_PLATFORM='wayland;xcb' for Wayland desktop environment.")

    logger.info("Launching PyQt event loop...")
    qapp = QApplication(sys.argv)
    qapp.setApplicationName("HydrateMe")
    
    # Instantiate coordinator
    app_coordinator = HydrateMeApplication(qapp, args)
    
    # Bind UNIX sockets to QSocketNotifier
    lock.setup_ipc(app_coordinator.open_settings)
    
    # Start managers
    app_coordinator.start()
    
    try:
        sys.exit(qapp.exec())
    finally:
        # Release flock on exit
        lock.release()

if __name__ == "__main__":
    main()
