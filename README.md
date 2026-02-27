# HydrateMe

HydrateMe is a lightweight desktop application for Ubuntu that reminds you to drink water every 30 minutes. It runs in the system tray, shows notifications, and can play a custom sound until you acknowledge the reminder.

## Features
- System‑tray icon with menu
- Periodic desktop notifications (even on lock screen)
- Configurable reminder sound (default `paani.wav`)
- Single‑instance enforcement using file locks
- Snap package ready with a proper desktop entry

## Installation
```bash
# Build the snap
snapcraft pack
```

## Usage
Run `hydrateme` from the terminal or launch it from the applications menu. The app will stay in the background and remind you to stay hydrated.

## Development
```bash
# Install dependencies
pip install -r requirements.txt
# Run the app in development mode
python -m hydrateme
```

## License
MIT License
