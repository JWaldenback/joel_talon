app: claude_desktop
-

# Conversations
chat new: key(ctrl-n)
conversation new: key(ctrl-n)

# Sidebar / navigation
sidebar toggle: key(ctrl-b)
search chats: key(ctrl-k)
command bar: key(ctrl-k)

# Submission / cancellation
message send: key(enter)
message cancel: key(esc)
stop it: key(esc)

# Slash commands (free dictation + go variant)
slash <user.text>$:
    insert("/{text}")
slash <user.text> go:
    insert("/{text}")
    key(enter)

# App
open settings: key(ctrl-comma)
shortcuts help: key(ctrl-/)
zoom in: key(ctrl-=)
zoom out: key(ctrl--)
zoom reset: key(ctrl-0)
