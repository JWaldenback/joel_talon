from talon import Module, actions

mod = Module()


@mod.action_class
class TabActions:
    def tab_jump(number: int):
        """Jumps to the specified tab"""
        if number < 9:
            if app.platform == "mac":
                actions.key(f"cmd-{number}")
            else:
                actions.key(f"ctrl-{number}")

    def tab_final():
        """Jumps to the final tab"""
        if app.platform == "mac":
            actions.key("cmd-9")
        else:
            actions.key("ctrl-9")

    def tab_close_wrapper():
        """Closes the current tab. Exists so that apps can implement their own delay before running tab_close() to handle repetitions better.
        """
        actions.sleep("180ms")
        actions.app.tab_close()

    def tab_duplicate():
        """Duplicates the current tab."""
        actions.browser.focus_address()
        actions.sleep("180ms")
        actions.key("alt-enter")

    def tab_left_wrapper():
        """Moves the current tab to the left."""
        actions.sleep("180ms")
        actions.key("ctrl-shift-pageup")

    def tab_right_wrapper():
        """Moves the current tab to the left."""
        actions.sleep("180ms")
        actions.key("ctrl-shift-pagedown")
