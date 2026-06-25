# Adds a `scope copy` command that copies the full current Talon scope
# (modes, tags, and misc keys like app/browser.host/win.title) to the
# clipboard. The built-in `help scope` GUI (core/help/help_scope.py) only
# displays the scope and truncates long values; this rebuilds the same
# content untruncated so it can be pasted elsewhere.

from typing import Optional

from talon import Module, actions, clip, scope

mod = Module()


def _format_value(value):
    # Mirror the help_scope GUI's formatting for lists/sets, but never truncate.
    if isinstance(value, (list, set)):
        return ", ".join(sorted(str(v) for v in value))
    return value


def _collect(path: str, value, ignore: Optional[set] = None) -> list[str]:
    """Flatten a (possibly nested) scope value into "path: value" lines."""
    lines: list[str] = []
    if isinstance(value, dict):
        ignore = ignore or set()
        for key in value:
            if key not in ignore:
                child_path = f"{path}.{key}" if path else key
                lines.extend(_collect(child_path, value[key]))
    elif value:
        lines.append(f"{path}: {_format_value(value)}")
    return lines


@mod.action_class
class Actions:
    def help_scope_copy():
        """Copy the current Talon scope (modes, tags, misc) to the clipboard"""
        lines: list[str] = ["Modes"]
        lines += [f"  {mode}" for mode in sorted(scope.get("mode"))]
        lines += ["", "Tags"]
        lines += [f"  {tag}" for tag in sorted(scope.get("tag"))]
        lines += ["", "Misc"]

        # Same key set the help_scope GUI iterates over.
        ignore = {"main", "mode", "tag"}
        keys = {*scope.data.keys(), *scope.data["main"].keys()}
        for key in sorted(keys):
            if key not in ignore:
                lines += [f"  {line}" for line in _collect(key, scope.get(key))]

        clip.set_text("\n".join(lines))
        actions.app.notify("Scope copied to clipboard")
