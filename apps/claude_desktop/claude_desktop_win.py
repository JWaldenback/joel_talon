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
