# windows_dictation_detector

Auto-pauses Talon's speech engine while Windows voice typing (Win+H) is
actively listening, then resumes it when the dictation pill closes.

## Setup

This plugin needs the `comtypes` package, which is not bundled with Talon.

Run `install_deps.bat` once after cloning (right-click → "Run as administrator"
since Talon lives under `C:\Program Files`).

Then restart Talon.

## Configuration

The watcher auto-starts at Talon launch when `user.windows_dictation_watch_enabled`
is True (the default). To disable it, add to your `settings.talon`:

```
settings():
    user.windows_dictation_watch_enabled = 0
```

Voice commands for debugging (`dictation watch start/stop`, `dictation check
now`, `dictation dump sessions`) are commented out in
[`windows_dictation_detector.talon`](windows_dictation_detector.talon) —
uncomment if you need them.

## How it works

The plugin watches Windows audio capture sessions via the Core Audio
`IAudioSessionEnumerator` API. When `TextInputHost.exe` opens an active
capture session (which happens when you press Win+H and start speaking), the
plugin disables Talon's speech engine and sleeps the mouse (so gaze/head
tracking stops moving the cursor while you dictate). When the session goes
inactive, both are restored.

This avoids two dead ends we hit during development: (1) Win11's dictation
pill is not enumerable as a top-level window, and (2) on modern Win11 builds
voice typing runs in-process inside `TextInputHost.exe` rather than spawning
a separate `SpeechRuntime.exe`, so process-presence checks don't help either.
