tag: browser
browser.host: docs.google.com
-
#https://support.google.com/docs/answer/179738?hl=en&co=GENIE.Platform%3DDesktop#zippy=%2Cpc-shortcuts

#Voice typing:
#https://support.google.com/docs/answer/4492226?hl=en
#To stop voice typing, say "Stop listening."

#tag(): user.native_dictation

[format] normal text: user.custom_app_shortcut("ctrl-alt-0", "cmd-alt-0")
[format] heading one: user.custom_app_shortcut("ctrl-alt-1", "cmd-alt-1")
[format] heading two: user.custom_app_shortcut("ctrl-alt-2", "cmd-alt-2")
[format] heading three: user.custom_app_shortcut("ctrl-alt-3", "cmd-alt-3")
[format] heading four: user.custom_app_shortcut("ctrl-alt-4", "cmd-alt-4")
[format] heading five: user.custom_app_shortcut("ctrl-alt-5", "cmd-alt-5")

[format] (bullet | bulleted) list: user.custom_app_shortcut("ctrl-shift-8", "cmd-shift-8")
[format] (number | numbered) list: user.custom_app_shortcut("ctrl-shift-7", "cmd-shift-7")
(format bold | [format] boldify): user.custom_app_shortcut("ctrl-b", "cmd-b")
(format italic | [format] italify): user.custom_app_shortcut("ctrl-i", "cmd-i")
(format underline | [format] underlinify): user.custom_app_shortcut("ctrl-u", "cmd-u")
(format strike | format strikethrough | [format] strikify): user.custom_app_shortcut("alt-shift-5", "cmd-shift-x")
(format link | [format] linkify): user.custom_app_shortcut("ctrl-k", "cmd-k")

spelling [and grammar]: user.custom_app_shortcut("f7", "cmd-alt-x")
#spelling next: key(ctrl-')
#spelling last: key(ctrl-;)

#formatting (clear | remove): key(ctrl-\)

#keyboard shortcuts: key(ctrl-/)
