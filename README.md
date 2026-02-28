# HydrateMe

HydrateMe is a lightweight desktop application for Ubuntu (22.04+) that reminds you to drink water every 30 minutes. It runs in the system tray, shows notifications, and can play a custom sound until you acknowledge the reminder.

## Features
- System‑tray icon with menu
- Periodic desktop notifications (even on lock screen)
- Configurable reminder sound (default `paani.wav`)
- Single‑instance enforcement using file locks
- Snap package ready with a proper desktop entry

## Installation

### From .deb Package (Recommended)
This is the easiest way to install HydrateMe on Ubuntu. Download the `.deb` file and install it using `apt` so that all dependencies are automatically resolved:

```bash
sudo apt update
sudo apt install ./hydrateme_1.3.5-1_all.deb
```

### From Snap
Building the snap ensures an isolated environment with all dependencies bundled:

```bash
# Build the snap locally
snapcraft pack
# Or build remotely if you don't have Lexus/Multipass
snapcraft remote-build
# Install the generated snap
sudo snap install --dangerous --classic hydrateme_*.snap
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
