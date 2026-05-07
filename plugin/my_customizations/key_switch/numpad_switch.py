from talon import Module, Context, actions, cron, scope

mod = Module()
#Instantiation of the tags
#"user.avc", "user.zoom_mouse", "user.docs"
mod.tag("avc", desc="Tag for enabling specific commands for audio video calls")
mod.tag("zoom_mouse", desc="Indicates that zoom mouse is zoomed in")
mod.tag("native_dictation", desc="Tag for enabling native dictation for specific apps, like Google Docs")

#14 numpad keys
#refactor this later
num_of_numpad_keys = 14
#reference = [keypad0, keypad1, keypad2, keypad3, keypad4, keypad5, keypad6, keypad7, keypad8, keypad9, divide, multiply, minus, plus]
current_state = [False, False, False, False, False, False, False, False, False, False, False, False, False, False]
last_state = [False, False, False, False, False, False, False, False, False, False, False, False, False, False]
continuous_firing = [False, False, True, False, True, False, True, False, True, False, False, False, False, False]
has_fired = [False, False, False, False, False, False, False, False, False, False, False, False, False, False]

#fires call down and call up only once
# def on_interval():
#     for key in range(num_of_numpad_keys):
#         if current_state[key] != last_state[key]:
#             last_state[key] = current_state[key]
#             # Key is pressed downi
#             if current_state[key]:
#                 call_down(key)
#             # Key is released
#             else:
#                 last_state[key] = current_state[key]
#                 call_up(key)

# #fires continuously and then calls call_up only once
# def on_interval():
#     for key in range(num_of_numpad_keys):
#         # Key is pressed down
#         if current_state[key]:
#             last_state[key] = True
#             call_down(key)
#         # Key is released
#         elif (current_state[key] == False) and (last_state[key] == True):
#             last_state[key] = False
#             call_up(key)

#fires continuously if continuous_firing is set to true and then calls call_up() once when the key is released
def on_interval():
    for key in range(num_of_numpad_keys):
        # Key is pressed down
        if (current_state[key]) and (continuous_firing[key] == False) and (has_fired[key] == False):
            last_state[key] = True
            has_fired[key] = True
            call_down(key)
        elif (current_state[key]) and (continuous_firing[key] == True):
            last_state[key] = True
            call_down(key)
            actions.sleep("30ms")
        # Key is released
        elif (current_state[key] == False) and (last_state[key] == True):
            last_state[key] = False
            has_fired[key] = False
            call_up(key)

#the on_interval() below implementation below doesn't support call_up(key)
# def on_interval():
#     for key in range(4):
#         if current_state[key]:
#             # Key is pressed down
#             call_down(key)

cron.interval("10ms", on_interval)


@mod.action_class
class Actions:
    def keypad_down(key: int):
        """Keypad key down event"""
        current_state[key] = True

    def keypad_up(key: int):
        """Keypad key up event"""
        current_state[key] = False
    
    def keypad_0_down():
        """sdf"""

    def keypad_0_up():
        """sdf"""

    def keypad_1_down():
        """sdf"""

    def keypad_1_up():
        """sdf"""

    def keypad_2_down():
        """sdf"""

    def keypad_2_up():
        """sdf"""

    def keypad_3_down():
        """sdf"""

    def keypad_3_up():
        """sdf"""

    def keypad_4_down():
        """sdf"""

    def keypad_4_up():
        """sdf"""

    def keypad_5_down():
        """sdf"""

    def keypad_5_up():
        """sdf"""

    def keypad_6_down():
        """sdf"""

    def keypad_6_up():
        """sdf"""

    def keypad_7_down():
        """sdf"""

    def keypad_7_up():
        """sdf"""

    def keypad_8_down():
        """sdf"""

    def keypad_8_up():
        """sdf"""

    def keypad_9_down():
        """sdf"""

    def keypad_9_up():
        """sdf"""

    def keypad_divide_down():
        """sdf"""

    def keypad_divide_up():
        """sdf"""

    def keypad_multiply_down():
        """sdf"""

    def keypad_multiply_up():
        """sdf"""

    def keypad_minus_down():
        """sdf"""

    def keypad_minus_up():
        """sdf"""

    def keypad_plus_down():
        """sdf"""

    def keypad_plus_up():
        """sdf"""


# Default implementation
ctx = Context()

#test actions
#actions.user.play_pause()
#actions.app.notify("test notification")

@ctx.action_class("user")
class UserActions:
    def keypad_0_down():
        pass

    def keypad_0_up():
        pass

    def keypad_1_down():
        pass
        #actions.user.toggle_dictation_key_switch()

    def keypad_1_up():
        pass

    def keypad_2_down():
        actions.key("down")
        #actions.user.mouse_scroll_down()

    def keypad_2_up():
        pass

    def keypad_3_down():
        pass

    def keypad_3_up():
        pass

    def keypad_4_down():
        actions.key("left")

    def keypad_4_up():
        pass

    def keypad_5_down():
        pass

    def keypad_5_up():
        pass

    def keypad_6_down():
        actions.key("right")

    def keypad_6_up():
        pass

    def keypad_7_down():
        pass

    def keypad_7_up():
        pass

    def keypad_8_down():
        actions.key("up")
        #actions.user.mouse_scroll_up()

    def keypad_8_up():
        pass

    def keypad_9_down():
        pass

    def keypad_9_up():
        pass

    def keypad_divide_down():
        # Toggle Talon sleep/wake instead of just the microphone, so that sleep
        # and mic-mute can't drift out of sync (which left gaze mode active
        # while the mic was off).
        from talon import scope
        if "sleep" in scope.get("mode"):
            actions.mode.disable("sleep")
            actions.mode.enable("command")
        else:
            actions.mode.disable("command")
            actions.mode.disable("dictation")
            actions.mode.enable("sleep")
        #actions.user.toggle_talon_microphone()

    def keypad_divide_up():
        pass

    def keypad_multiply_down():
        pass

    def keypad_multiply_up():
        pass

    def keypad_minus_down():
        pass

    def keypad_minus_up():
        pass

    def keypad_plus_down():
        actions.core.repeat_phrase(1)

    def keypad_plus_up():
        pass


# Audio / Video conferencing
ctx_avc = Context()
ctx_avc.matches = r"""
tag: user.avc
"""

@ctx_avc.action_class("user")
class AvcActions:
    def keypad_0_down():
        pass

    def keypad_1_down():
        actions.user.avc_toggle_mute()

    def keypad_2_down():
        actions.user.avc_toggle_video()

    def keypad_3_down():
        actions.user.avc_raise_hand()

    def keypad_4_down():
        actions.user.avc_decrease_participants_tiles()

    def keypad_5_down():
        actions.user.avc_toggle_participants()

    def keypad_6_down():
        actions.user.avc_increase_participants_tiles()

    def keypad_7_down():
        actions.key("f11")

    def keypad_8_down():
        actions.user.avc_toggle_chat_window()

    def keypad_9_down():
        pass

    #def keypad_divide_down():
    #inherit the general numpad action

    def keypad_multiply_down():
        pass

    def keypad_minus_down():
        actions.user.avc_leave_call()

    def keypad_plus_down():
        pass


# Native dictation mode
ctx_native_dictation = Context()
ctx_native_dictation.matches = r"""
tag: user.native_dictation
"""

@ctx_native_dictation.action_class("user")
class NativeDictationActions:
    def keypad_2_down():
        actions.user.toggle_dictation_key_switch()


# Mouse zoom mode
ctx_zoom = Context()
ctx_zoom.matches = r"""
tag: user.zoom_mouse
"""

@ctx_zoom.action_class("user")
class ZoomActions: 
    def keypad_0_down():
        actions.user.zoom_mouse_click("triple")

    def keypad_1_down():
        actions.user.zoom_mouse_click("middle")

    def keypad_2_down():
        actions.user.zoom_mouse_click("double")

    def keypad_3_down():
        actions.user.zoom_mouse_click("right")


def call_down(key: int):
    if key == 0:
        actions.user.keypad_0_down()
    elif key == 1:
        actions.user.keypad_1_down()
    elif key == 2:
        actions.user.keypad_2_down()
    elif key == 3:
        actions.user.keypad_3_down()
    elif key == 4:
        actions.user.keypad_4_down()
    elif key == 5:
        actions.user.keypad_5_down()
    elif key == 6:
        actions.user.keypad_6_down()
    elif key == 7:
        actions.user.keypad_7_down()
    elif key == 8:
        actions.user.keypad_8_down()
    elif key == 9:
        actions.user.keypad_9_down()
    elif key == 10:
        actions.user.keypad_divide_down()
    elif key == 11:
        actions.user.keypad_multiply_down()
    elif key == 12:
        actions.user.keypad_minus_down()
    elif key == 13:
        actions.user.keypad_plus_down()


def call_up(key: int):
    if key == 0:
        actions.user.keypad_0_up()
    elif key == 1:
        actions.user.keypad_1_up()
    elif key == 2:
        actions.user.keypad_2_up()
    elif key == 3:
        actions.user.keypad_3_up()
    elif key == 4:
        actions.user.keypad_4_up()
    elif key == 5:
        actions.user.keypad_5_up()
    elif key == 6:
        actions.user.keypad_6_up()
    elif key == 7:
        actions.user.keypad_7_up()
    elif key == 8:
        actions.user.keypad_8_up()
    elif key == 9:
        actions.user.keypad_9_up()
    elif key == 10:
        actions.user.keypad_divide_up()
    elif key == 11:
        actions.user.keypad_multiply_up()
    elif key == 12:
        actions.user.keypad_minus_up()
    elif key == 13:
        actions.user.keypad_plus_up()
