# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import os
import sys
import pytest
import signal
from unittest.mock import MagicMock
from hydrateme.services.ipc import IPCLock
from hydrateme.utils import paths

def test_ipc_lock_acquire_release(clean_lock_file, monkeypatch):
    """
    Verifies lock acquisition and release life cycle.
    """
    lock = IPCLock()
    
    # First acquisition
    assert lock.acquire() is True
    assert os.path.exists(paths.get_lock_file())
    
    with open(paths.get_lock_file(), "r") as f:
        pid = int(f.read().strip())
    assert pid == os.getpid()
    
    # Simulate lock collision
    import fcntl
    def mock_lockf(fd, op):
        raise OSError("Resource temporarily unavailable")
    monkeypatch.setattr(fcntl, "lockf", mock_lockf)
    
    lock2 = IPCLock()
    assert lock2.acquire() is False
    
    # Restore original fcntl.lockf
    monkeypatch.undo()
    
    # Release
    lock.release()
    assert not os.path.exists(paths.get_lock_file())

def test_ipc_notify_instance(clean_lock_file, monkeypatch):
    """
    Verifies sending SIGUSR1 signal to the PID registered in the lock file.
    """
    mock_kill = MagicMock()
    monkeypatch.setattr("os.kill", mock_kill)
    
    lock = IPCLock()
    assert lock.acquire() is True
    
    lock2 = IPCLock()
    assert lock2.notify_existing_instance() is True
    
    mock_kill.assert_called_once_with(os.getpid(), signal.SIGUSR1)
    lock.release()
