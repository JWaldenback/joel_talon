# Outdated dictation/mic actions kept here for reference.
#
# The mic capture watcher in plugin/mic_capture_watcher/ now auto-pauses
# Talon's speech engine and tracking whenever a known capture service
# (Win+H, Super Whisper, ...) is listening, and resumes when it stops, so
# the manual "toggle mic + put Talon to sleep before dictation, wake it
# up after" flow below is no longer needed. The actions are still
# registered (in the same user.* namespace) so existing call sites keep
# working.

from talon import Module, Context, actions, app, scope


mod = Module()


@mod.action_class
class Actions:
    def toggle_talon_microphone():
        """Toggle the Talon microphone on/off using talon_HUD actions (please note: talon_HUD must be installed in the talon user folder for this function to work)"""

    def start_stop_dictation():
        """Start dictation on both Windows and macOS"""

    def toggle_dictation_voice_command():
        """Start dictation on both Windows and macOS using a voice command"""

    def toggle_dictation_key_switch():
        """Start dictation on both Windows and macOS using a physical key"""


ctx = Context()


@ctx.action_class("user")
class UserActions:
    """
    #If gaze control should be enabled when using the eye tracker
    def toggle_talon_microphone():
        current_microphone = actions.sound.active_microphone()
        if current_microphone == "None":
            #https://github.com/chaosparrot/talon_hud/blob/master/CUSTOMIZATION.md#log-messages
            actions.user.hud_add_log('success', 'ON') #Mic and eye tracking enabled
            actions.user.hud_toggle_microphone()
            actions.user.mouse_wake()
        elif not actions.tracking.control_enabled():
            actions.user.hud_add_log('success', 'ON') #Eye tracking enabled
            actions.user.mouse_wake()
        else:
            actions.user.hud_add_log('error', 'OFF') #Mic and eye tracking disabled
            actions.user.hud_toggle_microphone()
            actions.user.mouse_sleep()
    """
    """
    #If gaze control should be disabled when using the eye tracker, i.e. using hissing to activate gaze control
    def toggle_talon_microphone():
        current_microphone = actions.sound.active_microphone()
        eye_tracking = get_eye_tracking_variable()
        actions.print(eye_tracking)
        if current_microphone == "None":
            #https://github.com/chaosparrot/talon_hud/blob/master/CUSTOMIZATION.md#log-messages
            actions.user.hud_add_log('success', 'ON') #Mic and eye tracking enabled
            actions.user.hud_toggle_microphone()
            actions.tracking.control_toggle(True)
            actions.tracking.control_gaze_toggle(False)
        elif not actions.tracking.control_enabled():
            actions.user.hud_add_log('success', 'ON') #Eye tracking enabled
            actions.tracking.control_toggle(True)
            actions.tracking.control_gaze_toggle(False)
        else:
            actions.user.hud_add_log('error', 'OFF') #Mic and eye tracking disabled
            actions.user.hud_toggle_microphone()
            actions.user.mouse_sleep()
    """

    """
    # Previous version: bundled mic toggle with eye-tracking enable/disable
    # logic. Replaced because the bundled tracking branch could intercept the
    # mic toggle (e.g. when control_enabled() returned False the function
    # re-enabled tracking instead of muting). It also did not properly support
    # the "No Eye Tracker" mode in practice.
    def toggle_talon_microphone():
        current_microphone = actions.sound.active_microphone()
        eye_tracking = get_eye_tracking_variable()
        actions.print(current_microphone)
        actions.print(eye_tracking)
        actions.print(actions.tracking.control_enabled())

        # No eye tracker: just toggle the mic; skip all eye tracking actions.
        # Without this branch, the elif below would loop forever because
        # control_enabled() always reports False when no tracker is connected.
        if eye_tracking == "no eye tracker":
            if current_microphone == "None":
                actions.user.hud_add_log('success', 'ON')
                actions.user.hud_toggle_microphone()
            else:
                actions.user.hud_add_log('error', 'OFF')
                actions.user.hud_toggle_microphone()
            return

        if current_microphone == "None":
            #https://github.com/chaosparrot/talon_hud/blob/master/CUSTOMIZATION.md#log-messages
            actions.user.hud_add_log('success', 'ON') #Mic and eye tracking enabled
            actions.user.hud_toggle_microphone()
            if eye_tracking == "gaze control":
                actions.user.mouse_wake()
            elif eye_tracking == "hiss control":
                actions.tracking.control_toggle(True)
                actions.tracking.control_gaze_toggle(False)
        elif not actions.tracking.control_enabled(): #Eye tracking is currently disabled. Please note: one could end up here because the eye tracker is not connected.
            actions.user.hud_add_log('success', 'ON') #Eye tracking enabled
            if eye_tracking == "gaze control":
                actions.user.mouse_wake()
            elif eye_tracking == "hiss control":
                actions.tracking.control_toggle(True)
                actions.tracking.control_gaze_toggle(False)
        else:
            actions.user.hud_add_log('error', 'OFF') #Mic and eye tracking disabled
            actions.user.hud_toggle_microphone()
            actions.user.mouse_sleep()
    """

    """
    # Previous version: this function was its OWN pause/resume owner — it
    # called set_microphone("None") + mouse_sleep() / _restore_microphone() +
    # mouse_wake() directly, separate from user.toggle_talon_sleep (which the
    # HUD mic icon, HUD mode toggle, and numpad-divide all use). That made two
    # uncoordinated owners of the re-entrant mouse_sleep/mouse_wake depth
    # counter. Pausing here (Scroll Lock / "mic toggle" / foot pedal) and then
    # resuming via the HUD icon (or any mix of the two) left _sleep_depth stuck
    # at 1, so every later mouse_wake hit the "nested wake" early-return and
    # never re-enabled the eye tracker — the mic came back but the tracker
    # stayed off.
    def toggle_talon_microphone():
        current_microphone = actions.sound.active_microphone()
        eye_tracking = get_eye_tracking_variable()

        if current_microphone == "None":
            # Mic is currently OFF -> turn ON and restore tracking for the mode
            actions.user.hud_add_log('success', 'ON')
            _restore_microphone()
            if eye_tracking == "gaze control":
                actions.user.mouse_wake()
            elif eye_tracking == "hiss control":
                actions.tracking.control_toggle(True)
                actions.tracking.control_gaze_toggle(False)
        else:
            # Mic is currently ON -> turn OFF and pause tracking
            actions.user.hud_add_log('error', 'OFF')
            _disable_microphone()
            if eye_tracking != "no eye tracker":
                actions.user.mouse_sleep()
    """

    # Single source of truth for the mic + eye-tracker pause/resume is
    # user.toggle_talon_sleep — it holds the "toggle" owner token in the
    # mouse_sleep/mouse_wake stack and coordinates with the
    # mic_capture_watcher, and mouse_wake already restores
    # the tracker correctly for every eye_tracking mode (gaze / hiss / none).
    # This action now just delegates, so Scroll Lock, the "mic toggle" voice
    # command, the foot pedal, and the HUD mic icon are all the SAME function
    # and can't drift out of sync with each other.
    #
    # The green "ON" / red "OFF" HUD indicator is layered on top. Direction is
    # read from the toggle's ownership flag (not the live mic state) so the
    # label matches whether toggle_talon_sleep is about to resume or pause.
    def toggle_talon_microphone():
        resuming = actions.user.toggle_talon_sleep_holds_tracker_pause()
        actions.user.toggle_talon_sleep()
        if resuming:
            actions.user.hud_add_log('success', 'ON')
        else:
            actions.user.hud_add_log('error', 'OFF')


    def start_stop_dictation():
        """Start dictation on both Windows and macOS"""
        if app.platform == "windows":
            actions.key("super-h")
        elif app.platform == "mac":
            actions.key("ctrl")
            actions.sleep("50ms")
            actions.key("ctrl")

    """
    def toggle_dictation_voice_command():
        #if the microphone has been disabled through talon_hud then we just start the dictation without putting Talon to sleep
        current_microphone = actions.sound.active_microphone()
        if current_microphone == "None":
            actions.user.start_stop_dictation()
        #if not we must take other actions before we start the dictation
        elif "command" in scope.get("mode"):
            actions.user.mouse_sleep()
            actions.speech.toggle()
            actions.user.start_stop_dictation()
        elif "sleep" in scope.get("mode"):
            #add some sleep time to make sure talon doesn't pick up any speech
            actions.sleep("500ms")
            actions.speech.toggle()
            actions.user.mouse_wake()
    """

    def toggle_dictation_voice_command():
        if "sleep" in scope.get("mode"):
            #add some sleep time to make sure Talon doesn't pick up any speech
            actions.sleep("500ms")
            actions.user.mouse_wake("dictation")
            actions.speech.toggle()
            actions.user.voice_dictation_disarm_keypress_resume()
        else:
            actions.user.mouse_sleep("dictation")
            actions.speech.toggle()
            actions.user.start_stop_dictation()
            actions.user.voice_dictation_arm_keypress_resume()

    """
    def toggle_dictation_key_switch():
        #if the microphone has been disabled through talon_hud then we just start the dictation without putting Talon to sleep
        current_microphone = actions.sound.active_microphone()
        if current_microphone == "None":
            actions.user.start_stop_dictation()
        #if not we must take other actions before we start the dictation
        elif "command" in scope.get("mode"):
            actions.user.mouse_sleep()
            actions.speech.toggle()
            actions.user.start_stop_dictation()
        elif "dictation" in scope.get("mode"):
            actions.user.mouse_sleep()
            actions.speech.toggle()
            actions.user.start_stop_dictation()
        elif "sleep" in scope.get("mode"):
            actions.user.start_stop_dictation()
            actions.speech.toggle()
            actions.user.mouse_wake()
    """

    def toggle_dictation_key_switch():
        actions.user.toggle_talon_microphone()
        actions.user.start_stop_dictation()
        actions.user.voice_dictation_arm_keypress_resume()
        #actions.key("super-h")
