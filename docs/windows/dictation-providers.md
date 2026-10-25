# Select a Windows dictation provider

The repo-owned AutoHotkey 1.1 script
[double_tap_control.ahk](../../plugin/dictation_router/double_tap_control.ahk)
runs independently of Talon. Wispr Flow must be running and its hands-free
shortcut must be **Ctrl+Win+Space**. Leave cancellation bound to Escape.

| Input | Result |
| --- | --- |
| Pedal sending Win+H, or physical Win+H | Toggle the selected provider |
| Two isolated taps of left Alt | Toggle the selected provider |
| Two isolated taps of either Control key | Native Windows voice typing |
| Right Alt / AltGr | Existing keyboard and screenshot shortcuts |

Each tap must be shorter than 500 ms and the gap between releases at most
400 ms. Another key between or during taps cancels the gesture. Ordinary
Alt+letter shortcuts pass through. Isolated left Alt taps no longer open an
application's menu, so that menu does not receive the dictation shortcut.
Talon's injected native-dictation voice shortcuts continue to target Windows.

A pedal press starts Flow; the next press stops and inserts the transcript.
The script routes after the pedal is released and ignores held-key repeats.
If Flow is closed, a tray notification asks you to open it. There is no silent
fallback to Windows dictation.

## Select the provider

For repo-owned runnable controls and a repeatable Desktop/startup installer,
see the [Windows tools catalog](../../tools/windows/README.md).

On this Windows machine, double-click **Talon - Use Wispr.cmd** or
**Talon - Use Windows Dictation.cmd** on the Desktop. **Talon - Dictation
Status.cmd** shows the saved choice. The accompanying **Dictation provider
commands.txt** explains the controls and includes the PowerShell commands.
These Desktop files call the selector below and work with Talon closed.

Run from this repository in PowerShell, between recordings:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\docs\windows\dictation-provider.ps1 wispr
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\docs\windows\dictation-provider.ps1 windows
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\docs\windows\dictation-provider.ps1 status
```

With Talon running, the same choices are available as voice commands:

- **dictation provider Wispr**
- **dictation provider Windows**
- **dictation provider status**

Selection is saved in `%APPDATA%\TalonDictation\provider.txt`. The script reads
it for each toggle, so selection survives restarting Talon, AutoHotkey or
Windows and needs no script reload. An absent file means Windows; an invalid
file produces a notification and sends no dictation shortcut.

## Windows startup

The existing `double-tap-control-dictation.lnk` in `shell:startup` runs:

```text
"C:\Program Files\AutoHotkey\AutoHotkey.exe" "%APPDATA%\talon\user\joel_talon\plugin\dictation_router\double_tap_control.ahk"
```

The shortcut points directly at the repo, including the adjacent
`dictation_taps.ahk` library. After changing these scripts, launch the startup
shortcut again to replace the old instance. Keep only one startup entry for
this script. Do not also run the older `double_tap_altgr.ahk` if right Alt is
reserved for screenshot shortcuts. To disable this setup, exit its AutoHotkey
tray icon and remove the startup shortcut.

## Talon and physical checks

When Talon runs, the microphone watcher recognises active capture sessions
from `Wispr Flow.exe` and `Wispr Flow Helper.exe`. It pauses Talon's mic and
gaze during recording and restores them afterward. An existing manual pause
stays in effect. Keypad divide cancels a recording and recovers Talon input,
as it does for Windows voice typing.

In an editable scratch document, test the pedal twice and double left Alt
twice. Confirm recording starts, finishes and inserts text. Repeat with Talon
open and confirm mic/gaze pause and restore, then check keypad-divide recovery.
Confirm double Control still starts Windows voice typing, Alt+letter and AltGr
shortcuts still work, and select `windows` to check the native pedal route.
Switch back to the desired provider afterward. A fresh Windows login confirms
startup execution; inspecting the shortcut alone cannot prove that login check.

Flow documents its [Windows shortcuts](https://docs.wisprflow.ai/articles/2612050838-Supported-%26-Unsupported-Keyboard-Hotkey-Shortcuts)
and [hands-free behaviour](https://docs.wisprflow.ai/articles/6391241694-use-flow-hands-free).
