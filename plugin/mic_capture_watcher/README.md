# mic_capture_watcher

Auto-pauses Talon's speech engine and head/eye tracking whenever a known
microphone-capturing service (Windows voice typing, Super Whisper, ...) is
actively listening, then resumes when the service stops.

## Setup

macOS uses the system Core Audio API to monitor Apple built-in Dictation.
No extra Python package is needed. Linux automatic polling remains disabled.

On Mac, say **start listening** (or use your existing dictation key switch).
The plugin reads your configured macOS Dictation shortcut without changing it.
Talon’s microphone and tracking pause during recording and restore afterward.
A separate manual Talon pause stays in effect. **Control-Option-Escape** stops
Dictation and releases its pause if recovery is needed.

If shortcut detection is unavailable, set `user.mac_dictation_shortcut` to the
configured Talon key sequence, such as `ctrl ctrl` or `fn-d`. Automatic detection
uses the Core Audio process bundle `com.apple.inputmethod.ironwood`; this can be
overridden with `user.mac_dictation_bundle_ids` if Apple changes it.

This Mac integration targets Apple Dictation only, not Superwhisper. It uses
per-process input state rather than treating any app using the microphone as
dictation.

On Windows, it needs the `comtypes` package, which is not bundled with Talon.

Run `install_deps.bat` once after cloning (right-click → "Run as administrator"
since Talon lives under `C:\Program Files`).

Then restart Talon.

## Configuration

On Windows and macOS, the watcher auto-starts at Talon launch when
`user.mic_capture_watch_enabled` is True (the default). To disable it, add to
your `settings.talon`:

```
settings():
    user.mic_capture_watch_enabled = 0
```

Voice commands for debugging (`mic watch start/stop`, `mic check now`,
`mic dump sessions`) are commented out in
[`mic_capture_watcher.talon`](mic_capture_watcher.talon) — uncomment if needed.

## Adding a new service

Edit the `CAPTURE_SERVICES` list at the top of
[`mic_capture_watcher.py`](mic_capture_watcher.py):

```python
CAPTURE_SERVICES = [
    ...,
    {
        "name": "my_new_service",
        "display": "My New Service",
        "processes": {"myapp.exe"},  # lowercase exe names
    },
]
```

To find the right process name while the service is listening, run the
`mic_capture_dump_sessions` action — the capturing process appears with
`state=Active`.

If the service needs custom behavior on deactivation (e.g. clearing an
external flag), add an `"on_deactivate": callable` key to the entry.

## How it works on Windows

Polls Windows Core Audio's `IAudioSessionEnumerator` API every ~300 ms for
processes with an active capture session. When any registered service
matches, Talon's speech engine is disabled and the mouse is slept (so
gaze/head tracking stops moving the cursor while you dictate elsewhere).
When all services go inactive, both are restored.

The audio-session approach was chosen over window-presence or process-
presence checks because: (1) Win11's dictation pill is not enumerable as
a top-level window, (2) on modern Win11 builds voice typing runs in-process
inside `TextInputHost.exe`, and (3) GUI apps like Super Whisper keep their
process running continuously — only the *capture session* reliably tracks
whether the mic is actually being recorded.
