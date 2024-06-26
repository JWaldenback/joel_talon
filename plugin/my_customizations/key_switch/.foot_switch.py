import time
from talon import Module, Context, actions, cron

mod = Module()
mod.tag("av")

current_state = [False, False, False, False]
last_state = [False, False, False, False]
continuous_firing = [True, False, False, False]
has_fired = [False, False, False, False]
timestamps = [0, 0, 0, 0]
scroll_reversed = False
hold_timeout = 0.2


#the original implementation
# def on_interval():
#     for key in range(4):
#         if current_state[key] != last_state[key]:
#             last_state[key] = current_state[key]
#             # Key is pressed down
#             if current_state[key]:
#                 call_down(key)
#             # Key is released after specified hold time out. ie key was held.
#             elif time.perf_counter() - timestamps[key] > hold_timeout:
#                 call_up(key)


#fires call down and call up only once
# def on_interval():
#     for key in range(4):
#         if current_state[key] != last_state[key]:
#             last_state[key] = current_state[key]
#             # Key is pressed down
#             if current_state[key]:
#                 call_down(key)
#             # Key is released
#             else:
#                 last_state[key] = current_state[key]
#                 call_up(key)


# #fires continuously and then calls call_up only once
# def on_interval():
#     for key in range(4):
#         # Key is pressed down
#         if current_state[key]:
#             last_state[key] = True
#             call_down(key)
#         # Key is released
#         elif (current_state[key] == False) and (last_state[key] == True):
#             last_state[key] = False
#             call_up(key)


#fires continuously if continuous_firing is set to true and then calls call_up only once
def on_interval():
    for key in range(4):
        # Key is pressed down
        if (current_state[key]) and (continuous_firing[key] == False) and (has_fired[key] == False):
            last_state[key] = True
            has_fired[key] = True
            call_down(key)
        elif (current_state[key]) and (continuous_firing[key] == True):
            last_state[key] = True
            call_down(key)
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


cron.interval("100ms", on_interval)


@mod.action_class
class Actions:
    def foot_switch_down(key: int):
        """Foot switch key down event. Top(0), Center(1), Left(2), Right(3)"""
        timestamps[key] = time.perf_counter()
        current_state[key] = True

    def foot_switch_up(key: int):
        """Foot switch key up event. Top(0), Center(1), Left(2), Right(3)"""
        current_state[key] = False

    def foot_switch_scroll_reverse():
        """Reverse scroll direction using foot switch"""
        global scroll_reversed
        scroll_reversed = not scroll_reversed

    def foot_switch_top_down():
        """Foot switch button top:down"""

    def foot_switch_top_up():
        """Foot switch button top:up"""

    def foot_switch_center_down():
        """Foot switch button center:down"""

    def foot_switch_center_up():
        """Foot switch button center:up"""

    def foot_switch_left_down():
        """Foot switch button left:down"""

    def foot_switch_left_up():
        """Foot switch button left:up"""

    def foot_switch_right_down():
        """Foot switch button right:down"""

    def foot_switch_right_up():
        """Foot switch button right:up"""


# Default implementation
ctx = Context()


@ctx.action_class("user")
class UserActions:
    def foot_switch_top_down():
        actions.user.mouse_scroll_up()

    def foot_switch_top_up():
        #testing, Ask Andreas why this doesn't work
        actions.user.play_pause()
        actions.user.stop_scroll()

    def foot_switch_center_down():
        actions.user.mouse_scroll_down()

    def foot_switch_center_up():
        actions.user.stop_scroll()

    def foot_switch_left_down():
        actions.user.go_back()

    def foot_switch_left_up():
        pass

    def foot_switch_right_down():
        actions.core.repeat_command(1)

    def foot_switch_right_up():
        pass


# Audio / Video conferencing
ctx_av = Context()
ctx_av.matches = r"""
tag: user.av
"""


@ctx_av.action_class("user")
class AvActions:
    def foot_switch_right_down():
        actions.user.mute_microphone()

    def foot_switch_right_up():
        actions.user.mute_microphone()


# Mouse zoom mode
ctx_zoom = Context()
ctx_zoom.matches = r"""
tag: user.zoom_mouse
"""


@ctx_zoom.action_class("user")
class ZoomActions:
    def foot_switch_top_down():
        actions.user.zoom_mouse_click("triple")

    def foot_switch_center_down():
        actions.user.zoom_mouse_click("middle")

    def foot_switch_left_down():
        actions.user.zoom_mouse_click("double")

    def foot_switch_right_down():
        actions.user.zoom_mouse_click("right")

    def foot_switch_top_up():
        pass

    def foot_switch_center_up():
        pass

    def foot_switch_left_up():
        pass

    def foot_switch_right_up():
        pass


def call_down(key: int):
    # Top
    if key == 0:
        actions.user.foot_switch_top_down()
    # Center
    elif key == 1:
        actions.user.foot_switch_center_down()
    # Left
    elif key == 2:
        actions.user.foot_switch_left_down()
    # Right
    elif key == 3:
        actions.user.foot_switch_right_down()


def call_up(key: int):
    # Top
    if key == 0:
        actions.user.foot_switch_top_up()
    # Center
    elif key == 1:
        actions.user.foot_switch_center_up()
    # Left
    elif key == 2:
        actions.user.foot_switch_left_up()
    # Right
    elif key == 3:
        actions.user.foot_switch_right_up()
