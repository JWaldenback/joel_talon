from talon import Context, actions

ctx = Context()
ctx.matches = r"""
os: mac
tag: browser
browser.host: meet.google.com
"""
ctx.tags = ["user.avc"]


@ctx.action_class("user")
class Actions:
    def avc_toggle_mute():
        actions.key('cmd-d')

    def avc_toggle_video():
        actions.key('cmd-e')

    def avc_raise_hand():
        actions.key('ctrl-cmd-h')

    def avc_toggle_chat_window():
        actions.key('ctrl-cmd-c')

    def avc_toggle_participants():
        actions.key('ctrl-cmd-p')

    def avc_increase_participants_tiles():
        actions.key('ctrl-cmd-k')

    def avc_decrease_participants_tiles():
        actions.key('ctrl-cmd-j')

    def avc_keyboard_shortcuts():
        actions.key('shift-?')

    def avc_leave_call():
        actions.app.tab_close()

