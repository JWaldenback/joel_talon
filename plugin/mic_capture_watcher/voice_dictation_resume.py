"""
Auto-resume Talon when a manual key press cancels a Win+H dictation that
was started via the "start listening" voice command.

Flow:
  1. "start listening" calls `voice_dictation_arm_keypress_resume()`, which
     sets a flag and installs a Windows low-level keyboard hook (the hook
     itself is installed once, lazily, and stays loaded; only the flag
     toggles).
  2. While armed, any non-injected key-down event triggers a resume:
     close the Win+H pill (via super-h) and re-enable Talon speech +
     wake the mouse. Talon's own injected keystrokes are filtered via
     LLKHF_INJECTED so they never trip the hook.
  3. The flag is cleared automatically on resume, on "stop listening",
     and whenever the mic_capture_watcher observes the pill closing —
     so paths that didn't go through "start listening" (e.g. talon
     sleep then manual Win+H) are unaffected.
"""

import ctypes
import ctypes.wintypes as wt
import threading

from talon import Module, actions, app, cron

mod = Module()

WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_SYSKEYDOWN = 0x0104
WM_QUIT = 0x0012
LLKHF_INJECTED = 0x10
LLKHF_LOWER_IL_INJECTED = 0x02

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


_state = {
    "armed": False,
    "hook": None,
    "thread": None,
    "thread_id": None,
    "proc": None,
}
_lock = threading.Lock()


def _resume_on_main():
    with _lock:
        if not _state["armed"]:
            return
        _state["armed"] = False
    # Hand the resume off to mic_capture_watcher. mark_disabled_by_us
    # ensures it will speech.enable() the next time it observes the pill
    # close — whether that close came from the user's keystroke (most
    # common on Win11) or from our delayed super-h below.
    # Avoid sending super-h immediately: the audio-session check can still
    # report active when the keystroke is already closing the pill, and
    # toggling super-h then would reopen it and silence Talon again.
    try:
        from . import mic_capture_watcher as _mcw
        _mcw.mark_disabled_by_us("win_h_dictation")
    except Exception as e:
        print(f"[voice_dictation_resume] mark disabled_by_us failed: {e}")
    try:
        actions.user.mouse_wake()
    except Exception as e:
        print(f"[voice_dictation_resume] mouse_wake failed: {e}")
    cron.after("600ms", _close_pill_if_still_active)


def _close_pill_if_still_active():
    try:
        from . import mic_capture_watcher as _mcw
        if _mcw.is_service_active("win_h_dictation"):
            actions.key("super-h")
    except Exception as e:
        print(f"[voice_dictation_resume] late super-h failed: {e}")


def _hook_proc(nCode, wParam, lParam):
    if nCode == 0 and wParam in (WM_KEYDOWN, WM_SYSKEYDOWN):
        if _state["armed"]:
            kbd = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT))[0]
            injected = bool(kbd.flags & (LLKHF_INJECTED | LLKHF_LOWER_IL_INJECTED))
            if not injected:
                cron.after("0ms", _resume_on_main)
    return _user32.CallNextHookEx(_state["hook"] or 0, nCode, wParam, lParam)


def _hook_thread():
    proc = LowLevelKeyboardProc(_hook_proc)
    _state["proc"] = proc
    _state["thread_id"] = _kernel32.GetCurrentThreadId()
    hmod = _kernel32.GetModuleHandleW(None)
    hook = _user32.SetWindowsHookExW(WH_KEYBOARD_LL, proc, hmod, 0)
    if not hook:
        err = ctypes.get_last_error()
        print(f"[voice_dictation_resume] SetWindowsHookEx failed: {err}")
        return
    _state["hook"] = hook
    msg = wt.MSG()
    while True:
        ret = _user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
        if ret == 0 or ret == -1:
            break
    _user32.UnhookWindowsHookEx(hook)
    _state["hook"] = None


def _ensure_hook_running():
    if app.platform != "windows":
        return
    t = _state["thread"]
    if t is not None and t.is_alive():
        return
    t = threading.Thread(
        target=_hook_thread, daemon=True, name="voice_dictation_resume_hook"
    )
    _state["thread"] = t
    t.start()


def _shutdown(*_):
    _state["armed"] = False
    tid = _state.get("thread_id")
    if tid and _user32 is not None:
        _user32.PostThreadMessageW(tid, WM_QUIT, 0, 0)


app.register("shutdown", _shutdown)


@mod.action_class
class Actions:
    def voice_dictation_arm_keypress_resume():
        """Arm: next non-injected key press will close Win+H and resume Talon."""
        if app.platform != "windows":
            return
        with _lock:
            _state["armed"] = True
        _ensure_hook_running()

    def voice_dictation_disarm_keypress_resume():
        """Clear the arm flag without closing dictation."""
        with _lock:
            _state["armed"] = False
