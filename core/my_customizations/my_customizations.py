from talon import Module, Context, actions, imgui, scope

#Below is for the navigation_text()
import re

#Below is for the talon_relaunch()
from talon import ui, app
import os



@imgui.open(x=700, y=0)
def gui_select(gui: imgui.GUI):
    gui.text(f"Select mode:")
    gui.line()
    if gui.button("End selection"):
        actions.user.select_continous(0)

modifier = ""

# State for toggle_talon_sleep: the mic name active at pause time, so we
# can restore it on resume. We pause via the input device (set_microphone
# "None") because speech.disable/enable can leave Talon's cubeb stream in
# a stale state — same reasoning as mic_capture_watcher.
_mic_before_sleep = None
@imgui.open(x=700, y=0)
def gui_hold_modifier(gui: imgui.GUI):
    gui.text(f"Modifier held:")
    gui.line()
    if gui.button("Lift " + modifier):
        actions.key(modifier + ":up")
        actions.user.gui_hold_modifier_toggle(0, modifier)


mod = Module()

@mod.action_class
class Actions:
    def repeat_command_wrapper(rep: int):
        """Repeats the command `rep` times with wait times in between each repetition"""

    def repeat_phrase_wrapper(rep: int):
        """Repeats the phrase `rep` times with wait times in between each repetition"""

    def open_specific_tab(browser: str, search_str: str):
        """This function requires that the searched for tab actually is open in the browser"""

    def open_browser_profile_switcher(browser: str):
        """sdf"""

    def open_specific_profile(browser: str):
        """sdf"""

    def gui_hold_modifier_toggle(flag: int, key_str: str):
        """sdf"""

    def talon_relaunch():
        """Quit and relaunch the Talon app"""

    def talon_close():
        """Quit the Talon app without relaunching"""

    def close_program():
        """Uses the OS built-in keyboard shortcut to close the program"""

    def current_app(name: str):
        """Confirms if an app with app.name == name is in focus"""

    def replace_text(to_replace: str, replacer: str):
        """Replaces `to_replace` with `replacer`"""

    def slack_toggle_huddle():
        """sdf"""

    def select_continous(run: int):
        """sdf"""

    def select_continous_end():
        """sdf"""

    def toggle_talon_sleep():
        """Pause Talon by muting the mic (set_microphone "None") and sleeping
        the mouse, or resume by restoring both. Does NOT change Talon's mode
        — same primitive the mic_capture_watcher uses, so external dictation
        and the keypad-divide pause stay symmetric."""

    def toggle_talon_sleep_holds_tracker_pause() -> bool:
        """True if toggle_talon_sleep is the current owner of an active
        mouse_sleep state. Used by mic_capture_watcher to avoid stacking
        a second mouse_sleep on top, which would orphan the _sleep_depth
        counter and leave the tracker permanently off."""

ctx=Context()

@ctx.action_class("user")
class UserActions:
    def repeat_command_wrapper(rep: int):
        """Repeats the command rep times with wait times in between each repetition"""
        for i in range(rep):
            actions.core.repeat_command(1)
            actions.sleep("200ms")

    def repeat_phrase_wrapper(rep: int):
        """Repeats the phrase rep times with wait times in between each repetition"""
        for i in range(rep):
            actions.core.repeat_phrase(1)
            actions.sleep("200ms")

    def open_specific_tab(browser: str, search_str: str):
        """This function requires that the searched for tab actually is open in the browser"""
        if actions.user.current_app(browser) == False:
            actions.user.switcher_focus(browser)
            actions.sleep("400ms")
            #Check that the browser was successfully opened
            if actions.user.current_app(browser) == False:
                #If not, return
                return
        #Using the browser's built-in keyboard shortcuts
        #actions.key("ctrl-shift-a")
        #actions.sleep("400ms")
        #actions.auto_insert(search_str)
        #actions.sleep("400ms")
        #actions.key("enter")
        #Using Rango commands
        actions.user.rango_focus_tab_by_text(search_str)

    def open_browser_profile_switcher(browser: str):
        if actions.user.current_app(browser) == False:
            actions.user.switcher_focus(browser)
            actions.sleep("400ms")
            #Check that the browser was successfully opened
            if actions.user.current_app(browser) == False:
                #If not, return
                return
        actions.sleep("200ms")
        actions.key("ctrl-shift-m")
        actions.sleep("200ms")
        actions.key("shift-tab")
        actions.sleep("200ms")
        actions.key("enter")

    def gui_hold_modifier_toggle(flag: int, key_str: str):
        global modifier
        modifier = key_str
        if flag:
            gui_hold_modifier.show()
        else:
            gui_hold_modifier.hide()

    # From this repo:
    # https://github.com/nriley/knausj_talon/blob/ed7b1c1e/code/talon_helpers.py#L161
    def talon_relaunch():
        """Quit and relaunch the Talon app"""
        talon_app = ui.apps(pid=os.getpid())[0]
        if app.platform == "windows":
            os.startfile(talon_app.exe)
            talon_app.quit()  
        elif app.platform == "mac":
            from shlex import quote
            from subprocess import Popen

            talon_app_path = quote(talon_app.path)
            Popen(
                [
                    "/bin/sh",
                    "-c",
                    f"/usr/bin/open -W {talon_app_path} ; /usr/bin/open {talon_app_path}",
                ],
                start_new_session=True,
            )
            talon_app.quit()

    def talon_close():
        """Quit the Talon app without relaunching"""
        talon_app = ui.apps(pid=os.getpid())[0]
        talon_app.quit()

    def close_program():
        """Uses the OS built-in keyboard shortcut to close the program"""
        if app.platform == "windows":
            actions.key("alt-f4")
        elif app.platform == "mac":
            actions.key("cmd-q")
    
    def current_app(name: str):
        """Confirms if an app with app.name == name is in focus"""
        active_app = ui.active_app()
        if active_app.name == name:
            return True
        else: 
            return False

    #System wide toggle huddle function. Works only if one uses the Slack desktop app, not the Slack web app
    def slack_toggle_huddle():
        if actions.user.current_app("Slack"):
            actions.key("ctrl-shift-h")
        else:
            actions.user.switcher_focus("Slack")
            actions.sleep("300ms")
            if actions.user.current_app("Slack"):
                actions.key("ctrl-shift-h")

    def replace_text(to_replace: str, replacer: str):
        """Replaces `to_replace` with `replacer`"""
        actions.user.navigation_literal_text("GO", "left", "AFTER", to_replace, 1)
        actions.edit.select_word()
        actions.insert(replacer)
        actions.key("space")

    # Non working prototype as of now
    def select_continous(run: int):

        gui_select.show()
        # Start selection

        # https://stackoverflow.com/questions/3969947/how-can-i-trigger-and-listen-for-events-in-python
        # self.actions.key(left:down).bind("left", actions.edit.extend_word_left())
        # self.actions.key(left:down).bind("right", actions.edit.extend_word_right())

        i = 0
        while run > 0:
            print("I will run forever")
            actions.sleep("75ms")
            # if actions.key(left:down)
            #     actions.edit.extend_word_left()
            #     actions.sleep("75ms")
            # elif actions.key(right:down)
            #     actions.edit.extend_word_right()
            #     actions.sleep("75ms")

    # Non working prototype as of now
    def select_continous_end():
        """sdf"""
        gui_select.hide()

    def toggle_talon_sleep():
        global _mic_before_sleep
        if _mic_before_sleep:
            # Paused → wake: restore the previously-active mic and mouse.
            restored = _mic_before_sleep
            actions.speech.set_microphone(_mic_before_sleep)
            _mic_before_sleep = None
            actions.user.mouse_wake()
            actions.user.mic_and_eye_tracker_state_log(
                "toggle_talon_sleep_resume",
                {"source": "toggle_talon_sleep", "restored_mic": restored},
            )
        else:
            # Awake → pause. If the watcher already holds the tracker
            # pause (external dictation is active), skip entirely —
            # stacking a second mouse_sleep on top of the watcher's would
            # bump _sleep_depth to 2, and the watcher's eventual wake
            # would only decrement to 1, leaving the tracker stuck off.
            # The user's press is effectively a no-op here since Talon
            # is already paused by the watcher.
            if actions.user.mic_capture_watcher_holds_tracker_pause():
                actions.user.mic_and_eye_tracker_state_log(
                    "toggle_talon_sleep_skipped",
                    {"source": "toggle_talon_sleep", "reason": "watcher_holds_tracker_pause"},
                )
                return
            # Awake → pause: same primitive the mic_capture_watcher uses
            # (set_microphone "None" + mouse_sleep), no mode change.
            current_mic = actions.sound.active_microphone()
            saved = None
            if current_mic and current_mic != "None":
                _mic_before_sleep = current_mic
                saved = current_mic
                actions.speech.set_microphone("None")
            actions.user.mouse_sleep()
            actions.user.mic_and_eye_tracker_state_log(
                "toggle_talon_sleep_pause",
                {"source": "toggle_talon_sleep", "saved_mic": saved, "current_mic": current_mic},
            )

    def toggle_talon_sleep_holds_tracker_pause() -> bool:
        return _mic_before_sleep is not None