tag: user.tabs
-
#tab back is used by Rango
tab (new | open): app.tab_open()
tab (last | previous | left): app.tab_previous()
tab (next | right): app.tab_next()
tab (close | plus): user.tab_close_wrapper()
ten (close | plus): user.tab_close_wrapper()
tab (reopen | restore): app.tab_reopen()
tab <number>: user.tab_jump(number)
tab final: user.tab_final()
tab (duplicate | clone): user.tab_duplicate()

tab move left: user.tab_left_wrapper()
tab move right: user.tab_right_wrapper()

