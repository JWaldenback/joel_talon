mode: user.power_mode
tag: user.tabs
-
tab (open | new): app.tab_open()
tab (last | previous): app.tab_previous()
tab next: app.tab_next()
tab (close | plus): user.tab_close_wrapper()
ten (close | plus): user.tab_close_wrapper()
tab (reopen | restore): app.tab_reopen()
tab <number>: user.tab_jump(number)
tab final: user.tab_final()
tab duplicate: user.tab_duplicate()
tab left: key(ctrl-shift-pageup)
tab right: key(ctrl-shift-pagedown)
