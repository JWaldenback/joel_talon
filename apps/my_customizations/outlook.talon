tag: browser
browser.host: outlook.live.com
#https://support.microsoft.com/en-us/office/keyboard-shortcuts-for-outlook-3cdeb221-7ae5-4c1d-8c1d-9e63216c1efd?ui=en-us&rs=en-us&ad=us#PickTab=Web
-
#(conversation | convo | thread) last: key(k)
#(conversation | convo | thread) next: key(j)
#(comment | message | email) last: key(p)
#(comment | message | email) next: key(n)

go [to] inbox:
    key(g)
    key(i)
go [to] drafts:
    key(g)
    key(d)
go [to] sent:
    key(g)
    key(s)

(comment | message | email) new: key(n)
(comment | message | email) flag: key(insert)
report spam: key(j)
(comment | message | email) (delete | remove): key(delete)
(comment | message | email) reply: key(r)
(comment | message | email) reply all: key(ctrl-shift-r)
(comment | message | email) forward: key(ctrl-shift-f)
(comment | message | email) send: key(ctrl-enter)
(undo | undo it | undo send): edit.undo()
mark as read: key(q)
mark as unread: key(u)

draft discard: key(esc)

search: key(alt-q)
keyboard shortcuts: key(?)
