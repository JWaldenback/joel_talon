from talon import Context, Module, actions

mod = Module()
ctx = Context()

# "Claude for Windows" desktop chat app (claude.ai client).
# Talon scope reports app.name="Claude" and app.exe="claude.exe" for this
# Microsoft Store / UWP install. The Claude Code CLI wrapper is also
# named claude.exe but reports a different app.name, so combining the
# two keys uniquely identifies this app.
apps = mod.apps
apps.claude_desktop = r"""
os: windows
and app.name: Claude
and app.exe: /^claude\.exe$/i
"""

ctx.matches = r"""
app: claude_desktop
"""


# The message box is a chat input, not a text editor, so "insert a line
# below" should just be a soft newline (shift-enter). Talon resolves actions
# by context but voice commands have no precedence, so we override the action
# here; the global "new (line | row)" command in core/edit/edit.talon routes
# through it.
@ctx.action_class("edit")
class EditActions:
    def line_insert_down():
        actions.key("shift-enter")
