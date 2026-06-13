"""Watch the microphone for known capture services and auto-pause Talon.

Polls Windows Core Audio for active capture sessions. When any registered
service (e.g. Windows Dictation, Super Whisper) starts listening, Talon's
speech engine is disabled and the mouse is slept (so head/eye tracking
doesn't move the cursor). State is restored when all services go inactive.

To watch a new service, add an entry to CAPTURE_SERVICES below. The only
required keys are `name`, `display`, and `processes` (lowercase exe names).
"""

from talon import Module, actions, app, cron, scope, settings

from .mic_and_eye_tracker_state_log import log as _state_log

mod = Module()


CAPTURE_SERVICES = [
    {
        "name": "win_h_dictation",
        "display": "Windows Dictation",
        # Win11 voice typing runs in-process inside TextInputHost.exe.
        # SpeechRuntime.exe is a fallback for older/alternate builds.
        "processes": {"textinputhost.exe", "speechruntime.exe"},
        # Clear the "armed keystroke resume" flag from voice_dictation_resume
        # when the pill closes, regardless of who closed it.
        "on_deactivate": lambda: actions.user.voice_dictation_disarm_keypress_resume(),
    },
    {
        "name": "super_whisper",
        "display": "Super Whisper",
        "processes": {"superwhisper.exe"},
    },
]


mod.setting(
    "mic_capture_watch_enabled",
    type=bool,
    default=True,
    desc="When True, watch the microphone for known capture services and auto-pause Talon speech + mouse while any of them is listening.",
)

mod.setting(
    "mic_capture_poll_ms",
    type=int,
    default=300,
    desc="Polling interval in ms for mic capture session detection.",
)


def _import_monitor():
    """Lazy import so a missing comtypes dep doesn't crash module load."""
    try:
        from . import audio_session_monitor
        return audio_session_monitor, None
    except ImportError as e:
        return None, e


def _services_active() -> set[str]:
    """Names of services that currently have an active capture session."""
    monitor, err = _import_monitor()
    if monitor is None:
        print(
            f"[mic_capture_watcher] comtypes missing: {err}. "
            "Run plugin/mic_capture_watcher/install_deps.bat."
        )
        return set()
    try:
        sessions = monitor.list_active_capture_sessions()
    except Exception as e:
        print(f"[mic_capture_watcher] capture check failed: {e}")
        return set()
    ACTIVE = 1
    active_procs = {
        name.lower() for _pid, name, state in sessions if state == ACTIVE and name
    }
    return {
        s["name"] for s in CAPTURE_SERVICES if s["processes"] & active_procs
    }


# Per-service state. `disabled_by_us` indicates that this service was the
# one that triggered the current global pause (so the matching restore is
# owed to it). External modules can set it via `mark_disabled_by_us(name)`.
_service_state: dict[str, dict] = {
    s["name"]: {"active": False, "disabled_by_us": False} for s in CAPTURE_SERVICES
}

_global = {
    "speech_disabled_by_us": False,
    "previous_microphone": None,
    "mouse_slept_by_us": False,
    "cron": None,
    # Last mic name seen by the polling tick — used to log changes whose
    # cause isn't this module (HUD click, voice command, etc.).
    "last_polled_mic": None,
    # Last (control, control_zoom, control1) eye-tracker tuple seen by the
    # polling tick. Logged when it changes so out-of-sync states (tracker
    # left on while watcher thinks Talon is paused, or vice versa) are
    # captured even when the change came from outside mouse_sleep/wake.
    "last_polled_tracking": None,
}


def _service_by_name(name: str):
    return next((s for s in CAPTURE_SERVICES if s["name"] == name), None)


def _any_service_active() -> bool:
    return any(s["active"] for s in _service_state.values())


def _activate(name: str):
    service = _service_by_name(name)
    if service is None:
        return
    was_any_active = _any_service_active()
    _service_state[name]["active"] = True
    # Only take global pause actions on the first service to go active.
    # If Talon is already sleeping, don't touch speech or the mouse —
    # speech.enable() on resume would wake Talon, and stacking a sleep
    # would entangle our restore with the user's "talon wake".
    # Likewise, if toggle_talon_sleep (numpad-divide pause) already
    # holds the tracker pause, don't redundantly mute/sleep again — Talon
    # is already paused by that toggle. (The tracker stack is keyed by owner
    # token now, so a second sleep wouldn't corrupt it; this just avoids
    # double mic muting and a confusing second restore.)
    was_sleeping = "sleep" in scope.get("mode") if not was_any_active else None
    toggle_holds_pause = False
    if not was_any_active:
        try:
            toggle_holds_pause = actions.user.toggle_talon_sleep_holds_tracker_pause()
        except Exception:
            pass
    saved_mic = None
    if not was_any_active:
        try:
            if not was_sleeping and not toggle_holds_pause:
                current_mic = actions.sound.active_microphone()
                if current_mic and current_mic != "None":
                    _global["previous_microphone"] = current_mic
                    saved_mic = current_mic
                    actions.speech.set_microphone("None")
                    _global["speech_disabled_by_us"] = True
                    _service_state[name]["disabled_by_us"] = True
        except Exception as e:
            print(f"[mic_capture_watcher] disable failed: {e}")
        if not was_sleeping and not toggle_holds_pause:
            try:
                actions.user.mouse_sleep("watcher")
                _global["mouse_slept_by_us"] = True
            except Exception as e:
                print(f"[mic_capture_watcher] mouse_sleep failed: {e}")
    _state_log(
        "dictation_detected",
        source="mic_capture_watcher",
        service=name,
        first_active=not was_any_active,
        was_sleeping=was_sleeping,
        toggle_holds_pause=toggle_holds_pause,
        saved_mic=saved_mic,
    )
    app.notify(f"Talon paused: {service['display']} active")


def _deactivate(name: str):
    service = _service_by_name(name)
    _service_state[name]["active"] = False
    _service_state[name]["disabled_by_us"] = False
    if service is not None:
        hook = service.get("on_deactivate")
        if hook is not None:
            try:
                hook()
            except Exception as e:
                print(f"[mic_capture_watcher] {name} on_deactivate failed: {e}")
    # If any other service is still active, leave the global pause in place.
    if _any_service_active():
        _state_log(
            "dictation_cleared",
            source="mic_capture_watcher",
            service=name,
            still_active=[n for n, st in _service_state.items() if st["active"]],
            restored=False,
        )
        return
    restored_mic = _global["previous_microphone"] if _global["speech_disabled_by_us"] else None
    if _global["speech_disabled_by_us"]:
        try:
            if _global["previous_microphone"]:
                actions.speech.set_microphone(_global["previous_microphone"])
        except Exception as e:
            print(f"[mic_capture_watcher] enable failed: {e}")
        _global["speech_disabled_by_us"] = False
        _global["previous_microphone"] = None
    woke_mouse = _global["mouse_slept_by_us"]
    if _global["mouse_slept_by_us"]:
        try:
            actions.user.mouse_wake("watcher")
        except Exception as e:
            print(f"[mic_capture_watcher] mouse_wake failed: {e}")
        _global["mouse_slept_by_us"] = False
    _state_log(
        "dictation_cleared",
        source="mic_capture_watcher",
        service=name,
        still_active=[],
        restored=True,
        restored_mic=restored_mic,
        woke_mouse=woke_mouse,
    )
    if service is not None:
        app.notify(f"Talon resumed: {service['display']} closed")


def _tick():
    active_names = _services_active()
    for s in CAPTURE_SERVICES:
        name = s["name"]
        was_active = _service_state[name]["active"]
        is_active = name in active_names
        if is_active and not was_active:
            _activate(name)
        elif not is_active and was_active:
            _deactivate(name)
    # Log every mic-name change we observe, regardless of cause. Any change
    # that isn't paired with a same-tick source-specific entry above (or a
    # toggle_talon_sleep_* line) came from outside this module — HUD mic
    # click, voice command, OS, etc.
    try:
        current_mic = actions.sound.active_microphone()
    except Exception:
        current_mic = None
    last = _global["last_polled_mic"]
    if current_mic != last:
        _global["last_polled_mic"] = current_mic
        # Skip the very first tick after load so we don't log the initial
        # observation as if it were a change.
        if last is not None or current_mic not in (None, "None"):
            _state_log(
                "mic_changed",
                source="mic_poll",
                old=last,
                new=current_mic,
                watcher_active=[n for n, st in _service_state.items() if st["active"]],
                speech_disabled_by_watcher=_global["speech_disabled_by_us"],
            )
    # Same idea for the eye tracker: capture every flip in the queryable
    # tracking-state tuple so we can correlate "dictation started but
    # tracker stayed on" against the events around it. control_gaze /
    # control_head are not queryable, so this triple is the best we get.
    try:
        tracking = (
            actions.tracking.control_enabled(),
            actions.tracking.control_zoom_enabled(),
            actions.tracking.control1_enabled(),
        )
    except Exception:
        tracking = None
    last_tracking = _global["last_polled_tracking"]
    if tracking is not None and tracking != last_tracking:
        _global["last_polled_tracking"] = tracking
        if last_tracking is not None:
            _state_log(
                "tracking_changed",
                source="tracking_poll",
                old_control=last_tracking[0],
                old_zoom=last_tracking[1],
                old_control1=last_tracking[2],
                new_control=tracking[0],
                new_zoom=tracking[1],
                new_control1=tracking[2],
                watcher_active=[n for n, st in _service_state.items() if st["active"]],
                mouse_slept_by_watcher=_global["mouse_slept_by_us"],
            )


def _start_polling():
    if _global["cron"] is not None:
        return
    interval_ms = int(settings.get("user.mic_capture_poll_ms"))
    _global["cron"] = cron.interval(f"{interval_ms}ms", _tick)


def _stop_polling():
    if _global["cron"] is not None:
        cron.cancel(_global["cron"])
        _global["cron"] = None
    if _global["speech_disabled_by_us"]:
        try:
            if _global["previous_microphone"]:
                actions.speech.set_microphone(_global["previous_microphone"])
        except Exception:
            pass
        _global["speech_disabled_by_us"] = False
        _global["previous_microphone"] = None
    if _global["mouse_slept_by_us"]:
        try:
            actions.user.mouse_wake("watcher")
        except Exception:
            pass
        _global["mouse_slept_by_us"] = False
    for st in _service_state.values():
        st["active"] = False
        st["disabled_by_us"] = False


def _apply_setting(*_args):
    if settings.get("user.mic_capture_watch_enabled"):
        _start_polling()
    else:
        _stop_polling()


def _on_ready():
    settings.register("user.mic_capture_watch_enabled", _apply_setting)
    settings.register("user.mic_capture_poll_ms", _apply_setting)
    _apply_setting()


app.register("ready", _on_ready)


def is_service_active(name: str) -> bool:
    """Public helper: True if the named service currently has an active capture session."""
    return _service_state.get(name, {}).get("active", False)


def mark_disabled_by_us(name: str):
    """Declare that the next deactivation of `name` should restore Talon speech/mouse,
    even if we didn't disable them this cycle. Used by voice_dictation_resume.py
    for the Win+H keystroke-cancel flow."""
    if name in _service_state:
        _service_state[name]["disabled_by_us"] = True
        _global["speech_disabled_by_us"] = True


@mod.action_class
class Actions:
    def mic_capture_start_watch():
        """Start polling for mic capture sessions and auto-pause Talon."""
        _start_polling()
        app.notify("Mic capture watcher: ON")

    def mic_capture_stop_watch():
        """Stop polling for mic capture sessions."""
        _stop_polling()
        app.notify("Mic capture watcher: OFF")

    def mic_capture_check_now():
        """Run a single detection pass and announce which services are active."""
        active = _services_active()
        msg = ", ".join(sorted(active)) if active else "none"
        app.notify(f"Active capture services: {msg}")
        print(f"[mic_capture_watcher] active={active}")

    def mic_capture_watcher_holds_tracker_pause() -> bool:
        """True if the watcher currently holds the tracker pause. Used by
        toggle_talon_sleep to avoid redundant mic muting/restoring while the
        watcher already owns the pause. (The tracker stack is keyed by owner
        token in mouse_sleep/mouse_wake now, so stacking no longer corrupts
        it — this guard is just for clean mic coordination.)"""
        return _global["mouse_slept_by_us"]

    def mic_capture_dump_sessions():
        """Print every audio capture session (pid, process, state) to the log.

        Start the service you want to inspect (e.g. press Ctrl+Space for
        Super Whisper), then run this. The capturing process should appear
        with state=Active.
        """
        monitor, err = _import_monitor()
        if monitor is None:
            print(
                f"[mic_capture_watcher] comtypes missing: {err}. "
                "Run install_deps.bat."
            )
            return
        try:
            sessions = monitor.list_active_capture_sessions()
        except Exception as e:
            print(f"[mic_capture_watcher] enumerate failed: {e}")
            return
        print(f"=== mic_capture_watcher: {len(sessions)} capture sessions ===")
        for pid, name, state in sessions:
            label = {0: "Inactive", 1: "Active", 2: "Expired"}.get(state, str(state))
            print(f"pid={pid:>6}  state={label:<8}  proc={name!r}")
        print("=== end session dump ===")
