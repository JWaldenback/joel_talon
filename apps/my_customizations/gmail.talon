tag: browser
browser.host: mail.google.com
#https://support.google.com/mail/answer/6594?hl=en&co=GENIE.Platform%3DDesktop
-
(chat | convo | thread | email) last: key(k)
(chat | convo | thread | email) next: key(j)
# Stepped through individual messages within an open conversation/thread (Gmail p/n).
# Disabled - inbox-list navigation above is enough.
#(comment | message) last: key(p)
#(comment | message) next: key(n)

go [to] inbox: 
    key(g)
    key(i)
go [to] starred: 
    key(g)
    key(s)
go [to] drafts: 
    key(g)
    key(d)
go [to] sent: 
    key(g)
    key(t)

#(comment | message | email) new: key(n)
(comment | message | email) flag: key(s)
report spam: key(!)
(comment | message | email) (delete | remove): key(#)
(comment | message | email) reply: key(r)
(comment | message | email) reply all: key(a)
(comment | message | email) forward: key(f)
(comment | message | email) send: key(ctrl-enter)
(undo | undo it | undo send): key(z)
#mark as read: key(q)
#mark as unread: key(u)

search: key(/)
#keyboard shortcuts: key()