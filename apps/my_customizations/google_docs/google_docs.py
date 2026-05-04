from talon import Module, actions, Context, app, scope

ctx_native_dictation=Context()
ctx_native_dictation.matches = r"""
os: windows
os: linux
tag: browser
browser.host: docs.google.com
"""

ctx_native_dictation.tags = ["user.docs"]

"""
#Commented out this part as it currently doesn't seem to work using Google's own dictation for some reason
#Unfortunately Google voice typing doesn't work in the Brave browser (and probably won't start working anytime soon): https://github.com/brave/brave-browser/issues/3725
@ctx_native_dictation.action_class("user")
class NativeDictationActions:
    def start_stop_dictation():
        if app.platform == "windows":
            actions.key("ctrl-shift-s")
        elif app.platform == "mac":
            actions.key("cmd-shift-s")
        #https://www.reddit.com/r/firefox/comments/w7tztb/ctrlshifts_on_google_translate_is_hijacked_by/
        #To make it work in Firefox small alterations need to be done in Firefox itself
        #Open about:config from your address bar
        #Set extensions.screenshots.disabled to true
"""
        
"""
@ctx_native_dictation.action_class("user")
class NativeDictationActions:
    def toggle_dictation_voice_command():
        current_microphone = actions.sound.active_microphone()
        if "command" in scope.get("mode"):
            if current_microphone == "None":
                actions.user.toggle_talon_microphone()
            actions.user.mouse_sleep()
            actions.mimic("dictation mode")
        elif "dictation" in scope.get("mode"):
            #Currently power mode is not supported, need to utilize a stack to know which mode to go back to
            actions.mimic("command mode")
            actions.user.mouse_wake()

    def toggle_dictation_key_switch():
        current_microphone = actions.sound.active_microphone()
        if "command" in scope.get("mode"):
            if current_microphone == "None":
                actions.user.toggle_talon_microphone()
            actions.user.mouse_sleep()
            actions.mimic("dictation mode")
        elif "dictation" in scope.get("mode"):
            #Currently power mode is not supported, need to utilize a stack to know which mode to go back to
            actions.mimic("command mode")
            actions.user.mouse_wake()
"""