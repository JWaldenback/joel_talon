# Personal Windows tools

This is the catalog of runnable tools kept with this Talon setup. The source
stays in Git. Desktop and startup shortcuts can be recreated on a new PC.

## Set up a new PC

1. Install Talon, Git and AutoHotkey **1.1**. Install Wispr Flow if you want
   to use it. AutoHotkey 2 cannot run these 1.1 scripts.
2. Clone this fork into Talon's user directory:

   ```powershell
   git clone https://github.com/JWaldenback/joel_talon.git "$env:APPDATA\talon\user\joel_talon"
   ```

   Keep only one community command set loaded in Talon's user directory.

3. In that checkout, open `tools\windows` and double-click **install.cmd**.
   It creates a **Talon tools** folder on the Desktop and the dictation
   startup shortcut. Rerunning it updates the same links.
4. Open the Desktop folder and run **Talon - Start dictation shortcuts**,
   or sign in again. Setup does not launch any keyboard hook automatically.
5. For Wispr, set Flow's hands-free shortcut to **Ctrl+Win+Space** and leave
   cancellation on Escape. Run **Talon - Use Wispr**. A new PC initially uses
   native Windows dictation; an existing PC keeps its saved selection.
6. For Talon's automatic mic/gaze pause, follow the
   [microphone watcher setup](../../plugin/mic_capture_watcher/README.md).
   Check the pedal and keyboard shortcuts in a scratch text field.

Keep this checkout in place. The links point at its source, so pulling an
update updates the tools too. If you move the checkout, rerun setup from the
new location. After an AutoHotkey source change, run **Start dictation
shortcuts** again to replace its running instance.

## Installed controls

| Control | What it does | Runs at login? |
| --- | --- | --- |
| [Talon - Use Wispr](launchers/Talon%20-%20Use%20Wispr.cmd) | Select Wispr for the pedal and double left Alt | No |
| [Talon - Use Windows Dictation](launchers/Talon%20-%20Use%20Windows%20Dictation.cmd) | Select native Windows dictation for those controls | No |
| [Talon - Dictation Status](launchers/Talon%20-%20Dictation%20Status.cmd) | Show the saved provider choice | No |
| [Talon - Start dictation shortcuts](../../plugin/dictation_router/double_tap_control.ahk) | Run the AutoHotkey pedal, Alt and Control shortcuts | Yes |
| Talon - Tools guide | Open this catalog | No |

These controls work with Talon closed. Double Control always opens native
Windows dictation. Switch providers between recordings. Selection survives
restarting the apps or PC. The three `.cmd` files also run directly from the
repo without installing Desktop links.

The installer uses Windows' actual Desktop and Startup folders, including
redirected Desktops. If AutoHotkey is installed elsewhere, run this from
`tools\windows` with its actual executable path:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -AutoHotkeyPath "D:\Apps\AutoHotkey\AutoHotkey.exe"
```

## Other helpers and their status

| Source | Status and purpose |
| --- | --- |
| [double_tap_control.ahk](../../plugin/dictation_router/double_tap_control.ahk) | Active. The main dictation shortcut process installed above |
| [dictation_taps.ahk](../../plugin/dictation_router/dictation_taps.ahk) | Library used by the main script. Do not run separately |
| [double_tap_altgr.ahk](../../plugin/dictation_router/double_tap_altgr.ahk) | Older optional helper. Double right Alt starts Windows dictation. Setup does not enable it because it conflicts with reserving AltGr for other shortcuts |
| [dictation-provider.ps1](../../docs/windows/dictation-provider.ps1) | Standalone provider selector used by the Desktop and voice controls |
| [install_deps.bat](../../plugin/mic_capture_watcher/install_deps.bat) | One-time installation of Talon's Windows audio-monitoring dependency. Follow the watcher's setup instructions |

Add future personal launchers here, describe their purpose and dependencies,
and state whether they run at login. Keep only deliberately enabled tools in
the installer. The test-only AutoHotkey script under `test` is not a user tool.

## Existing Desktop files and removal

The earlier loose `.cmd` controls on this PC remain usable. Setup creates the
managed folder alongside them and does not delete them or any unrelated files.

To remove these installed links, delete the **Talon tools** Desktop folder and
`double-tap-control-dictation.lnk` from `shell:startup`. Exit the dictation
script's AutoHotkey tray icon to stop its current instance. The repo and saved
provider choice remain available.
