from talon import Module, actions, app

mod = Module()


@mod.action_class
class Actions:
    def custom_app_shortcut(windows: str, mac: str):
        """Send an explicitly mapped application shortcut for the current platform."""
        shortcut = mac if app.platform == "mac" else windows
        if not shortcut:
            raise NotImplementedError("This application shortcut is not configured on this platform")
        actions.key(shortcut)
