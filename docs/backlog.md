# Backlog

## DONE
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
