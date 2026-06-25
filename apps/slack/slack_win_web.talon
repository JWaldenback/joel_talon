os: windows
os: linux
tag: browser
browser.host: app.slack.com
-
tag(): user.messaging
tag(): user.emoji
# Workspaces
workspace <number>: key("ctrl-{number}")
workspace next: app.notify("Command not available")
workspace (last | back | previous): app.notify("Command not available")
# Channel
#(slack | lack | like) [channel] info: key(ctrl-shift-i)
# Navigation
#focus (move | next): key(ctrl-`)
(go [to] | section | zone) next: key(f6)
(go [to] | section | zone) (previous | last): key(shift-f6)
go [to] messages: key(ctrl-shift-k)
go [to] threads: app.notify("Command not available")
go (next | forth): key("alt-right")
go (last | back | previous): key("alt-left")
element next: key(tab)
element (last | back | previous): key(shift-tab)
go [to] mentions [and reactions]: app.notify("Command not available")
go [to] people [and user groups]: key(ctrl-shift-e)
go [to] (saved | later): app.notify("Command not available")
go [to] (unread | unreads): key(ctrl-shift-a)
mark [messages] as read: key(esc)
mark all [messages] [as] read: key(shift-esc)
go [to] channels: key(ctrl-shift-l)
go [to] search: app.notify("Command not available")
go [to] unread next: key(alt-shift-down)
# Messaging
go up: key(up)
go down: key(down)
#grab left: key(shift-up)
#grab right: key(shift-down)
edit (message | last): key(ctrl-up)
message edit: key(ctrl-up)
message send: key(enter)
#add line: key(shift-enter)
(format command | [format] commandify): key(ctrl-shift-c)
(format code | [format] codify): key(ctrl-alt-shift-c)
[format] (bullet | bulleted) list: key(ctrl-shift-8)
[format] (number | numbered) list: key(ctrl-shift-7)
(format quotes | format quotation | [format] quotify): key(ctrl-shift-9)
(format bold | [format] boldify): key(ctrl-b)
(format italic | [format] italify): key(ctrl-i)
(format strike | format strikethrough | [format] strikify): key(ctrl-shift-x)
(format link | [format] linkify): key(ctrl-shift-u)
[format] snippet: key(ctrl-shift-enter)
formatting apply: key(ctrl-shift-f)
#formatting (clear | remove): key(ctrl-z)

# Calls
(huddle | call) (new | join): 
    key(ctrl-shift-h)
    sleep(200ms)
    key(scroll_lock)
(huddle | call) close: key(ctrl-shift-h)
#toggle (mute | unmute): key(m)
#toggle video: key(v)
#invite people: key(a)
# Miscellaneous
keyboard shortcuts: key(ctrl-/)
#emote <user.text>: "{text}"
left (sidebar | menu) toggle: key(ctrl-shift-d)
right (sidebar | menu) toggle: key(ctrl-.)

go [to] messages <phrase>$: app.notify("Command not available")

go [to] channel <phrase>$: app.notify("Command not available")