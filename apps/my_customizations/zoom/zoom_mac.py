from talon import Context, actions

ctx = Context()
ctx.matches = r"""
os: mac
app.bundle: us.zoom.xos
"""
ctx.tags = ["user.avc"]


@ctx.action_class("user")
class Actions:
    def avc_toggle_mute():
        actions.key('cmd-shift-a')

    def avc_toggle_video():
        actions.key('cmd-shift-v')

    def avc_toggle_screensharing():
        actions.key('cmd-shift-s')

    def avc_raise_hand():
        actions.key('alt-y')

    def avc_toggle_chat_window():
        actions.key('cmd-shift-h')

    def avc_toggle_participants():
        actions.key('cmd-u')

    def avc_increase_participants_tiles():
        actions.key('ctrl-p')

    def avc_decrease_participants_tiles():
        actions.key('ctrl-n')

    def avc_invite_participants():
        actions.key('cmd-i')

    def avc_leave_call():
        actions.app.window_close()

