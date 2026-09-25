from talon import Context, actions

ctx = Context()
ctx.matches = "os: mac"


def system_event(command):
    # Import only when invoked on macOS; other platforms still load this module.
    from talon.mac import applescript

    applescript.run(f'tell application "System Events" to {command}')


@ctx.action_class("user")
class MacSystemActions:
    def system_shutdown():
        system_event("shut down")

    def system_restart():
        system_event("restart")

    def system_hibernate():
        # macOS manages safe sleep itself; the user-facing equivalent is sleep.
        system_event("sleep")

    def system_lock():
        actions.key("ctrl-cmd-q")
