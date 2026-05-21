"""
Language-aware dictation router (Windows only, standalone).

Bound to a key in win_h_language_router.talon. When triggered:
  - If the foreground window's keyboard layout is PASSTHROUGH_LANGID
    (Swedish by default), send WIN_LANG_KEY (Win+H) so Windows opens
    its native dictation pill.
  - Otherwise, send REROUTE_KEY (Ctrl+Space by default) to start a
    different dictation tool.

This module is self-contained: no imports from other user modules. To
remove the feature, delete this folder entirely (both files), or just
delete/rename the .talon file to unbind the trigger key.

To change behavior, edit only the CONFIG block below. To change the
trigger key, edit win_h_language_router.talon.
"""

# ============================== CONFIG ===============================
# When the foreground window's keyboard layout matches this LANGID,
# WIN_LANG_KEY is sent. Otherwise REROUTE_KEY is sent.
#   0x041D = Swedish (sv-SE)
#   0x0409 = English (US)
# Full list: https://learn.microsoft.com/openspecs/windows_protocols/ms-lcid/a9eac961-e77d-41a6-90a5-ce1a8b0cdb9c
PASSTHROUGH_LANGID = 0x041D

# Key sent when the foreground layout matches PASSTHROUGH_LANGID.
# "super-h" opens Windows' native dictation pill.
WIN_LANG_KEY = "super-h"

# Key sent when the foreground layout does NOT match PASSTHROUGH_LANGID.
REROUTE_KEY = "ctrl-shift-j"

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
        """Send WIN_LANG_KEY or REROUTE_KEY depending on foreground keyboard layout."""
        lang_id = _foreground_langid()
        if lang_id == PASSTHROUGH_LANGID:
            _log(f"LANGID=0x{lang_id:04X} matches passthrough; sending {WIN_LANG_KEY!r}")
            actions.key(WIN_LANG_KEY)
        else:
            _log(f"LANGID=0x{lang_id:04X} does not match passthrough; sending {REROUTE_KEY!r}")
            actions.key(REROUTE_KEY)
