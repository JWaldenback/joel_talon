"""Dedicated event log for mic on/off and external-dictation detection.

Appends one line per event to ``<talon root>/mic_state.log`` so out-of-sync
situations between Talon's mic, the mouse-sleep state, and external capture
services (Windows Dictation, Super Whisper, etc.) can be reconstructed
without scrubbing through the noisy main talon.log.

Best effort — failures here never propagate, so a missing/locked file can't
break the watcher loop.

Exposes a Talon action so callers in other folders can log via
``actions.user.mic_state_log("event", key="value", ...)``. Same-folder
callers can also import ``log`` directly.
"""

from datetime import datetime
from pathlib import Path
from threading import Lock

from talon import Module

# .../talon/user/joel_talon/plugin/mic_capture_watcher/mic_state_log.py
#   parents[4] == .../talon
_LOG_PATH = Path(__file__).resolve().parents[4] / "mic_state.log"
_lock = Lock()


def log(event: str, **fields):
    """Append one line to mic_state.log."""
    try:
        ts = datetime.now().isoformat(timespec="milliseconds")
        parts = [ts, event]
        for k, v in fields.items():
            parts.append(f"{k}={v!r}")
        line = " | ".join(parts) + "\n"
        with _lock, _LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass


mod = Module()


@mod.action_class
class Actions:
    def mic_state_log(event: str, fields: dict = None):
        """Append one line to mic_state.log for cross-module callers."""
        log(event, **(fields or {}))
