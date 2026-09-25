from talon import Context, Module, actions, app, settings

ctx = Context()
# Gemini's prompt box is a chat input, so "insert a line below" should be a
# soft newline (shift-enter). Overriding the action here lets the global
# new line / new row commands work on Gemini without submitting the prompt.
ctx.matches = r"""
tag: browser
browser.host: gemini.google.com
"""


@ctx.action_class("edit")
class EditActions:
    def line_insert_down():
        actions.key("shift-enter")


mod = Module()
# Gemini does not publish Mac equivalents for these custom Windows shortcuts.
# An empty setting keeps a guessed shortcut from triggering a browser command.
shortcuts = {
    "focus_input": "ctrl-/",
    "sidebar": "ctrl-shift-s",
    "search": "ctrl-shift-f",
    "settings": "ctrl-,",
    "copy_response": "ctrl-shift-c",
    "next_chat": "alt-down",
    "previous_chat": "alt-up",
}
for name in shortcuts:
    mod.setting(
        f"gemini_{name}_key",
        type=str,
        default="",
        desc=f"Verified Mac Gemini web shortcut for {name.replace('_', ' ')}",
    )


@mod.action_class
class GeminiActions:
    def gemini_new_chat():
        """Start a new Gemini conversation."""
        if app.platform == "mac":
            actions.browser.go("https://gemini.google.com/app")
        else:
            actions.key("ctrl-shift-o")

    def gemini_shortcut(name: str):
        """Run a Gemini shortcut, using an explicitly configured Mac binding."""
        shortcut = shortcuts[name]
        if app.platform == "mac":
            setting_name = f"user.gemini_{name}_key"
            shortcut = settings.get(setting_name)
            if not shortcut:
                actions.app.notify(f"Configure {setting_name} after checking Gemini's shortcuts")
                return
        actions.key(shortcut)
