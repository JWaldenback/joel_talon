"""Pause Talon's input while Apple's built-in Dictation records on macOS."""

import time
from threading import RLock

from talon import Module, actions, app, cron, settings

from .dictation_session import DictationSession, InputPause
from .mac_audio import MacAudio
from .mac_dictation_shortcut import dictation_shortcut
from .mic_and_eye_tracker_state_log import log

mod = Module()
mod.setting(
    "mac_dictation_shortcut", type=str, default="",
    desc="Talon key sequence for Apple Dictation. Empty reads the configured macOS shortcut.",
)
# DictationIM can remain idle while corespeechd records on its behalf.
# Observe input activity for both services, not mere process presence.
mod.setting(
    "mac_dictation_bundle_ids", type=str,
    default="com.apple.inputmethod.ironwood,com.apple.CoreSpeech",
    desc="Comma-separated Core Audio bundle IDs for Apple speech recording used by Dictation.",
)

_pause = InputPause(
    lambda: actions.sound.active_microphone(),
    lambda name: actions.sound.set_microphone(name),
    lambda owner: actions.user.mouse_sleep(owner),
    lambda owner: actions.user.mouse_wake(owner),
)
_session = DictationSession(_pause)
_lock = RLock()
_audio = None
_job = None
_last_error = None
_suppress_until_inactive = False


def _recording():
    global _audio
    if _audio is None:
        _audio = MacAudio()
    bundles = {s.strip() for s in settings.get("user.mac_dictation_bundle_ids").split(",") if s.strip()}
    if not bundles:
        raise ValueError("user.mac_dictation_bundle_ids must identify Apple Dictation")
    return _audio.is_recording(bundles)


def _report_error(exc):
    global _last_error
    message = str(exc)
    if message != _last_error:
        _last_error = message
        print(f"[mac_dictation] {message}")
        app.notify("Apple Dictation monitoring unavailable", "Control-Option-Escape restores Talon input if needed.")


def _tick():
    global _last_error, _suppress_until_inactive, _job
    with _lock:
        # A manual launch needs monitoring even when automatic detection is
        # disabled, but must not leave an automatic watcher running afterward.
        if not settings.get("user.mic_capture_watch_enabled") and not _session.active:
            if _job is not None:
                cron.cancel(_job)
                _job = None
            return
        try:
            recording = _recording()
            _last_error = None
            if _suppress_until_inactive:
                if not recording:
                    _suppress_until_inactive = False
                return
            was_active = _session.active
            outcome = _session.observe(recording, time.monotonic())
            if not was_active and _session.active:
                log("dictation_detected", source="mac_dictation")
            if outcome:
                log(outcome, source="mac_dictation")
            if outcome == "start_failed":
                app.notify("Apple Dictation did not start", "Talon input restored. Check the Dictation shortcut and text field.")
        except Exception as exc:
            # Unknown is not 'stopped': do not unmute during a transient read
            # failure. The recovery hotkey also works while speech is muted.
            _report_error(exc)


def _ensure_polling():
    global _job
    if _job is None:
        _job = cron.interval("200ms", _tick)


def _apply_setting(*_args):
    global _job
    if app.platform != "mac":
        return
    with _lock:
        if settings.get("user.mic_capture_watch_enabled"):
            _ensure_polling()
        else:
            if _job is not None:
                cron.cancel(_job)
                _job = None
            _session.finish()


def _ready():
    if app.platform == "mac":
        settings.register("user.mic_capture_watch_enabled", _apply_setting)
        _apply_setting()


def _shutdown():
    global _job
    if app.platform != "mac":
        return
    with _lock:
        if _job is not None:
            cron.cancel(_job)
            _job = None
        _session.finish()
        _pause.release("mac_manual")


app.register("ready", _ready)
app.register("shutdown", _shutdown)


@mod.action_class
class Actions:
    def mac_dictation_toggle():
        """Start/stop Apple Dictation, pausing Talon until recording ends."""
        global _suppress_until_inactive
        if app.platform != "mac":
            raise RuntimeError("Apple Dictation requires macOS")
        with _lock:
            # A second press during launch cancels the pending handoff. Do
            # not send another start shortcut before recording is established.
            if _session.pending_until is not None:
                actions.key("escape")
                _session.finish()
                _suppress_until_inactive = True
                return
            # Validate both prerequisites before muting any input.
            keys = dictation_shortcut(settings.get("user.mac_dictation_shortcut"))
            recording = _recording()
            starting = not recording and not _session.active
            if starting:
                _suppress_until_inactive = False
                _session.start(time.monotonic())
            try:
                for index, key in enumerate(keys):
                    if index:
                        actions.sleep("50ms")
                    actions.key(key)
            except Exception:
                if starting:
                    _session.finish()
                raise
            _ensure_polling()
            log("dictation_shortcut", source="mac_dictation", starting=starting)

    def mac_dictation_resume():
        """Recover from a failed Dictation handoff using a physical shortcut."""
        global _suppress_until_inactive
        if app.platform != "mac":
            return
        with _lock:
            actions.key("escape")
            _session.finish()
            # An explicit recovery wins until the external recorder stops.
            # Preserve a separate manual pause, if the user requested one.
            _suppress_until_inactive = True
            log("dictation_recovery", source="mac_dictation")

    def mac_talon_pause_toggle():
        """End active Dictation or toggle Talon's manual input pause."""
        global _suppress_until_inactive
        with _lock:
            dictation_active = _session.active
            if not dictation_active:
                try:
                    dictation_active = _recording()
                except Exception:
                    # Keep the physical pedal useful if audio monitoring fails.
                    pass
            if dictation_active:
                # Escape stops Apple Dictation without risking a new start
                # through its Control-twice toggle shortcut.
                actions.key("escape")
                _session.finish()
                _pause.release("mac_manual")
                _suppress_until_inactive = True
                if not _pause.owners and actions.sound.active_microphone() in (None, "None"):
                    actions.sound.set_microphone("System Default")
                log("dictation_pedal_recovery", source="mac_dictation")
                return
            was_held = _pause.held("mac_manual")
            if was_held:
                _pause.release("mac_manual")
            # Talon can restart with its microphone already set to None.
            # A pedal press must still be able to turn voice input back on.
            if not _pause.owners and actions.sound.active_microphone() in (None, "None"):
                actions.sound.set_microphone("System Default")
            elif not was_held:
                _pause.acquire("mac_manual")

    def mac_talon_pause_held() -> bool:
        """Whether the user has manually paused Mac Talon input."""
        return _pause.held("mac_manual")
