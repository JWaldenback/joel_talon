control (on | mouse): tracking.control_toggle()
control off: user.mouse_sleep()
gaze on: tracking.control_gaze_toggle(true)
gaze off: tracking.control_gaze_toggle(false)
head on: tracking.control_head_toggle(true)
head off: tracking.control_head_toggle(false)
zoom (on | mouse | off): tracking.control_zoom_toggle()
camera overlay: tracking.control_debug_toggle()
run calibration: tracking.calibrate()

touch:
    # close zoom if open
    tracking.zoom_cancel()
    mouse_click(0)
    # close the mouse grid if open
    user.grid_close()
    # End any open drags
    # Touch automatically ends left drags so this is for right drags specifically
    user.mouse_drag_end()

righty:
    # close zoom if open
    tracking.zoom_cancel()
    mouse_click(1)
    # close the mouse grid if open
    user.grid_close()

mid click:
    # close zoom if open
    tracking.zoom_cancel()
    mouse_click(2)
    # close the mouse grid
    user.grid_close()

#see keys.py for modifiers.
#defaults
#command
#control
#option = alt
#shift
#super = windows key
<user.modifiers> touch:
    # close zoom if open
    tracking.zoom_cancel()
    key("{modifiers}:down")
    mouse_click(0)
    key("{modifiers}:up")
    # close the mouse grid
    user.grid_close()
<user.modifiers> righty:
    # close zoom if open
    tracking.zoom_cancel()
    key("{modifiers}:down")
    mouse_click(1)
    key("{modifiers}:up")
    # close the mouse grid
    user.grid_close()
dub click | duke:
    # close zoom if open
    tracking.zoom_cancel()
    mouse_click()
    mouse_click()
    # close the mouse grid
    user.grid_close()
trip click | trip lick:
    # close zoom if open
    tracking.zoom_cancel()
    mouse_click()
    mouse_click()
    mouse_click()
    # close the mouse grid
    user.grid_close()
left drag | drag | drag start:
    # close zoom if open
    tracking.zoom_cancel()
    user.mouse_drag(0)
    # close the mouse grid
    user.grid_close()
right drag | right drag start:
    # close zoom if open
    tracking.zoom_cancel()
    user.mouse_drag(1)
    # close the mouse grid
    user.grid_close()
end drag | drag end: user.mouse_drag_end()
downer: user.mouse_scroll_down()
downer here: user.mouse_scroll_down_no_rango()
downer center:
    user.mouse_move_center_active_window()
    user.mouse_scroll_down()
downer all: user.mouse_scroll_down(99)
downer here all: user.mouse_scroll_down_no_rango(99)
tiny down: user.mouse_scroll_down(0.2)
tiny down center:
    user.mouse_move_center_active_window()
    user.mouse_scroll_down(0.2)
downer (continuous | continue): user.mouse_scroll_down_continuous()
downer (continuous | continue) center:
    user.mouse_move_center_active_window()
    user.mouse_scroll_down_continuous()
upper: user.mouse_scroll_up()
upper here: user.mouse_scroll_up_no_rango()
upper center:
    user.mouse_move_center_active_window()
    user.mouse_scroll_up()
upper all: user.mouse_scroll_up(99)
upper here all: user.mouse_scroll_up_no_rango(99)
tiny up: user.mouse_scroll_up(0.2)
tiny up center:
    user.mouse_move_center_active_window()
    user.mouse_scroll_up(0.2)
upper (continuous | continue): user.mouse_scroll_up_continuous()
upper (continuous | continue) center:
    user.mouse_move_center_active_window()
    user.mouse_scroll_up_continuous()
wheel gaze: user.mouse_gaze_scroll()
wheel gaze center:
    user.mouse_move_center_active_window()
    user.mouse_gaze_scroll()
wheel left: user.mouse_scroll_left()
wheel left center:
    user.mouse_move_center_active_window()
    user.mouse_scroll_left()
wheel tiny left: user.mouse_scroll_left(0.5)
wheel tiny left center:
    user.mouse_move_center_active_window()
    user.mouse_scroll_left(0.5)
wheel right: user.mouse_scroll_right()
wheel right center:
    user.mouse_move_center_active_window()
    user.mouse_scroll_right()
wheel tiny right: user.mouse_scroll_right(0.5)
wheel tiny right center:
    user.mouse_move_center_active_window()
    user.mouse_scroll_right(0.5)
wheel {user.continuous_scrolling_direction}:
    user.mouse_scroll_continuous(continuous_scrolling_direction)
wheel {user.continuous_scrolling_direction} here:
    user.mouse_move_center_active_window()
    user.mouse_scroll_continuous(continuous_scrolling_direction)
wheel {user.continuous_scrolling_direction} <number_small>:
    user.mouse_scroll_continuous(continuous_scrolling_direction, number_small)
wheel {user.continuous_scrolling_direction} here <number_small>:
    user.mouse_move_center_active_window()
    user.mouse_scroll_continuous(continuous_scrolling_direction, number_small)
copy mouse position: user.copy_mouse_position()
# To scroll with a hiss sound, set mouse_enable_hiss_scroll to true in settings.talon
mouse hiss up: user.hiss_scroll_up()
mouse hiss down: user.hiss_scroll_down()