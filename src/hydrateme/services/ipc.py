# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import os
import sys
import fcntl
import signal
import socket
import logging
from PyQt6.QtCore import QSocketNotifier
from hydrateme.utils import paths

logger = logging.getLogger("hydrateme")

class IPCLock:
    """
    Enforces a single running instance per user using fcntl file locks.
    Supports Unix IPC signaling to raise active instance window.
    """
    def __init__(self):
        self.lock_fp = None
        self.sig_rsock = None
        self.sig_wsock = None
        self.sig_notifier = None

    def acquire(self) -> bool:
        """
        Attempts to acquire the exclusive file lock.
        Returns True if successful, False if already locked.
        """
        lock_file = paths.get_lock_file()
        try:
            lock_fd = os.open(lock_file, os.O_RDWR | os.O_CREAT, 0o600)
            self.lock_fp = os.fdopen(lock_fd, "r+")
            fcntl.lockf(self.lock_fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
            
            # Record PID
            self.lock_fp.truncate(0)
            self.lock_fp.seek(0)
            self.lock_fp.write(str(os.getpid()))
            self.lock_fp.flush()
            logger.info(f"Lock file acquired. Saved PID {os.getpid()} to {lock_file}")
            return True
        except (IOError, OSError) as e:
            logger.warning(f"Lock acquisition rejected. Another instance might be active: {e}")
            return False

    def notify_existing_instance(self) -> bool:
        """
        Sends SIGUSR1 to the PID recorded in the lock file.
        """
        lock_file = paths.get_lock_file()
        try:
            if not os.path.exists(lock_file):
                logger.warning(f"Lock file {lock_file} not found. Cannot notify.")
                return False
            with open(lock_file, "r") as f:
                pid_str = f.read().strip()
            if pid_str:
                pid = int(pid_str)
                logger.info(f"Sending SIGUSR1 to target PID: {pid}")
                os.kill(pid, signal.SIGUSR1)
                return True
        except ProcessLookupError:
            logger.warning("Target PID is not running. Stale lock file detected. Cleaning up.")
            try:
                if os.path.exists(lock_file):
                    os.remove(lock_file)
            except Exception:
                pass
        except Exception as e:
            logger.error(f"Failed to signal existing instance: {e}")
        return False

    def setup_ipc(self, open_settings_callback):
        """
        Sets up the socket pair and SIGUSR1 handler integrated with Qt.
        """
        try:
            self.sig_rsock, self.sig_wsock = socket.socketpair()
            self.sig_wsock.setblocking(False)
            self.sig_rsock.setblocking(False)

            def handle_sigusr1(signum, frame):
                try:
                    self.sig_wsock.send(b'x')
                except BlockingIOError:
                    pass

            signal.signal(signal.SIGUSR1, handle_sigusr1)

            # Route to Qt event loop via socket descriptor
            self.sig_notifier = QSocketNotifier(self.sig_rsock.fileno(), QSocketNotifier.Type.Read)
            
            def handle_qt_signal_read(fd):
                try:
                    self.sig_rsock.recv(1024)
                except BlockingIOError:
                    pass
                logger.info("Signal event notifier activated. Triggering callback.")
                open_settings_callback()

            self.sig_notifier.activated.connect(handle_qt_signal_read)
            logger.info("IPC Signal Notifiers configured.")
        except Exception as e:
            logger.error(f"Failed to configure IPC socket notification: {e}")

    def release(self):
        """
        Releases the lock file and closes file descriptors.
        """
        lock_file = paths.get_lock_file()
        if self.lock_fp:
            try:
                fcntl.lockf(self.lock_fp, fcntl.LOCK_UN)
                self.lock_fp.close()
                if os.path.exists(lock_file):
                    os.remove(lock_file)
                logger.info("Exclusive lock released successfully.")
            except Exception as e:
                logger.error(f"Error releasing lock file: {e}")
