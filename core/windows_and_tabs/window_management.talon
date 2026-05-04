window (new | open): app.window_open()
window next: app.window_next()
window (last | back | previous): app.window_previous()
window close: app.window_close()
window (hide | minimize): app.window_hide()
app (preferences | prefs | settings): app.preferences()
focus <number>: user.window_jump(number)
focus <user.running_applications>: user.switcher_focus(running_applications)
# following only works on windows. Can't figure out how to make it work for mac. No idea what the equivalent for linux would be.
focus$: user.switcher_menu()
focus last: user.switcher_focus_last()
running list: user.switcher_toggle_running()
running [list] close: user.switcher_hide_running()
launch <user.launch_applications>: user.switcher_launch(launch_applications)

#`window` could potentially also work as a command for the snap feature. Although it could clash with window close, window hide and so on...
(snap | move) <user.window_snap_position>: user.snap_window(window_snap_position)
(snap | move) next [screen]: user.move_window_next_screen()
(snap | move) (last | back | previous) [screen]: user.move_window_previous_screen()
(snap | move) screen <number>: user.move_window_to_screen(number)
(snap | move) <user.running_applications> <user.window_snap_position>:
    user.snap_app(running_applications, window_snap_position)
(snap | move)  <user.running_applications> [screen] <number>:
    user.move_app_to_screen(running_applications, number)
