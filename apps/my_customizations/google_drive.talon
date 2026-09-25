tag: browser
browser.host: drive.google.com
-
#https://support.google.com/drive/answer/2563044?hl=en&co=GENIE.Platform%3DDesktop&oco=0

(document | doc) new: user.custom_app_shortcut("shift-t", "ctrl-c t")
(presentation | powerpoint) new: user.custom_app_shortcut("shift-p", "ctrl-c p")
spreadsheet new: user.custom_app_shortcut("shift-s", "ctrl-c s")
folder new: user.custom_app_shortcut("shift-f", "ctrl-c f")
form new: user.custom_app_shortcut("shift-o", "ctrl-c o")

#search: key(/)

(undo | undo it): user.custom_app_shortcut("ctrl-z", "cmd-z")
(redo | redo it): user.custom_app_shortcut("ctrl-shift-z", "cmd-y")

rename: user.custom_app_shortcut("ctrl-alt-n", "f2")

video (play | pause): key(k)
video (mute | unmute): key(m)
seek left: key(j)
seek right: key(l)
video fullscreen: key(f)

keyboard shortcuts: user.custom_app_shortcut("shift-/", "cmd-/")
