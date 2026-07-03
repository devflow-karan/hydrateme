# Backlog

## TODO
- Task: Add feature to autostart the application on system restart (controlled via Settings UI).

## DONE
- Task: Resolve tray icon visibility in snap (via `unity7` plug), Settings Dialog button clipping, and correct About version display.
- Task: Integrate `gnome` desktop extension and configure build script to automatically remove old snap files.

- Task: Fix snap launch entry point failure by staging `usr/share/hydrateme/main.py`.

- Task: Add `scripts/build_snap.sh` to build snap locally with --push and --destructive flags, and update CI workflows to use direct snapcraft commands.
- Task: Migrate snap base from `core22` to `core24` so the snap runs natively on Ubuntu 24.04 without requiring manual `core22` installation.
- Task: Modernize application structure, add automated testing suite, implement structured logging, crash reporting, multi-DE backends, AppImage/Flatpak, and CI/CD pipelines.
- Task: Add custom audio configuration for hydration reminder.
- Task: Enforce single-instance application behavior using fcntl locking.
- Task: Reset hydration timer only after the user acknowledges the reminder.
- Task: Add feature to loop notification sound every 10 seconds while the reminder popup is active.
- Task: Resolve background system tray issue by adding IPC signals so the application menu launches the settings window.
- Task: Change the default application reminder sound to the newly provided `paani.wav` file.
- Task: Add desktop entry `usr/share/applications/hydrateme.desktop` for snap packaging.
- Task: Ensure Ubuntu 22.04 compatibility by downgrading snap base to core22.
- Task: Fix missing snap assets (logo and sound) by dynamically resolving paths with `$SNAP`.
- Task: Fix snap runner script path by dynamically referencing `$SNAP`.
- Task: Fix Python snap build failure by adding dependencies and system libraries.
- Task: Fix `metadata-generation-failed` by adding `libglib2.0-dev` to build-packages.
- Task: Improve `.deb` package distribution with a custom build script and clear installation instructions.
