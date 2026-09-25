app.exe: /WINWORD.EXE/
app.name: /Microsoft Word/
-
[format] normal text: user.custom_app_shortcut("ctrl-alt-n", "cmd-shift-n")
[format] heading one: user.custom_app_shortcut("ctrl-alt-1", "cmd-alt-1")
[format] heading two: user.custom_app_shortcut("ctrl-alt-2", "cmd-alt-2")
[format] heading three: user.custom_app_shortcut("ctrl-alt-3", "cmd-alt-3")
#[format] heading four: key(ctrl-alt-4)
#[format] heading five: key(ctrl-alt-5)

[format] (bullet | bulleted) list: user.custom_app_shortcut("ctrl-shift-l", "cmd-shift-l")
#[format] (number | numbered) list: key(ctrl-shift-7)
(format bold | [format] boldify): user.custom_app_shortcut("ctrl-b", "cmd-b")
(format italic | [format] italify): user.custom_app_shortcut("ctrl-i", "cmd-i")
(format underline | [format] underlinify): user.custom_app_shortcut("ctrl-u", "cmd-u")
(format strike | format strikethrough | [format] strikify): user.custom_app_shortcut("alt-shift-5", "cmd-shift-x")
(format link | [format] linkify): user.custom_app_shortcut("ctrl-k", "cmd-k")

#spelling [and grammar]: key(f7)
#spelling next: key(ctrl-')
#spelling last: key(ctrl-;)

#formatting (clear | remove): key(ctrl-shift-n)
formatting (clear | remove): user.custom_app_shortcut("ctrl-space", "ctrl-space")

#keyboard shortcuts: key(ctrl-/)
