#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import os
import sys

# Resolve execution context paths to support dev, deb, and snap environments
current_dir = os.path.dirname(os.path.abspath(__file__))

# Case 1: Package folder copied directly alongside this script (Debian layout)
if os.path.isdir(os.path.join(current_dir, "hydrateme")):
    sys.path.insert(0, current_dir)
else:
    # Case 2: Development workspace check (resolve src/ folder)
    # Move up 3 directories: hydrateme -> share -> usr -> project_root
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
    src_dir = os.path.join(project_root, "src")
    if os.path.isdir(src_dir):
        sys.path.insert(0, src_dir)

# Case 3: Snap packages will have installed the package directly into site-packages,
# so Python resolves it natively.

from hydrateme.__main__ import main

if __name__ == "__main__":
    main()
