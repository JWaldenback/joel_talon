"""
Language-aware dictation router (Windows only, standalone).

Bound to a key in win_h_language_router.talon. When triggered:
  - If the foreground window's keyboard layout is REROUTE_LANGID
    (English by default), send REROUTE_KEY so a different dictation
    tool can be started.
  - For ALL other layouts (Swedish, German, etc.), send DEFAULT_KEY
    (Win+H by default) so Windows opens its native dictation pill.

This module is self-contained: no imports from other user modules. To
remove the feature, delete this folder entirely (both files), or just
delete/rename the .talon file to unbind the trigger key.

To change behavior, edit only the CONFIG block below. To change the
trigger key, edit win_h_language_router.talon.
"""

# ============================== CONFIG ===============================
# ONLY when the foreground window's keyboard layout matches this LANGID
# is REROUTE_KEY sent. Every other layout sends DEFAULT_KEY.
#   0x0409 = English (US)
#   0x041D = Swedish (sv-SE)
# Full list: https://learn.microsoft.com/openspecs/windows_protocols/ms-lcid/a9eac961-e77d-41a6-90a5-ce1a8b0cdb9c
REROUTE_LANGID = 0x0409

# Key sent ONLY when the foreground layout matches REROUTE_LANGID.
REROUTE_KEY = "ctrl-shift-h"

# Key sent for all other layouts.
# "super-h" opens Windows' native dictation pill.
DEFAULT_KEY = "super-h"

# Verbose console logging for debugging. Safe to leave on.
DEBUG = True
# =====================================================================


import ctypes
import ctypes.wintypes as wt

from talon import Module, actions, app

mod = Module()


_user32 = ctypes.WinDLL("user32", use_last_error=True) if app.platform == "windows" else None

if _user32 is not None:
    _user32.GetForegroundWindow.restype = wt.HWND
    _user32.GetWindowThreadProcessId.restype = wt.DWORD
    _user32.GetWindowThreadProcessId.argtypes = [wt.HWND, ctypes.POINTER(wt.DWORD)]
    _user32.GetKeyboardLayout.restype = wt.HKL
    _user32.GetKeyboardLayout.argtypes = [wt.DWORD]


def _log(msg: str):
    if DEBUG:
        print(f"[win_h_language_router] {msg}")


def _foreground_langid() -> int:
    if _user32 is None:
        return 0
    hwnd = _user32.GetForegroundWindow()
    if not hwnd:
        return 0
    tid = _user32.GetWindowThreadProcessId(hwnd, None)
    hkl = _user32.GetKeyboardLayout(tid)
    return hkl & 0xFFFF


@mod.action_class
class Actions:
    def lang_router_dictate():
        """Send REROUTE_KEY if foreground layout matches REROUTE_LANGID, otherwise DEFAULT_KEY."""
        lang_id = _foreground_langid()
        if lang_id == REROUTE_LANGID:
            _log(f"LANGID=0x{lang_id:04X} matches reroute; sending {REROUTE_KEY!r}")
            actions.key(REROUTE_KEY)
        else:
            _log(f"LANGID=0x{lang_id:04X} does not match reroute; sending {DEFAULT_KEY!r}")
            actions.key(DEFAULT_KEY)
