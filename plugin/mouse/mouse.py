from dataclasses import dataclass
from pathlib import Path

from talon import Context, Module, actions, app, ctrl, imgui, settings, ui

# Guarded import: talon.plugins.eye_mouse_2 transitively imports eye_mouse,
# which calls into the Tobii driver at import time and raises EyeClosedErr
# when the tracker is disconnected. Catching that here means a missing /
# hung tracker stops eye-mask features from working — but does NOT bring
# down the entire mouse plugin (and the chain of modules that depend on
# user.mouse_sleep / user.mouse_wake).
try:
    from talon.plugins.eye_mouse_2 import set_eye_mask
except Exception as _eye_import_err:
    print(f"[mouse] eye_mouse_2 import failed ({_eye_import_err}); set_eye_mask disabled")

    def set_eye_mask(*_args, **_kwargs):
        pass

mod = Module()
ctx = Context()

mod.list(
    "mouse_button",
    desc="List of mouse button words to mouse_click index parameter",
)
mod.setting(
    "mouse_enable_pop_click",
    type=int,
    default=0,
    desc="Pop noise clicks left mouse button. 0 = off, 1 = on with eyetracker but not with zoom mouse mode, 2 = on but not with zoom mouse mode",
)
mod.setting(
    "mouse_enable_pop_stops_scroll",
    type=bool,
    default=False,
    desc="When enabled, pop stops continuous scroll modes (wheel upper/downer/gaze)",
)
mod.setting(
    "mouse_enable_pop_stops_drag",
    type=bool,
    default=False,
    desc="When enabled, pop stops mouse drag",
)
mod.setting(
    "mouse_wake_hides_cursor",
    type=bool,
    default=False,
    desc="When enabled, mouse wake will hide the cursor. mouse_wake enables zoom mouse.",
)


##### My customizations #####
_EYE_TRACKING_MODE_FILE = Path(__file__).resolve().parents[2] / "stored_state" / "eye_tracking_mode"
_VALID_EYE_TRACKING_MODES = {"gaze control", "hiss control", "no eye tracker"}


def _load_eye_tracking_mode() -> str:
    try:
        value = _EYE_TRACKING_MODE_FILE.read_text(encoding="utf-8").strip()
    except OSError:
        return "gaze control"
    return value if value in _VALID_EYE_TRACKING_MODES else "gaze control"


def _save_eye_tracking_mode(value: str) -> None:
    try:
        _EYE_TRACKING_MODE_FILE.parent.mkdir(parents=True, exist_ok=True)
        _EYE_TRACKING_MODE_FILE.write_text(value, encoding="utf-8")
    except OSError as exc:
        actions.print(f"Failed to persist eye tracking mode: {exc}")


eye_tracking = _load_eye_tracking_mode()


def get_eye_tracking_variable():
    return eye_tracking
##### End #####


@dataclass(slots=True)
class EyeTrackingState:
    """Eye tracking state that can be queried with tracking.*_enabled actions
    This is cached on the user.mouse_sleep action so the state can be restored on the user.mouse_wake action.
    """

    control_zoom: bool
    control: bool
    control1: bool


eye_tracking_state: EyeTrackingState

# mouse_sleep / mouse_wake are re-entrant: only the outermost sleep takes a
# snapshot, only the outermost wake restores it. This prevents overlapping
# callers (e.g. mic_capture_watcher + a voice command) from clobbering
# each other's saved state.
_sleep_depth = 0


def _log_tracker_event(event: str, **fields):
    """Best-effort: append a tracker state-change line to mic_state.log so
    eye-tracker sync bugs (depth drift, missed wake, etc.) can be diagnosed
    after the fact. Never propagate failures into the sleep/wake path."""
    try:
        actions.user.mic_and_eye_tracker_state_log(event, {"source": "mouse_sleep_wake", **fields})
    except Exception:
        pass


def on_ready():
    global eye_tracking_state
    eye_tracking_state = EyeTrackingState(
        actions.tracking.control_zoom_enabled(),
        actions.tracking.control_enabled(),
        actions.tracking.control1_enabled(),
    )


app.register("ready", on_ready)


@imgui.open(x=700, y=0)
def gui_drag(gui: imgui.GUI):
    gui.text("Drag mode:")
    gui.line()
    if gui.button("End drag"):
        actions.user.mouse_drag_end()


@mod.action_class
class Actions:
    def zoom_close():
        """Closes an in-progress zoom. Talon will move the cursor position but not click."""
        actions.user.deprecate_action(
            "2024-12-26",
            "user.zoom_close",
            "tracking.zoom_cancel",
        )
        actions.tracking.zoom_cancel()

    def mouse_wake():
        """Re-enable eye tracking state and disables cursor"""
        global _sleep_depth
        depth_before = _sleep_depth
        if _sleep_depth > 1:
            _sleep_depth -= 1
            _log_tracker_event(
                "mouse_wake",
                outermost=False,
                depth_before=depth_before,
                depth_after=_sleep_depth,
            )
            return
        _sleep_depth = 0
        # Restore the exact snapshot taken at the outermost mouse_sleep.
        actions.tracking.control_zoom_toggle(eye_tracking_state.control_zoom)
        actions.tracking.control_toggle(eye_tracking_state.control)
        actions.tracking.control1_toggle(eye_tracking_state.control1)
        # Gaze/head are not query-able, so re-apply them from the user's
        # eye_tracking mode setting (the source of truth for their default).
        if eye_tracking == "gaze control":
            actions.tracking.control_gaze_toggle(True)
            actions.tracking.control_head_toggle(True)

        if settings.get("user.mouse_wake_hides_cursor"):
            actions.user.mouse_cursor_hide()

        _log_tracker_event(
            "mouse_wake",
            outermost=True,
            depth_before=depth_before,
            depth_after=_sleep_depth,
            restored_control=eye_tracking_state.control,
            restored_control_zoom=eye_tracking_state.control_zoom,
            restored_control1=eye_tracking_state.control1,
            eye_tracking_mode=eye_tracking,
        )

    def mouse_drag(button: int):
        """Press and hold/release a specific mouse button for dragging"""
        # Clear any existing drags
        actions.user.mouse_drag_end()

        # Start drag
        actions.mouse_drag(button)
        gui_drag.show()

    def mouse_drag_end() -> bool:
        """Releases any held mouse buttons"""
        buttons = ctrl.mouse_buttons_down()
        gui_drag.hide()
        if buttons:
            for button in buttons:
                actions.mouse_release(button)
            return True
        return False

    def mouse_drag_toggle(button: int):
        """If the button is held down, release the button, else start dragging"""
        if button in ctrl.mouse_buttons_down():
            actions.mouse_release(button)
        else:
            actions.mouse_drag(button)

    def mouse_sleep():
        """Disables control mouse, zoom mouse, and re-enables cursor"""
        global _sleep_depth, eye_tracking_state
        depth_before = _sleep_depth
        outermost = _sleep_depth == 0
        if outermost:
            # Outermost sleep: snapshot current tracking state for restore.
            eye_tracking_state.control_zoom = actions.tracking.control_zoom_enabled()
            eye_tracking_state.control = actions.tracking.control_enabled()
            eye_tracking_state.control1 = actions.tracking.control1_enabled()

            actions.tracking.control_zoom_toggle(False)
            actions.tracking.control_toggle(False)
            actions.tracking.control1_toggle(False)
            # Gaze/head can't be queried, but we always want them off while
            # asleep so the cursor doesn't follow eye/head movement.
            actions.tracking.control_gaze_toggle(False)
            actions.tracking.control_head_toggle(False)

            actions.user.mouse_cursor_show()
            actions.user.mouse_scroll_stop()
            actions.user.mouse_drag_end()
        _sleep_depth += 1
        _log_tracker_event(
            "mouse_sleep",
            outermost=outermost,
            depth_before=depth_before,
            depth_after=_sleep_depth,
            snapshot_control=eye_tracking_state.control if outermost else None,
            snapshot_control_zoom=eye_tracking_state.control_zoom if outermost else None,
            snapshot_control1=eye_tracking_state.control1 if outermost else None,
        )

    def copy_mouse_position():
        """Copy the current mouse position coordinates"""
        x, y = actions.mouse_x(), actions.mouse_y()
        actions.clip.set_text(f"{x}, {y}")

    def mouse_move_center_active_window():
        """Move the mouse cursor to the center of the currently active window"""
        rect = ui.active_window().rect
        actions.mouse_move(rect.center.x, rect.center.y)

    def enable_gaze_control():
        """Switch eye tracking to gaze-control mode (hiss triggers scroll)"""
        global eye_tracking
        eye_tracking = "gaze control"
        _save_eye_tracking_mode(eye_tracking)
        actions.tracking.control_toggle(True)
        actions.tracking.control_gaze_toggle(True)
        actions.tracking.control_head_toggle(True)
        set_eye_mask("both")

    def enable_hiss_control():
        """Switch eye tracking to hiss-control mode (hiss toggles gaze/head tracking)"""
        global eye_tracking
        eye_tracking = "hiss control"
        _save_eye_tracking_mode(eye_tracking)
        actions.tracking.control_toggle(True)
        actions.tracking.control_gaze_toggle(False)
        actions.tracking.control_head_toggle(False)
        set_eye_mask("left")

    def enable_no_eye_tracker_mode():
        """Switch to no-eye-tracker mode so toggles skip eye tracking actions"""
        global eye_tracking
        eye_tracking = "no eye tracker"
        _save_eye_tracking_mode(eye_tracking)
        actions.tracking.control_zoom_toggle(False)
        actions.tracking.control_toggle(False)
        actions.tracking.control1_toggle(False)
        actions.user.mouse_cursor_show()

    def set_eye_tracking_mask(mask: str):
        """Set Talon eye selection. mask is "both", "left", or "right"."""
        set_eye_mask(mask)


# https://talonvoice.com/docs/index.html#talon-noise
@ctx.action_class("user")
class UserActions:
    def noise_trigger_pop():
        dont_click = False

        # Allow pop to stop drag
        if settings.get("user.mouse_enable_pop_stops_drag"):  # noqa: SIM102
            if actions.user.mouse_drag_end():
                dont_click = True

        # Allow pop to stop scroll
        if settings.get("user.mouse_enable_pop_stops_scroll"):  # noqa: SIM102
            if actions.user.mouse_scroll_stop():
                dont_click = True

        if dont_click:
            return

        # Otherwise respect the mouse_enable_pop_click setting
        setting_val = settings.get("user.mouse_enable_pop_click")

        is_using_eye_tracker = (
            actions.tracking.control_zoom_enabled()
            or actions.tracking.control_enabled()
            or actions.tracking.control1_enabled()
        )

        should_click = (
            setting_val == 2 and not actions.tracking.control_zoom_enabled()
        ) or (
            setting_val == 1
            and is_using_eye_tracker
            and not actions.tracking.control_zoom_enabled()
        )

        if should_click:
            ctrl.mouse_click(button=0, hold=16000)

    # Gaze control is now activated while hissing.
    # Should be used with the setting "Only Left Eye" or "Only Right Eye" because it
    # doesn't work remotely as reliably with "Use Both Eyes" enabled in Talon 0.4.
    def noise_trigger_hiss(active: bool):
        if active:
            if eye_tracking == "gaze control":
                if settings.get("user.mouse_enable_hiss_scroll"):
                    actions.user.mouse_scroll_down_continuous()
            else:
                actions.tracking.control_gaze_toggle(True)
                actions.tracking.control_head_toggle(True)
        else:
            if eye_tracking == "gaze control":
                if settings.get("user.mouse_enable_hiss_scroll"):
                    actions.user.mouse_scroll_stop()
            else:
                actions.tracking.control_gaze_toggle(False)
                actions.tracking.control_head_toggle(False)
