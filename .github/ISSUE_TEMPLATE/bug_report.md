name: 🐛 Bug Report
description: Report a bug or unexpected behavior in HydrateMe
title: "[BUG] "
labels: ["bug"]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        Thank you for reporting this issue! Please provide as much detail as possible to help us reproduce and fix it.
  - type: textarea
    id: description
    attributes:
      label: Description of the Bug
      description: Provide a clear and concise description of what the bug is.
      placeholder: E.g., The system tray icon is blank when launching on Ubuntu 22.04.
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: Explain the steps to reproduce this behavior.
      placeholder: |
        1. Run 'hydrateme'
        2. Wait for 30 minutes
        3. Observe the crash...
    validations:
      required: true
  - type: textarea
    id: environment
    attributes:
      label: System Diagnostics
      description: Please share your environment details.
      value: |
        - OS Version: Ubuntu 24.04 / 22.04
        - Desktop Environment: GNOME / KDE Plasma / Xfce
        - Display Server: Wayland / X11
        - Application Version: v1.4.0
        - Python/Qt Version: Python 3.12.3 / PyQt6 6.6.1
    validations:
      required: true
  - type: textarea
    id: logs
    attributes:
      label: Application logs or Stack Trace
      description: Paste any logs from ~/.local/state/hydrateme/logs/ or crash logs.
      placeholder: Paste tracebacks here...
