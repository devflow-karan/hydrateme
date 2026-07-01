# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import socket
import pytest
from unittest.mock import MagicMock
from hydrateme.services.ipc import IPCLock

def test_ipc_setup_and_trigger(clean_lock_file, qtbot):
    """
    Verifies that writing to the IPC socket triggers QSocketNotifier which invokes the settings callback.
    """
    lock = IPCLock()
    
    callback = MagicMock()
    lock.setup_ipc(callback)
    
    assert lock.sig_rsock is not None
    assert lock.sig_wsock is not None
    assert lock.sig_notifier is not None
    
    # Trigger write to write socket
    lock.sig_wsock.send(b'x')
    
    # Wait for notifier to wake up and invoke the callback
    qtbot.waitUntil(lambda: callback.called, timeout=1000)
    
    lock.release()
