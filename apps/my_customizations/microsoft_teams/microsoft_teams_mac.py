from talon import Context, actions

ctx = Context()
ctx.matches = r"""
os: mac
app.bundle: com.microsoft.teams
app.bundle: com.microsoft.teams2
"""
ctx.tags = ["user.avc"]


@ctx.action_class("user")
class Actions:
    def avc_toggle_mute():
        actions.key('cmd-shift-m')

    def avc_toggle_video():
        actions.key('cmd-shift-o')

    def avc_toggle_screensharing():
        actions.key('cmd-shift-e')

    def avc_raise_hand():
        actions.key('cmd-shift-k')

    def avc_push_to_talk():
        actions.key('alt-space')

    def avc_leave_call():
        actions.key('cmd-shift-h')

