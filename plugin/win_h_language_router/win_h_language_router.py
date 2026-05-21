"""
Win+H language router (Windows only, standalone).

When the user presses Win+H:
  - If the foreground window's keyboard layout is the PASSTHROUGH language
    (Swedish by default), let Win+H reach Windows so its native dictation
    pill opens normally.
  - Otherwise, suppress Win+H and inject REROUTE_KEY (Ctrl+Space by default)
    so a different dictation tool can be started instead.

This module is self-contained: it installs its own low-level keyboard hook
and does not import from other user modules. To remove the feature, set
ENABLED = False below, or delete this folder entirely.

To change behavior, edit only the CONFIG block.
"""

# ============================== CONFIG ===============================
# Master switch. Set to False to disable without deleting the file.
ENABLED = True

# Virtual-key code of the trigger key (the non-modifier part of the
# shortcut you're catching). 0x48 = 'H'. Reference:
# https://learn.microsoft.com/windows/win32/inputdev/virtual-key-codes
TRIGGER_VK = 0x48

# Which modifier(s) must be held for the trigger to fire.
# Set any of these to False if you don't want to require that modifier.
REQUIRE_WIN = True
REQUIRE_CTRL = False
REQUIRE_ALT = False
REQUIRE_SHIFT = False

# When the foreground window's keyboard layout matches this LANGID, the
# trigger is passed through to Windows unchanged. Otherwise, the trigger
# is suppressed and REROUTE_KEY is injected instead.
#   0x041D = Swedish (sv-SE)
#   0x0409 = English (US)
# Full list: https://learn.microsoft.com/openspecs/windows_protocols/ms-lcid/a9eac961-e77d-41a6-90a5-ce1a8b0cdb9c
PASSTHROUGH_LANGID = 0x041D

# Talon key spec injected when the trigger is rerouted.
# Examples: "ctrl-space", "ctrl-shift-d", "f13".
REROUTE_KEY = "ctrl-space"

# Verbose console logging for debugging. Safe to leave on.
DEBUG = True
# =====================================================================


import ctypes
import ctypes.wintypes as wt
import threading

from talon import Module, actions, app, cron

mod = Module()

WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
WM_SYSKEYDOWN = 0x0104
WM_SYSKEYUP = 0x0105
WM_QUIT = 0x0012
LLKHF_INJECTED = 0x10
LLKHF_LOWER_IL_INJECTED = 0x02

VK_LWIN = 0x5B
VK_RWIN = 0x5C
VK_LCONTROL = 0xA2
VK_RCONTROL = 0xA3
VK_LMENU = 0xA4   # left Alt
VK_RMENU = 0xA5   # right Alt
VK_LSHIFT = 0xA0
VK_RSHIFT = 0xA1

LowLevelKeyboardProc = ctypes.WINFUNCTYPE(
    ctypes.c_long, ctypes.c_int, wt.WPARAM, wt.LPARAM
)


class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("vkCode", wt.DWORD),
        ("scanCode", wt.DWORD),
        ("flags", wt.DWORD),
        ("time", wt.DWORD),
        ("dwExtraInfo", ctypes.c_void_p),
    ]


_user32 = ctypes.WinDLL("user32", use_last_error=True) if app.platform == "windows" else None
_kernel32 = ctypes.WinDLL("kernel32", use_last_error=True) if app.platform == "windows" else None

if _user32 is not None:
    _user32.SetWindowsHookExW.restype = wt.HHOOK
    _user32.SetWindowsHookExW.argtypes = [
        ctypes.c_int, LowLevelKeyboardProc, wt.HINSTANCE, wt.DWORD,
    ]
    _user32.CallNextHookEx.restype = wt.LPARAM
    _user32.CallNextHookEx.argtypes = [wt.HHOOK, ctypes.c_int, wt.WPARAM, wt.LPARAM]
    _user32.UnhookWindowsHookEx.restype = wt.BOOL
    _user32.UnhookWindowsHookEx.argtypes = [wt.HHOOK]
    _user32.GetMessageW.argtypes = [
        ctypes.POINTER(wt.MSG), wt.HWND, wt.UINT, wt.UINT,
    ]
    _user32.PostThreadMessageW.argtypes = [
        wt.DWORD, wt.UINT, wt.WPARAM, wt.LPARAM,
    ]
    _user32.GetForegroundWindow.restype = wt.HWND
    _user32.GetWindowThreadProcessId.restype = wt.DWORD
    _user32.GetWindowThreadProcessId.argtypes = [wt.HWND, ctypes.POINTER(wt.DWORD)]
    _user32.GetKeyboardLayout.restype = wt.HKL
    _user32.GetKeyboardLayout.argtypes = [wt.DWORD]
    _user32.GetAsyncKeyState.restype = ctypes.c_short
    _user32.GetAsyncKeyState.argtypes = [ctypes.c_int]


_state = {
    "hook": None,
    "thread": None,
    "thread_id": None,
    "proc": None,
    "suppress_trigger_keyup": False,
}


def _log(msg: str):
    if DEBUG:
        print(f"[win_h_language_router] {msg}")


def _key_down(vk: int) -> bool:
    return bool(_user32.GetAsyncKeyState(vk) & 0x8000)


def _modifiers_match() -> bool:
    win = _key_down(VK_LWIN) or _key_down(VK_RWIN)
    ctrl = _key_down(VK_LCONTROL) or _key_down(VK_RCONTROL)
    alt = _key_down(VK_LMENU) or _key_down(VK_RMENU)
    shift = _key_down(VK_LSHIFT) or _key_down(VK_RSHIFT)
    if REQUIRE_WIN and not win:
        return False
    if REQUIRE_CTRL and not ctrl:
        return False
    if REQUIRE_ALT and not alt:
        return False
    if REQUIRE_SHIFT and not shift:
        return False
    return True


def _foreground_langid() -> int:
    hwnd = _user32.GetForegroundWindow()
    if not hwnd:
        return 0
    tid = _user32.GetWindowThreadProcessId(hwnd, None)
    hkl = _user32.GetKeyboardLayout(tid)
    return hkl & 0xFFFF


def _do_reroute():
    # Release any held modifiers from the original shortcut so the injected
    # key spec isn't interpreted as a combo with them (e.g. Win+Ctrl+Space
    # is the Windows language switcher, which is not what we want).
    try:
        if REQUIRE_WIN:
            actions.key("super:up")
        if REQUIRE_CTRL:
            actions.key("ctrl:up")
        if REQUIRE_ALT:
            actions.key("alt:up")
        if REQUIRE_SHIFT:
            actions.key("shift:up")
        actions.key(REROUTE_KEY)
        _log(f"rerouted to {REROUTE_KEY!r}")
    except Exception as e:
        print(f"[win_h_language_router] reroute failed: {e}")


def _hook_proc(nCode, wParam, lParam):
    if nCode == 0 and ENABLED:
        kbd = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT))[0]
        injected = bool(kbd.flags & (LLKHF_INJECTED | LLKHF_LOWER_IL_INJECTED))

        if not injected and kbd.vkCode == TRIGGER_VK:
            if wParam in (WM_KEYDOWN, WM_SYSKEYDOWN):
                if _modifiers_match():
                    lang_id = _foreground_langid()
                    _log(f"trigger pressed; foreground LANGID=0x{lang_id:04X}")
                    if lang_id != PASSTHROUGH_LANGID:
                        _state["suppress_trigger_keyup"] = True
                        cron.after("0ms", _do_reroute)
                        return 1
            elif wParam in (WM_KEYUP, WM_SYSKEYUP):
                if _state["suppress_trigger_keyup"]:
                    _state["suppress_trigger_keyup"] = False
                    return 1

    return _user32.CallNextHookEx(_state["hook"] or 0, nCode, wParam, lParam)


def _hook_thread():
    proc = LowLevelKeyboardProc(_hook_proc)
    _state["proc"] = proc
    _state["thread_id"] = _kernel32.GetCurrentThreadId()
    hmod = _kernel32.GetModuleHandleW(None)
    hook = _user32.SetWindowsHookExW(WH_KEYBOARD_LL, proc, hmod, 0)
    if not hook:
        err = ctypes.get_last_error()
        print(f"[win_h_language_router] SetWindowsHookEx failed: {err}")
        return
    _state["hook"] = hook
    _log("hook installed")
    msg = wt.MSG()
    while True:
        ret = _user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
        if ret == 0 or ret == -1:
            break
    _user32.UnhookWindowsHookEx(hook)
    _state["hook"] = None
    _log("hook removed")


def _start():
    if not ENABLED:
        _log("disabled via ENABLED=False; not installing hook")
        return
    if app.platform != "windows":
        return
    t = _state["thread"]
    if t is not None and t.is_alive():
        return
    t = threading.Thread(
        target=_hook_thread, daemon=True, name="win_h_language_router_hook"
    )
    _state["thread"] = t
    t.start()


def _shutdown(*_):
    tid = _state.get("thread_id")
    if tid and _user32 is not None:
        _user32.PostThreadMessageW(tid, WM_QUIT, 0, 0)


app.register("ready", _start)
app.register("shutdown", _shutdown)
