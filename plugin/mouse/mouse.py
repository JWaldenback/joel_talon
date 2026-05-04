from dataclasses import dataclass

<<<<<<< HEAD
from talon import Context, Module, actions, app, clip, cron, ctrl, imgui, settings, ui
from talon_plugins import eye_zoom_mouse

key = actions.key
self = actions.self
scroll_amount = 0
click_job = None
scroll_job = None
gaze_job = None
cancel_scroll_on_pop = True
control_mouse_forced = False
hiss_scroll_up = False

##### My customizations #####
eye_tracking = "hiss control"

def get_eye_tracking_variable():
    return eye_tracking
##### End #####

default_cursor = {
    "AppStarting": r"%SystemRoot%\Cursors\aero_working.ani",
    "Arrow": r"%SystemRoot%\Cursors\aero_arrow.cur",
    "Hand": r"%SystemRoot%\Cursors\aero_link.cur",
    "Help": r"%SystemRoot%\Cursors\aero_helpsel.cur",
    "No": r"%SystemRoot%\Cursors\aero_unavail.cur",
    "NWPen": r"%SystemRoot%\Cursors\aero_pen.cur",
    "Person": r"%SystemRoot%\Cursors\aero_person.cur",
    "Pin": r"%SystemRoot%\Cursors\aero_pin.cur",
    "SizeAll": r"%SystemRoot%\Cursors\aero_move.cur",
    "SizeNESW": r"%SystemRoot%\Cursors\aero_nesw.cur",
    "SizeNS": r"%SystemRoot%\Cursors\aero_ns.cur",
    "SizeNWSE": r"%SystemRoot%\Cursors\aero_nwse.cur",
    "SizeWE": r"%SystemRoot%\Cursors\aero_ew.cur",
    "UpArrow": r"%SystemRoot%\Cursors\aero_up.cur",
    "Wait": r"%SystemRoot%\Cursors\aero_busy.ani",
    "Crosshair": "",
    "IBeam": "",
}

# todo figure out why notepad++ still shows the cursor sometimes.
hidden_cursor = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), r"Resources\HiddenCursor.cur"
)
=======
from talon import Context, Module, actions, app, ctrl, settings, ui
>>>>>>> upstream/main

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


<<<<<<< HEAD
@imgui.open(x=700, y=0)
def gui_wheel(gui: imgui.GUI):
    gui.text(f"Scroll mode: {continuous_scroll_mode}")
    gui.line()
    #if gui.button("Wheel Stop [stop scrolling]"):
    if gui.button("Wheel stop / Scroll stop"):
        actions.user.mouse_scroll_stop()
=======
@dataclass(slots=True)
class EyeTrackingState:
    """Eye tracking state that can be queried with tracking.*_enabled actions
    This is cached on the user.mouse_sleep action so the state can be restored on the user.mouse_wake action.
    """

    control_zoom: bool
    control: bool
    control1: bool


eye_tracking_state: EyeTrackingState


def on_ready():
    global eye_tracking_state
    eye_tracking_state = EyeTrackingState(
        actions.tracking.control_zoom_enabled(),
        actions.tracking.control_enabled(),
        actions.tracking.control1_enabled(),
    )


app.register("ready", on_ready)
>>>>>>> upstream/main


@imgui.open(x=700, y=0)
def gui_drag(gui: imgui.GUI):
    gui.text(f"Drag mode:")
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
<<<<<<< HEAD
        """Enable zoom mouse"""
        #actions.tracking.control_zoom_toggle(True)
        """Enable control mouse"""
        actions.tracking.control_toggle(True)
=======
        """Re-enable eye tracking state and disables cursor"""
        # restore eye tracking modes enabled as of the last user.mouse_sleep
        if eye_tracking_state.control_zoom:
            actions.tracking.control_zoom_toggle(True)
        if eye_tracking_state.control:
            actions.tracking.control_toggle(True)
        if eye_tracking_state.control1:
            actions.tracking.control1_toggle(True)
>>>>>>> upstream/main

        if settings.get("user.mouse_wake_hides_cursor"):
            actions.user.mouse_cursor_hide()

    def mouse_drag(button: int):
        """Press and hold/release a specific mouse button for dragging"""
        # Clear any existing drags
        actions.user.mouse_drag_end()

        # Start drag
<<<<<<< HEAD
        ctrl.mouse_click(button=button, down=True)
        gui_drag.show()
=======
        actions.mouse_drag(button)
>>>>>>> upstream/main

    def mouse_drag_end() -> bool:
        """Releases any held mouse buttons"""
<<<<<<< HEAD
        for button in ctrl.mouse_buttons_down():
            ctrl.mouse_click(button=button, up=True)
        gui_drag.hide()
=======
        buttons = ctrl.mouse_buttons_down()
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
>>>>>>> upstream/main

    def mouse_sleep():
        """Disables control mouse, zoom mouse, and re-enables cursor"""
        # save eye tracking state so it can be restored on user.mouse_wake
        global eye_tracking_state
        eye_tracking_state.control_zoom = actions.tracking.control_zoom_enabled()
        eye_tracking_state.control = actions.tracking.control_enabled()
        eye_tracking_state.control1 = actions.tracking.control1_enabled()

        actions.tracking.control_zoom_toggle(False)
        actions.tracking.control_toggle(False)
        actions.tracking.control1_toggle(False)

        actions.user.mouse_cursor_show()
        actions.user.mouse_scroll_stop()
        actions.user.mouse_drag_end()

<<<<<<< HEAD
    def mouse_scroll_down(amount: float = 1):
        """Scrolls down"""
        mouse_scroll(amount * settings.get("user.mouse_wheel_down_amount"))()


    #Since I have tweaked the Rango scroll to intercept `mouse_scroll_down()`, thus making it possible to just have one set of scroll actions, there is a need for a second scroll function (when browsing) that will not be intercepted by Rango.
    def mouse_scroll_down_no_rango(amount: float = 1):
        """Scrolls down"""
        mouse_scroll(amount * settings.get("user.mouse_wheel_down_amount"))()

    def mouse_scroll_up_no_rango(amount: float = 1):
        """Scrolls up"""
        mouse_scroll(-amount * settings.get("user.mouse_wheel_down_amount"))()


    def mouse_scroll_down_continuous():
        """Scrolls down continuously"""
        global continuous_scroll_mode
        continuous_scroll_mode = "scroll down continuous"
        mouse_scroll(settings.get("user.mouse_continuous_scroll_amount"))()

        if scroll_job is None:
            start_scroll()

        if not settings.get("user.mouse_hide_mouse_gui"):
            gui_wheel.show()

    def mouse_scroll_up(amount: float = 1):
        """Scrolls up"""
        mouse_scroll(-amount * settings.get("user.mouse_wheel_down_amount"))()

    def mouse_scroll_up_continuous():
        """Scrolls up continuously"""
        global continuous_scroll_mode
        continuous_scroll_mode = "scroll up continuous"
        mouse_scroll(-settings.get("user.mouse_continuous_scroll_amount"))()

        if scroll_job is None:
            start_scroll()
        if not settings.get("user.mouse_hide_mouse_gui"):
            gui_wheel.show()

    def mouse_scroll_left(amount: float = 1):
        """Scrolls left"""
        actions.mouse_scroll(
            0, -amount * settings.get("user.mouse_wheel_horizontal_amount")
        )

    def mouse_scroll_right(amount: float = 1):
        """Scrolls right"""
        actions.mouse_scroll(
            0, amount * settings.get("user.mouse_wheel_horizontal_amount")
        )

    def mouse_scroll_stop():
        """Stops scrolling"""
        stop_scroll()

    def mouse_gaze_scroll():
        """Starts gaze scroll"""
        global continuous_scroll_mode
        # this calls stop_scroll, which resets continuous_scroll_mode
        start_cursor_scrolling()

        continuous_scroll_mode = "gaze scroll"

        if not settings.get("user.mouse_hide_mouse_gui"):
            gui_wheel.show()

        # enable 'control mouse' if eye tracker is present and not enabled already
        global control_mouse_forced
        if not actions.tracking.control_enabled():
            actions.tracking.control_toggle(True)
            control_mouse_forced = True

=======
>>>>>>> upstream/main
    def copy_mouse_position():
        """Copy the current mouse position coordinates"""
        x, y = actions.mouse_x(), actions.mouse_y()
        actions.clip.set_text(f"{x}, {y}")

    def mouse_move_center_active_window():
        """Move the mouse cursor to the center of the currently active window"""
        rect = ui.active_window().rect
<<<<<<< HEAD
        ctrl.mouse_move(rect.left + (rect.width / 2), rect.top + (rect.height / 2))

    def hiss_scroll_up():
        """Change mouse hiss scroll direction to up"""
        global hiss_scroll_up
        hiss_scroll_up = True

    def hiss_scroll_down():
        """Change mouse hiss scroll direction to down"""
        global hiss_scroll_up
        hiss_scroll_up = False
    
    def enable_gaze_control():
        """sdf"""
        global eye_tracking 
        eye_tracking = "gaze control"
        actions.tracking.control_gaze_toggle(True)
        actions.tracking.control_head_toggle(True)

    def enable_hiss_control():
        """sdf"""
        global eye_tracking 
        eye_tracking = "hiss control"
        actions.tracking.control_gaze_toggle(False)
        actions.tracking.control_head_toggle(False)


def show_cursor_helper(show):
    """Show/hide the cursor"""
    if app.platform == "windows":
        import ctypes
        import winreg

        import win32con

        try:
            Registrykey = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, r"Control Panel\Cursors", 0, winreg.KEY_WRITE
            )

            for value_name, value in default_cursor.items():
                if show:
                    winreg.SetValueEx(
                        Registrykey, value_name, 0, winreg.REG_EXPAND_SZ, value
                    )
                else:
                    winreg.SetValueEx(
                        Registrykey, value_name, 0, winreg.REG_EXPAND_SZ, hidden_cursor
                    )

            winreg.CloseKey(Registrykey)

            ctypes.windll.user32.SystemParametersInfoA(
                win32con.SPI_SETCURSORS, 0, None, 0
            )

        except OSError:
            print(f"Unable to show_cursor({str(show)})")
    else:
        ctrl.cursor_visible(show)
=======
        actions.mouse_move(rect.center.x, rect.center.y)
>>>>>>> upstream/main


#https://talonvoice.com/docs/index.html#talon-noise
@ctx.action_class("user")
class UserActions:
    def noise_trigger_pop():
        dont_click = False

<<<<<<< HEAD
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
   

    #Gaze control is now activated while hissing
    #Should be used with the setting "Only Left Eye" or "Only Right Eye" because it doesn't work remotely as reliably when having the setting "Use Both Eyes" enabled in Talon 0.4
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

    """
    def noise_trigger_hiss(active: bool):
        if settings.get("user.mouse_enable_hiss_scroll"):
            if active:
                if hiss_scroll_up:
                    actions.user.mouse_scroll_up_continuous()
                else:
                    actions.user.mouse_scroll_down_continuous()
            else:
                actions.user.mouse_scroll_stop()
    """

def mouse_scroll(amount):
    def scroll():
        global scroll_amount
        if continuous_scroll_mode:
            if (scroll_amount >= 0) == (amount >= 0):
                scroll_amount += amount
            else:
                scroll_amount = amount
        actions.mouse_scroll(y=int(amount))

    return scroll


def scroll_continuous_helper():
    global scroll_amount
    # print("scroll_continuous_helper")
    if scroll_amount and (eye_zoom_mouse.zoom_mouse.state == eye_zoom_mouse.STATE_IDLE):
        actions.mouse_scroll(by_lines=False, y=int(scroll_amount / 10))


def start_scroll():
    global scroll_job
    scroll_job = cron.interval("60ms", scroll_continuous_helper)


def gaze_scroll():
    # print("gaze_scroll")
    if (
        eye_zoom_mouse.zoom_mouse.state == eye_zoom_mouse.STATE_IDLE
    ):  # or eye_zoom_mouse.zoom_mouse.state == eye_zoom_mouse.STATE_SLEEP:
        x, y = ctrl.mouse_pos()

        # the rect for the window containing the mouse
        rect = None

        # on windows, check the active_window first since ui.windows() is not z-ordered
        if app.platform == "windows" and ui.active_window().rect.contains(x, y):
            rect = ui.active_window().rect
        else:
            windows = ui.windows()
            for w in windows:
                if w.rect.contains(x, y):
                    rect = w.rect
                    break

        if rect is None:
            # print("no window found!")
=======
        # Allow pop to stop drag
        if settings.get("user.mouse_enable_pop_stops_drag"):
            if actions.user.mouse_drag_end():
                dont_click = True

        # Allow pop to stop scroll
        if settings.get("user.mouse_enable_pop_stops_scroll"):
            if actions.user.mouse_scroll_stop():
                dont_click = True

        if dont_click:
>>>>>>> upstream/main
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

<<<<<<< HEAD
def stop_scroll():
    global scroll_amount, scroll_job, gaze_job, continuous_scroll_mode
    scroll_amount = 0
    if scroll_job:
        cron.cancel(scroll_job)

    if gaze_job:
        cron.cancel(gaze_job)

    global control_mouse_forced
    if control_mouse_forced:
        actions.tracking.control_toggle(False)
        control_mouse_forced = False

    scroll_job = None
    gaze_job = None
    gui_wheel.hide()

    continuous_scroll_mode = ""


def start_cursor_scrolling():
    global scroll_job, gaze_job
    stop_scroll()
    gaze_job = cron.interval("60ms", gaze_scroll)
=======
        if should_click:
            ctrl.mouse_click(button=0, hold=16000)
>>>>>>> upstream/main
