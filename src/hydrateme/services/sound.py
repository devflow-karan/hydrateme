# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Karan Kumar

import subprocess
import os
import shutil
import logging
from hydrateme.utils.paths import get_asset_path, validate_audio_file

logger = logging.getLogger("hydrateme")

try:
    from PyQt6.QtMultimedia import QSoundEffect
    from PyQt6.QtCore import QUrl
    QT_MULTIMEDIA_AVAILABLE = True
except ImportError:
    QT_MULTIMEDIA_AVAILABLE = False

class SoundManager:
    """
    Handles audio reminder playback with a robust cascading fallback system:
    PulseAudio (paplay) -> PipeWire (pw-play) -> ALSA (aplay) -> PyQt6 (QSoundEffect).
    """
    def __init__(self, config):
        self.config = config
        self.process = None
        self._qt_effect = None

    def _get_sound_file(self) -> str:
        """
        Resolves path to the sound asset, prioritizing config paths then system paths.
        """
        sound_file = self.config.custom_sound_path
        if not sound_file or not validate_audio_file(sound_file):
            sound_file = get_asset_path("/usr/share/sounds/paani.wav")
            
        # Fallback to local asset check if not in system directories (development fallback)
        if not os.path.exists(sound_file):
            local_sound = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..", "..", "usr", "share", "sounds", "paani.wav")
            )
            if os.path.exists(local_sound):
                sound_file = local_sound
        return sound_file

    def play_reminder_sound(self):
        """
        Plays the hydration alert.
        """
        if not self.config.sound:
            logger.info("Sound disabled in settings. Skipping play.")
            return

        sound_file = self._get_sound_file()
        if not os.path.exists(sound_file):
            logger.error(f"Sound resource missing: {sound_file}")
            return

        logger.info(f"Triggering audio alert using file: {sound_file}")

        # 1. PulseAudio (paplay)
        if shutil.which("paplay"):
            try:
                logger.info("Invoking PulseAudio backend (paplay)")
                self.process = subprocess.Popen(
                    ["paplay", sound_file],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    shell=False
                )
                return
            except Exception as e:
                logger.warning(f"PulseAudio fallback failed: {e}")

        # 2. PipeWire (pw-play)
        if shutil.which("pw-play"):
            try:
                logger.info("Invoking PipeWire backend (pw-play)")
                self.process = subprocess.Popen(
                    ["pw-play", sound_file],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    shell=False
                )
                return
            except Exception as e:
                logger.warning(f"PipeWire fallback failed: {e}")

        # 3. ALSA Core (aplay)
        if shutil.which("aplay"):
            try:
                logger.info("Invoking ALSA backend (aplay)")
                self.process = subprocess.Popen(
                    ["aplay", "-q", sound_file],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    shell=False
                )
                return
            except Exception as e:
                logger.warning(f"ALSA fallback failed: {e}")

        # 4. Qt6 QSoundEffect fallback
        if QT_MULTIMEDIA_AVAILABLE:
            try:
                logger.info("Invoking native Qt6 Multimedia backend")
                self._qt_effect = QSoundEffect()
                self._qt_effect.setSource(QUrl.fromLocalFile(sound_file))
                self._qt_effect.setLoopCount(1)
                self._qt_effect.play()
                return
            except Exception as e:
                logger.warning(f"Qt6 QSoundEffect playback failed: {e}")
        else:
            logger.warning("Qt6 Multimedia is not available in current environment.")

        logger.error("All sound backend executions were unsuccessful.")

    def stop_sound(self):
        """
        Halts any running audio players.
        """
        if self.process and self.process.poll() is None:
            logger.info("Stopping shell audio backend subprocess.")
            try:
                self.process.terminate()
                self.process.wait(timeout=1)
            except Exception as e:
                logger.error(f"Error terminating audio process: {e}")
        self.process = None

        if QT_MULTIMEDIA_AVAILABLE and self._qt_effect and self._qt_effect.isPlaying():
            logger.info("Stopping native Qt QSoundEffect.")
            try:
                self._qt_effect.stop()
            except Exception as e:
                logger.error(f"Error stopping QSoundEffect execution: {e}")
        self._qt_effect = None
