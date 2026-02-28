# Changelog

## [1.3.6] - 2026-02-28
### Fixed
- Fixed Qt xcb platform plugin failure in Snap by adding missing `libxcb-cursor0` and related XCB dependencies to `stage-packages`.

## [1.3.5] - 2026-02-28
### Fixed
- Fixed `metadata-generation-failed` error during snap build by adding `libglib2.0-dev` build dependency for `dbus-python`.
- Enhanced `.deb` package distribution by updating the `DEBIAN/control` dependencies and providing a new `scripts/build_deb.sh` build script.
- Updated `README.md` with recommended `apt` installation instructions to ensure all dependencies are automatically resolved.

## [1.3.0] - 2026-02-27
### Added
- Make the newly added `paani.wav` the default reminder audio instead of `message.oga`.

## [1.2.0] - 2026-02-27
### Added
- Added an audio looping mechanism that plays the notification sound every 10 seconds while the visual reminder is active.
- Re-launching the application now functions as a system tray workaround to open the Settings UI via `SIGUSR1` IPC signaling.

## [1.1.0] - 2026-02-27
### Added
- Feature to configure a custom audio .ogg or .wav file for the hydration reminder instead of repeating the default system message sound.
- Mechanism to reset the hydration timer only after the user confirms they drank water.

### Fixed
- Fixed issue where the application would allow multiple processes to run in the background concurrently. Added single-instance `fcntl` locks.
- Changed default application behavior to immediately show the Settings UI when launched via the application menu or CLI so it does not appear broken.

## [1.3.4] - 2026-02-27
### Fixed
- Fixed snap runner issue where `python3` could not find the main script by using `$SNAP` environment variable for path resolution.
- Fixed Python snap build failure by adding missing `dbus-python` dependency and necessary build/stage packages (`libdbus-1-dev`, `pkg-config`, Qt6 runtime libs).

## [1.3.3] - 2026-02-27
### Fixed
- Fixed missing logo and sound when running as a Snap by dynamically prepending `$SNAP` environment variable to asset paths.

## [1.3.2] - 2026-02-27
### Changed
- Downgraded snap base from `core24` to `core22` to ensure native compatibility with Ubuntu 22.04 LTS.

## [1.3.1] - 2026-02-27
### Added
- Added desktop entry file `usr/share/applications/hydrateme.desktop` for snap packaging.
