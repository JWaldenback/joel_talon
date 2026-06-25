from talon import Context, actions

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
