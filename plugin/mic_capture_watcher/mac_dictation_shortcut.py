"""Resolve the user's configured Dictation shortcut without changing it."""

import plistlib
from pathlib import Path

_MODIFIERS = ((1 << 17, "shift"), (1 << 18, "ctrl"), (1 << 19, "alt"), (1 << 20, "cmd"), (1 << 23, "fn"))
_SPECIAL_KEYS = {36: "enter", 48: "tab", 49: "space", 51: "backspace", 53: "escape", 63: "fn"}


def dictation_shortcut(override="", path=None):
    if override.strip():
        return override.split()
    path = path or Path.home() / "Library/Preferences/com.apple.symbolichotkeys.plist"
    with open(path, "rb") as stream:
        hotkey = plistlib.load(stream).get("AppleSymbolicHotKeys", {}).get("164", {})
    if not hotkey.get("enabled"):
        raise ValueError("Enable a macOS Dictation shortcut, or set user.mac_dictation_shortcut")
    value = hotkey.get("value", {})
    params = value.get("parameters", [])
    if value.get("type") == "modifier" and params:
        matches = [name for bit, name in _MODIFIERS if params[0] == bit]
        if matches:
            return matches * 2
    if value.get("type") == "standard" and len(params) >= 3:
        character, keycode, mask = params[:3]
        key = _SPECIAL_KEYS.get(keycode)
        if key is None and isinstance(character, int) and 32 < character < 127:
            key = chr(character).lower()
            key = {"-": "minus", "=": "equal"}.get(key, key)
        if key:
            modifiers = [name for bit, name in _MODIFIERS if mask & bit]
            return ["-".join([*modifiers, key])]
    raise ValueError("Dictation shortcut could not be read; set user.mac_dictation_shortcut to its Talon key sequence")
