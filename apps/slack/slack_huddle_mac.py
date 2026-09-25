from talon import Context, actions

ctx = Context()
ctx.matches = r"""
os: mac
app: slack
win.title: /Huddle/i
"""
ctx.tags = ["user.avc"]


@ctx.action_class("user")
class Actions:
    def avc_toggle_mute():
        actions.key('cmd-shift-space')

    def avc_leave_call():
        actions.key('cmd-shift-h')

    def avc_keyboard_shortcuts():
        actions.key('cmd-/')

    def avc_toggle_video():
        actions.user.toggle_dictation_key_switch()

