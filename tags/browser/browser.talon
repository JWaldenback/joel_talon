tag: browser
-

tag(): user.address
tag(): user.find
tag(): user.navigation

go page | page focus: browser.focus_page()
address copy | url copy | copy address | copy url:
    browser.focus_address()
    sleep(50ms)
    edit.copy()
    user.hud_add_log('success', 'Content copied')
#go home: browser.go_home()
go [to] {user.website}: browser.go(website)
(incognito | private) (new | open): browser.open_private_window()

go (next | forth): browser.go_forward()
go (last | back | previous): browser.go_back()

bookmark it: browser.bookmark()
#bookmark tabs: browser.bookmark_tabs()
(refresh | reload) it: browser.reload()
(refresh | reload) it hard: browser.reload_hard()
tab (refresh | reload): browser.reload()
tab (refresh | reload) hard: browser.reload_hard()

bookmarks (new | open): browser.bookmarks()
#bookmarks bar (new | open): browser.bookmarks_bar()
downloads (new | open): browser.show_downloads()
(extensions | plugins) (new | open): browser.show_extensions()
history (new | open): browser.show_history()
cache (new | open): browser.show_clear_cache()
dev tools (new | open): browser.toggle_dev_tools()