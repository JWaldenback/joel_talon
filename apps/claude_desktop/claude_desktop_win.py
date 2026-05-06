from talon import Context, Module, actions

mod = Module()
ctx = Context()

# "Claude for Windows" desktop chat app (claude.ai client),
# installed via the Microsoft Store under \WindowsApps\Claude_*.
# Note: the Claude Code CLI wrapper at AppData\Roaming\Claude\claude-code\
# is also named claude.exe, so we disambiguate by path.
apps = mod.apps
apps.claude_desktop = r"""
os: windows
and app.exe: /^claude\.exe$/i
and app.path: /WindowsApps[\\/]Claude_/i
os: windows
and win.title: /^Claude$/
"""

ctx.matches = r"""
app: claude_desktop
"""
