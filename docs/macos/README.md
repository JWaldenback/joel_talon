# Mac setup: Talon, Apple Dictation and foot pedal

Recorded on 2026-09-26 using macOS 27.0, Talon 1.0 build 116 and
Karabiner-Elements 16.3.0. The user confirmed the direct Dictation pedal mapping
works on this Mac. Recheck it after installation on another computer.

## 1. Install the Talon repositories

Install [Talon](https://talonvoice.com/) and complete its permissions and input
device setup. The macOS user folder is `~/.talon/user`, which expands to
`/Users/<your-account>/.talon/user`.

Clone these repositories as sibling folders. Authenticate to GitHub with an
account that can access the private repository. Skip any clone already present.

```sh
mkdir -p ~/.talon/user
cd ~/.talon/user
git clone https://github.com/JWaldenback/joel_talon.git
git clone https://github.com/JWaldenback/joel_talon_private.git
git clone https://github.com/JWaldenback/talon_hud.git
```

Use repository revisions containing the Mac support and CoreSpeech watcher fix.
Local commits must be pushed or transferred before a different Mac can obtain
them; cloning GitHub does not include unpublished work.

Talon loads these folders directly. Keep only one active copy of each command
set under the user folder. Put backups outside that folder.

### Private files and hostname

Follow `joel_talon_private/README.md`. Find the new computer's Talon hostname
with `actions.user.talon_get_hostname()` in the Talon REPL. Create its own
`<hostname>/system_paths.talon-list` in the private repository, with a matching
`hostname:` header and paths appropriate to that Mac. Folder names alone do not
restrict which computer loads a file.

Shared vocabulary and websites already load across computers. If the public
repo generated `core/system_paths-<hostname>.talon-list`, migrate its contents
to the private file and keep only one active definition for that host. Preserve
the old file outside Talon's user folder until the migration is verified.

### HUD and eye tracking

Say **talon hood restart** to enable the HUD, status bar, microphone control and
command history. HUD installation does not configure the eye tracker itself;
complete Talon's tracker setup separately. Say **gaze mode** to test gaze control.

## 2. Configure Apple Dictation

In **System Settings → Keyboard → Dictation**:

1. Enable Dictation and select the intended microphone.
2. Keep **Shortcut → Press Control Key Twice** as the keyboard shortcut.
3. Under **Languages → Edit**, select **English (United States)** and
   **Swedish (Sweden)** if both are wanted. Complete any language downloads.

Keep **Text Input → Input Sources** set to Swedish. Dictation languages are
configured separately; adding English Dictation does not require adding an
English keyboard layout. This computer now has both Dictation languages enabled
and only the Swedish keyboard layout. macOS reported that support for processing
voice input on the Mac was still awaiting download after Swedish was added.

Start Dictation with the cursor in a text field. When multiple languages are
enabled, click the language label beside the cursor to choose another language.
Apple also documents pressing the Globe key, if available, and choosing a
language. This does not require changing the Mac's interface language.

The pedal below starts Dictation in its selected language. It does not choose
Swedish or English. No dedicated language-switching pedal rule is installed.
The existing Windows AutoHotkey language commands remain Windows-only.

See [Apple's Dictation instructions](https://support.apple.com/guide/mac-help/use-dictation-mh40584/mac)
and [language availability](https://www.apple.com/macos/feature-availability/).
Both enabled languages were verified in System Settings. Swedish speech
recognition and switching languages using only the keyboard still need a live
test. Control-Space was tested with only the Swedish keyboard layout enabled
and did not change the Dictation language. Do not use it as a verified
Dictation-only language switch for this setup.

## 3. Install Karabiner-Elements

Install from the [official website](https://karabiner-elements.pqrs.org/), or use
`brew install --cask karabiner-elements` if Homebrew is available. The installer
needs macOS administrator authentication.

Open Karabiner-Elements and finish its setup prompts for background services,
Accessibility/Input Monitoring and the virtual keyboard driver. Choose the
virtual keyboard type that matches your hardware. This Mac uses ISO with a
Swedish keyboard layout; do not copy that choice blindly to another keyboard.

See [Karabiner's installation guide](https://karabiner-elements.pqrs.org/docs/getting-started/installation/).

## 4. Add the foot-pedal rule

Leave the pedal programmed to send **Windows-H**. macOS receives that as
**Command-H**. Karabiner translates it only when it comes from the matching
pedal, sending the native Dictation key directly:

```json
{ "consumer_key_code": "dictation", "repeat": false }
```

The working device reports:

| Field | Value |
| --- | --- |
| Manufacturer | OLYMPUS CORPORATION |
| Product | HID FootSwitch RS Series |
| Vendor ID | `1972` / `0x07B4` |
| Product ID | `660` / `0x0294` |
| Interface | Keyboard |

The filter matches this model, not a unique serial number. Another pedal of the
same model would also match. For different hardware, inspect its identifiers
in Karabiner's Devices/EventViewer and update the rule.

Copy the included [rule file](rs-foot-pedal-dictation.json) into Karabiner's
rule library:

```sh
mkdir -p ~/.config/karabiner/assets/complex_modifications
cp ~/.talon/user/joel_talon/docs/macos/rs-foot-pedal-dictation.json \
  ~/.config/karabiner/assets/complex_modifications/
```

In **Karabiner-Elements → Complex Modifications**, choose **Add predefined rule**
and enable **RS foot pedal: Windows-H sends Apple Dictation key** in the desired
profile. If that rule already exists, edit or replace it instead of adding a
duplicate. In **Devices**, make sure **Modify events** is enabled for the foot
switch's keyboard interface.

The JSON file is a rule library, not an entire `karabiner.json` configuration.
Do not overwrite an existing profile with it. Talon does not install this rule
automatically just because this repository is present.

Simple Modifications cannot match the Command-H combination. Complex
Modifications also let us restrict the match to the pedal. Normal keyboard
Command-H keeps its normal behavior. The original attempt to generate two
Control presses did not work in the physical test; the direct Dictation key
replacement did. Keep Control twice as the separate macOS keyboard shortcut.

## 5. Check the behavior

1. Focus a text field and press/release the Windows-H pedal. Confirm Dictation
   starts. Test stopping it with another press.
2. Confirm Control twice still starts Dictation from the keyboard.
3. Quit Talon and repeat the pedal test, then reopen Talon. The rule uses only
   Karabiner and macOS; this explicit Talon-closed test remains a verification
   step for a new setup and was not separately observed in this session.
4. With Talon running and gaze enabled, start Dictation and check that Talon's
   microphone and gaze pause, then restore when Dictation stops.
5. Press the keypad-divide pedal to check manual Talon pause/resume. This pedal
   binding belongs to Talon and therefore needs Talon running.

The Mac watcher uses CoreAudio and needs no extra Python package. It watches
both DictationIM and CoreSpeech recording activity. CoreSpeech may also be used
by other Apple speech features, so those can pause Talon too. A manual Talon
pause remains in effect after Dictation ends. **Control-Option-Escape** releases
a stuck Dictation pause. See the [watcher README](../../plugin/mic_capture_watcher/README.md).

This setup leaves the pedal's hardware programming and Windows commands
unchanged. Karabiner's mapping exists only on the Mac.

## Troubleshooting and removal

- If the rule is missing, check that its file is in the rule library and enable
  it in the selected profile. Copying the file alone does not enable it.
- If nothing happens, check Karabiner's setup warnings, device identifiers and
  **Modify events** setting. Use EventViewer to inspect what the pedal sends.
- Test in an editable text field with Dictation enabled. The rule does not
  enable the macOS Dictation setting or select a language for you.
- To undo the mapping, remove/disable this rule in Complex Modifications.
  The pedal then sends ordinary Command-H on the Mac again.

The configuration file is `~/.config/karabiner/karabiner.json`. Back it up before
manual edits. The portable rule is tracked here; local profiles and private
Talon vocabulary are not copied into this public repository.
