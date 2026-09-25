tag: browser
browser.host: gemini.google.com
-
(chat | convo | thread) new: user.gemini_new_chat()

[message] send: key(enter)
stop generating: key(escape)

focus input: user.gemini_shortcut("focus_input")
(sidebar | menu) toggle: user.gemini_shortcut("sidebar")
search: user.gemini_shortcut("search")
settings open: user.gemini_shortcut("settings")

response copy: user.gemini_shortcut("copy_response")

(chat | convo | thread) next: user.gemini_shortcut("next_chat")
(chat | convo | thread) last: user.gemini_shortcut("previous_chat")
