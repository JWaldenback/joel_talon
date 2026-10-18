"""Timing log for Win+H dictation starts.

Answers "I pressed the pedal, why did dictation start late (or not at all)?"
by appending these events to mic_and_eye_tracker_state.log:

  win_h_pressed      Win+H reached our low-level keyboard hook. hook_delay_ms
                     is how long Windows held the key event before our hook saw
                     it (GetTickCount resolution, ~16 ms). A large value means
                     the keystroke itself was delayed system-wide.
  dictation_detected / dictation_cleared
                     (logged by mic_capture_watcher) now carry since_win_h_ms:
                     time from the last unanswered Win+H to the watcher seeing
                     voice typing open or close.
  win_h_unanswered   A Win+H was followed by no open/close within
                     UNANSWERED_AFTER_S, or was superseded by another Win+H
                     first (the "press it again" case).
  watcher_tick_gap   The watcher's cron tick ran much later than its interval,
                     i.e. Talon's cron thread was stalled. Detection latency in
                     that window is Talon's, not Windows'.

The keyboard hook itself lives in voice_dictation_resume.py (one hook for
both features). This module is pure Python so it can be unit tested, and the
hook thread only enqueues — all file I/O happens on a writer thread.
"""

import queue
import threading
import time

from talon import Module, app, settings

from .mic_and_eye_tracker_state_log import log as _state_log

mod = Module()
mod.setting(
    "dictation_timing_log_enabled",
    type=bool,
    default=True,
    desc="Log Win+H press times and dictation start latency to mic_and_eye_tracker_state.log. Keeps the low-level keyboard hook installed from startup.",
)

VK_H = 0x48
UNANSWERED_AFTER_S = 3.0
# Only report tick gaps clearly beyond normal jitter of the 300 ms poll.
TICK_GAP_MIN_MS = 1000


class PressTracker:
    """Pairs Win+H presses with the next dictation open/close.

    Times are time.monotonic() seconds. Thread-safe: presses arrive on the
    writer thread, transitions and expiry on Talon's cron thread.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._pending = None

    def press(self, t: float):
        """Record a press. Returns the superseded pending press time, if any."""
        with self._lock:
            superseded = self._pending
            self._pending = t
            return superseded

    def transition(self, t: float):
        """Dictation opened or closed. Returns ms since the pending press."""
        with self._lock:
            pending, self._pending = self._pending, None
        if pending is None:
            return None
        return round((t - pending) * 1000)

    def expire(self, t: float):
        """Return and clear a press that has gone unanswered too long."""
        with self._lock:
            if self._pending is None or t - self._pending < UNANSWERED_AFTER_S:
                return None
            pending, self._pending = self._pending, None
            return pending


class TickGapDetector:
    """Detects cron ticks that fire far later than their interval."""

    def __init__(self):
        self._last = None

    def tick(self, t: float, interval_ms: int):
        """Returns the gap in ms when it is abnormally long, else None."""
        last, self._last = self._last, t
        if last is None:
            return None
        gap_ms = round((t - last) * 1000)
        if gap_ms >= max(TICK_GAP_MIN_MS, 3 * interval_ms):
            return gap_ms
        return None


_presses = PressTracker()
_gaps = TickGapDetector()
_queue: queue.SimpleQueue = queue.SimpleQueue()
_state = {"enabled": True, "h_down": False, "writer": None}


def enabled() -> bool:
    return _state["enabled"]


def on_hook_key(vk: int, is_down: bool, win_down: bool, injected: bool, hook_delay_ms: int):
    """Called on the keyboard-hook thread for every key event. Must stay
    cheap and never block: it only filters and enqueues."""
    if vk != VK_H:
        return
    if not is_down:
        _state["h_down"] = False
        return
    # Ignore auto-repeat while H (or the pedal) is held.
    if _state["h_down"]:
        return
    _state["h_down"] = True
    if win_down and _state["enabled"]:
        _queue.put((time.monotonic(), hook_delay_ms, injected))


_WRITER_NAME = "dictation_timing_writer"


def _writer(inbox: queue.SimpleQueue):
    while True:
        item = inbox.get()
        if item is None:
            return
        _handle_press(*item)


def _handle_press(t: float, hook_delay_ms: int, injected: bool):
    superseded = _presses.press(t)
    if superseded is not None:
        _state_log(
            "win_h_unanswered",
            source="dictation_timing",
            reason="pressed_again",
            waited_ms=round((t - superseded) * 1000),
        )
    _state_log(
        "win_h_pressed",
        source="dictation_timing",
        hook_delay_ms=hook_delay_ms,
        injected=injected,
    )


def _ensure_writer():
    w = _state["writer"]
    if w is not None and w.is_alive():
        return
    # A Talon reload leaves the previous module's writer blocked on its own
    # queue; send it the stop sentinel so threads don't pile up.
    for old in threading.enumerate():
        if old.name == _WRITER_NAME and old is not w and hasattr(old, "inbox"):
            old.inbox.put(None)
    w = threading.Thread(target=_writer, args=(_queue,), daemon=True, name=_WRITER_NAME)
    w.inbox = _queue
    _state["writer"] = w
    w.start()


def on_dictation_transition():
    """Called by the watcher when Win+H dictation opens or closes. Returns
    ms since the press that (presumably) caused it, or None."""
    return _presses.transition(time.monotonic())


def on_watcher_tick(interval_ms: int):
    """Called at the start of every watcher tick."""
    if not _state["enabled"]:
        return
    now = time.monotonic()
    gap_ms = _gaps.tick(now, interval_ms)
    if gap_ms is not None:
        _state_log(
            "watcher_tick_gap",
            source="dictation_timing",
            gap_ms=gap_ms,
            interval_ms=interval_ms,
        )
    unanswered = _presses.expire(now)
    if unanswered is not None:
        _state_log(
            "win_h_unanswered",
            source="dictation_timing",
            reason="no_open_or_close",
            waited_ms=round((now - unanswered) * 1000),
        )


def _apply_setting(*_args):
    _state["enabled"] = bool(settings.get("user.dictation_timing_log_enabled"))
    if _state["enabled"]:
        _ensure_writer()


def _on_ready():
    settings.register("user.dictation_timing_log_enabled", _apply_setting)
    _apply_setting()


app.register("ready", _on_ready)
