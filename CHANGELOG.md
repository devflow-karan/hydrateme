# Changelog

## [1.5.3] - 2026-07-03
### Fixed
- Fixed tray icon visibility under strict Snap confinement by adding the `unity7` plug to the app definition.
- Fixed layout design issue causing Settings Dialog save/cancel buttons to clip by increasing default dialog size and adjusting sidebar spacing.
- Updated `APP_VERSION` in the crash service so the "About" dialog displays the correct current version.

## [1.5.2] - 2026-07-03
### Changed
- Integrated `gnome` extension in `snapcraft.yaml` to handle library setups, theme integrations, and font resolution natively.
- Modified local build script to clean up old `.snap` files automatically before starting a new build.

## [1.5.1] - 2026-07-03
### Fixed
- Fixed snap launch failure by packaging `usr/share/hydrateme/main.py` in the `desktop-entry` stage configuration.

## [1.5.0] - 2026-07-03
### Added
- `scripts/build_snap.sh`: new script to build the snap locally and optionally push to the Snap Store (`--push`) with LXD or host (`--destructive`) build modes.

### Changed
- Replaced deprecated `samuelmeuli/action-snapcraft@v2` in CI workflows with direct `snapcraft` commands (modern Canonical approach).
- Updated `release.yml` to use `SNAPCRAFT_STORE_CREDENTIALS` secret and `snapcraft upload --release=stable`.
- `build.yml` now uploads the built `.snap` as a downloadable GitHub Actions artifact.

## [1.4.1] - 2026-07-03
### Fixed
- Migrated snap base from `core22` to `core24` so the snap works natively on Ubuntu 24.04 (Noble) without requiring manual `core22` installation.
- Added `home` plug to snap app definition for proper XDG config/state directory access under `core24` strict confinement.
- Added `libgirepository1.0-dev` build package for improved GObject introspection compatibility on Noble.

## [1.4.0] - 2026-07-01
### Added
- Modular architecture with deep package segmentation (src/hydrateme/).
- Automated test coverage targeting 80%+ lines with pytest-qt and path isolations.
- Polymorphic desktop environment backends (GNOME, KDE, XFCE, Cinnamon, MATE, LXQt).
- Cascading audio pipeline (paplay -> pw-play -> aplay -> QSoundEffect).
- Reversed notification prioritize chain (Qt Tray -> DBus -> notify-send -> QMessageBox).
- XDG folder specifications compliance (config, state, logs).
- User-restricted runtime locks to support safe multi-user shared machines.
- Config schema migrations and diagnostic boot logging.
- Global crash reporters with user-safe PyQt recovery prompts.
- Github templates, License, Telemetry policies, and developer Contribution guidelines.
- Split CI/CD workflows (lint, tests, build, release) and smoke test verification.
- Flatpak and AppImage manifest specifications.

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
