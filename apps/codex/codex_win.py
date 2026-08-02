from talon import Context, Module, actions

mod = Module()
ctx = Context()

# OpenAI "Codex" desktop app (Electron/Chromium client; win.class is
# Chrome_WidgetWin_1). Talon scope reports app.name="Codex" and
# app.exe="Codex.exe". Match on both keys to stay specific in case a Codex
# CLI wrapper ever shares the exe name (as happens with claude.exe).
apps = mod.apps
apps.codex = r"""
os: windows
and app.name: Codex
and app.exe: /^codex\.exe$/i
"""

ctx.matches = r"""
app: codex
"""


# The prompt box is a chat input, not a text editor, so "insert a line below"
# should be a soft newline (shift-enter). The global "new (line | row)" command
# in core/edit/edit.talon routes through edit.line_insert_down, so overriding it
# here keeps that command from submitting the prompt.
@ctx.action_class("edit")
class EditActions:
    def line_insert_down():
        actions.key("shift-enter")
