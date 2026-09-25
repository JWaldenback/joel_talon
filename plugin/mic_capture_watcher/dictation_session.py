"""State shared by Mac dictation and manual input pauses, independent of Talon."""

from threading import RLock


class InputPause:
    def __init__(self, get_microphone, set_microphone, sleep_mouse, wake_mouse):
        self.get_microphone = get_microphone
        self.set_microphone = set_microphone
        self.sleep_mouse = sleep_mouse
        self.wake_mouse = wake_mouse
        self.owners = set()
        self.saved_microphone = None
        self.lock = RLock()

    def acquire(self, owner):
        with self.lock:
            if owner in self.owners:
                return
            first = not self.owners
            if first:
                self.saved_microphone = self.get_microphone()
                if self.saved_microphone and self.saved_microphone != "None":
                    self.set_microphone("None")
            try:
                self.sleep_mouse(owner)
            except Exception:
                # mouse_sleep can acquire its owner before a later action
                # fails. Always release that partial acquisition as well.
                try:
                    self.wake_mouse(owner)
                finally:
                    if first and self.saved_microphone and self.saved_microphone != "None":
                        self.set_microphone(self.saved_microphone)
                    if first:
                        self.saved_microphone = None
                raise
            self.owners.add(owner)

    def release(self, owner):
        with self.lock:
            if owner not in self.owners:
                return
            self.wake_mouse(owner)
            if len(self.owners) == 1:
                # Never unmute a microphone which was already off, or override
                # a different microphone explicitly selected while paused.
                if self.saved_microphone and self.saved_microphone != "None":
                    if self.get_microphone() == "None":
                        self.set_microphone(self.saved_microphone)
                self.saved_microphone = None
            self.owners.remove(owner)

    def held(self, owner):
        with self.lock:
            return owner in self.owners


class DictationSession:
    """Wait for recording to start, then resume after a stable stop signal."""

    def __init__(self, pause, start_timeout=5.0, stop_delay=0.6):
        self.pause = pause
        self.start_timeout = start_timeout
        self.stop_delay = stop_delay
        self.pending_until = None
        self.inactive_since = None
        self.owner = "mac_dictation"

    @property
    def active(self):
        return self.pause.held(self.owner)

    def start(self, now):
        if self.active:
            return
        self.pause.acquire(self.owner)
        self.pending_until = now + self.start_timeout
        self.inactive_since = None

    def observe(self, recording, now):
        if recording:
            self.pause.acquire(self.owner)
            self.pending_until = None
            self.inactive_since = None
            return None
        if not self.active:
            return None
        if self.pending_until is not None:
            if now < self.pending_until:
                return None
            self.finish()
            return "start_failed"
        if self.inactive_since is None:
            self.inactive_since = now
        elif now - self.inactive_since >= self.stop_delay:
            self.finish()
            return "finished"
        return None

    def finish(self):
        self.pause.release(self.owner)
        self.pending_until = None
        self.inactive_since = None
