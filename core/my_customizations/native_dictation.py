"""Manual microphone control and native dictation entry points."""

from talon import Context, Module, actions, app, scope

mod = Module()
ctx = Context()


@mod.action_class
class Actions:
    def toggle_talon_microphone():
        """Pause or resume Talon's microphone and eye tracking."""

    def start_stop_dictation():
        """Toggle native operating-system dictation."""

    def toggle_dictation_voice_command():
        """Toggle native dictation from a voice command."""

    def toggle_dictation_key_switch():
        """Toggle native dictation from a physical key."""


@ctx.action_class("user")
class UserActions:
    def toggle_talon_microphone():
        actions.user.toggle_talon_sleep()

    def start_stop_dictation():
        if app.platform == "windows":
            actions.key("super-h")
        elif app.platform == "mac":
            actions.user.mac_dictation_toggle()
        else:
            raise RuntimeError("Native dictation is configured only for Windows and macOS")

    def toggle_dictation_voice_command():
        if app.platform == "mac":
            actions.user.mac_dictation_toggle()
            return
        if app.platform != "windows":
            raise RuntimeError("Native dictation is configured only for Windows and macOS")
        if "sleep" in scope.get("mode"):
            actions.sleep("500ms")
            actions.user.mouse_wake("dictation")
            actions.speech.toggle()
            actions.user.voice_dictation_disarm_keypress_resume()
        else:
            actions.user.mouse_sleep("dictation")
            actions.speech.toggle()
            actions.user.start_stop_dictation()
            actions.user.voice_dictation_arm_keypress_resume()

    def toggle_dictation_key_switch():
        if app.platform == "mac":
            actions.user.mac_dictation_toggle()
            return
        if app.platform != "windows":
            raise RuntimeError("Native dictation is configured only for Windows and macOS")
        actions.user.toggle_talon_microphone()
        actions.user.start_stop_dictation()
        actions.user.voice_dictation_arm_keypress_resume()
