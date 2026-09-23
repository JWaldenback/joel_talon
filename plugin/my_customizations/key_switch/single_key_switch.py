import threading
import time
from talon import Module, Context, actions, cron

mod = Module()

current_state = [False]
last_state = [False]
continuous_firing = [False]
# Presses seen by key_down that on_interval hasn't handled yet. Key events and
# the cron tick run on different threads, hence the lock.
pending_presses = [0]
_press_lock = threading.Lock()


#fires call down and call up only once
# def on_interval():
#     for key in range(4):
#         if current_state[key] != last_state[key]:
#             last_state[key] = current_state[key]
#             # Key is pressed downi
#             if current_state[key]:
#                 call_down(key)
#             # Key is released
#             else:
#                 last_state[key] = current_state[key]
#                 call_up(key)


#fires continuously if continuous_firing is set to true and then calls call_up() once when the key is released

def on_interval():
    for key in range(1):
        # Grab and reset the presses latched by key_down since the last tick,
        # so a tap whose down+up both land between two ticks isn't lost.
        # Same approach as numpad_switch.py.
        with _press_lock:
            presses = pending_presses[key]
            pending_presses[key] = 0
        held = current_state[key]
        if continuous_firing[key]:
            if held or presses:
                last_state[key] = True
                call_down(key)
                actions.sleep("100ms")
        else:
            # One call_down per press; close earlier queued presses with a
            # call_up so fast repeated taps aren't collapsed into one.
            for _ in range(presses):
                if last_state[key]:
                    call_up(key)
                call_down(key)
                last_state[key] = True
        # Key is released
        if not held and last_state[key]:
            last_state[key] = False
            call_up(key)


cron.interval("10ms", on_interval)


@mod.action_class
class Actions:
    def set_flag(value: int):
        """sdf"""

    def key_down(key: int):
        """Key down event"""
        with _press_lock:
            # Only count the up→down transition so key auto-repeat while
            # holding doesn't register as extra presses.
            if not current_state[key]:
                pending_presses[key] += 1
            current_state[key] = True

    def key_up(key: int):
        """Key up event"""
        current_state[key] = False
    
    def key_selected_down():
        """sdf"""

    def key_selected_up():
        """sdf"""


# Default implementation
ctx = Context()

#test actions
#actions.user.play_pause()

flag = 0
@ctx.action_class("user")
class UserActions:

    def set_flag(value: int):
        global flag 
        flag = value

    def key_selected_down():
        if flag:
            actions.core.repeat_command(1)
        else:
            actions.core.repeat_phrase(1)

    def key_selected_up():
        pass


def call_down(key: int):
    if key == 0:
        actions.user.key_selected_down()


def call_up(key: int):
    if key == 0:
        actions.user.key_selected_up()

   