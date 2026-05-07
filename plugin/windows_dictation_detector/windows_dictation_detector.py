from talon import Module, actions, app, cron, scope, settings

mod = Module()

mod.setting(
    "windows_dictation_watch_enabled",
    type=bool,
    default=True,
    desc="When True, watch for Windows voice typing (Win+H) and auto-pause Talon speech + mouse while it's listening. Set to False in settings.talon to disable.",
)

mod.setting(
    "windows_dictation_poll_ms",
    type=int,
    default=300,
    desc="Polling interval in ms for checking if Windows voice typing (Win+H) is actively listening.",
)

# Process names whose active capture session indicates Windows voice typing
# is listening. On Win11, the dictation pill runs in-process inside
# TextInputHost.exe. SpeechRuntime.exe is included as a fallback for builds
# that still spawn it.
DICTATION_CAPTURE_PROCESSES = {
    "textinputhost.exe",
    "speechruntime.exe",
}


def _import_monitor():
    """Lazy import so a missing comtypes dep doesn't crash module load."""
    try:
        from . import audio_session_monitor
        return audio_session_monitor, None
    except ImportError as e:
        return None, e


def _dictation_active() -> bool:
    monitor, err = _import_monitor()
    if monitor is None:
        print(
            f"[windows_dictation_detector] comtypes missing: {err}. "
            "Run plugin/windows_dictation_detector/install_deps.bat."
        )
        return False
    try:
        return monitor.is_process_capturing(DICTATION_CAPTURE_PROCESSES)
    except Exception as e:
        print(f"[windows_dictation_detector] capture check failed: {e}")
        return False


_state = {
    "active": False,
    "disabled_by_us": False,
    "mouse_slept_by_us": False,
    "cron": None,
}


def _tick():
    active = _dictation_active()
    if active and not _state["active"]:
        _state["active"] = True
        # If Talon is already in sleep mode, don't touch speech or the mouse.
        # speech.enable() on resume would wake Talon, and stacking a sleep
        # here would entangle our restore with the user's "talon wake".
        was_sleeping = "sleep" in scope.get("mode")
        try:
            if was_sleeping or not actions.speech.enabled():
                _state["disabled_by_us"] = False
            else:
                actions.speech.disable()
                _state["disabled_by_us"] = True
        except Exception as e:
            print(f"[windows_dictation_detector] disable failed: {e}")
        if not was_sleeping:
            try:
                actions.user.mouse_sleep()
                _state["mouse_slept_by_us"] = True
            except Exception as e:
                print(f"[windows_dictation_detector] mouse_sleep failed: {e}")
        app.notify("Talon paused: Windows Dictation active")
    elif not active and _state["active"]:
        _state["active"] = False
        try:
            actions.user.voice_dictation_disarm_keypress_resume()
        except Exception:
            pass
        if _state["disabled_by_us"]:
            try:
                actions.speech.enable()
            except Exception as e:
                print(f"[windows_dictation_detector] enable failed: {e}")
        _state["disabled_by_us"] = False
        if _state["mouse_slept_by_us"]:
            try:
                actions.user.mouse_wake()
            except Exception as e:
                print(f"[windows_dictation_detector] mouse_wake failed: {e}")
        _state["mouse_slept_by_us"] = False
        app.notify("Talon resumed: Windows Dictation closed")


def _start_polling():
    if _state["cron"] is not None:
        return
    interval_ms = int(settings.get("user.windows_dictation_poll_ms"))
    _state["cron"] = cron.interval(f"{interval_ms}ms", _tick)


def _stop_polling():
    if _state["cron"] is not None:
        cron.cancel(_state["cron"])
        _state["cron"] = None
    if _state["disabled_by_us"]:
        try:
            actions.speech.enable()
        except Exception:
            pass
    if _state["mouse_slept_by_us"]:
        try:
            actions.user.mouse_wake()
        except Exception:
            pass
    _state["active"] = False
    _state["disabled_by_us"] = False
    _state["mouse_slept_by_us"] = False


def _apply_setting(*_args):
    if settings.get("user.windows_dictation_watch_enabled"):
        _start_polling()
    else:
        _stop_polling()


def _on_ready():
    settings.register("user.windows_dictation_watch_enabled", _apply_setting)
    settings.register("user.windows_dictation_poll_ms", _apply_setting)
    _apply_setting()


app.register("ready", _on_ready)


@mod.action_class
class Actions:
    def windows_dictation_start_watch():
        """Start polling for Windows Dictation and auto-toggle Talon speech."""
        _start_polling()
        app.notify("Windows Dictation watcher: ON")

    def windows_dictation_stop_watch():
        """Stop polling for Windows Dictation."""
        _stop_polling()
        app.notify("Windows Dictation watcher: OFF")

    def windows_dictation_check_now():
        """Run a single detection pass and announce the result."""
        active = _dictation_active()
        app.notify(f"Dictation active: {active}")
        print(f"[windows_dictation_detector] active={active}")

    def windows_dictation_dump_sessions():
        """Print every audio capture session (pid, process, state) to the log.

        Press Win+H, start it actively listening, then run this. The session
        for the dictation host should appear with state=1 (Active).
        """
        monitor, err = _import_monitor()
        if monitor is None:
            print(
                f"[windows_dictation_detector] comtypes missing: {err}. "
                "Run install_deps.bat."
            )
            return
        try:
            sessions = monitor.list_active_capture_sessions()
        except Exception as e:
            print(f"[windows_dictation_detector] enumerate failed: {e}")
            return
        print(f"=== windows_dictation_detector: {len(sessions)} capture sessions ===")
        for pid, name, state in sessions:
            label = {0: "Inactive", 1: "Active", 2: "Expired"}.get(state, str(state))
            print(f"pid={pid:>6}  state={label:<8}  proc={name!r}")
        print("=== end session dump ===")
