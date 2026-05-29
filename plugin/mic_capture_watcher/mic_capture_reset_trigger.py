"""Out-of-Talon trigger for mic_capture_reset.

When the file %TEMP%\\mic_capture_reset.trigger appears, run
user.mic_capture_reset() and delete the trigger. Pair with
mic_capture_reset.bat to give yourself a clickable recovery path
when Talon's speech engine is stuck disabled and you can't issue
voice commands.

Polling runs on Talon's own cron, so it works regardless of whether
speech is enabled. The file is deleted BEFORE the reset is invoked,
so a hung reset can't cause an infinite loop.
"""

import tempfile
from pathlib import Path

from talon import Module, actions, app, cron

mod = Module()

_TRIGGER_PATH = Path(tempfile.gettempdir()) / "mic_capture_reset.trigger"
_state = {"cron": None}


def _check():
    if not _TRIGGER_PATH.exists():
        return
    # Delete first — if mic_capture_reset() hangs, we still won't loop.
    try:
        _TRIGGER_PATH.unlink()
    except Exception as e:
        print(f"[mic_capture_reset_trigger] failed to delete trigger: {e}")
        return
    print(f"[mic_capture_reset_trigger] trigger received, running reset")
    try:
        actions.user.mic_capture_reset()
    except Exception as e:
        print(f"[mic_capture_reset_trigger] reset failed: {e}")


def _on_ready():
    _state["cron"] = cron.interval("1s", _check)


app.register("ready", _on_ready)
