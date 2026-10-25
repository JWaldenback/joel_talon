# Select a Mac dictation provider

The pedal and double left Option use the provider selected in Karabiner.
Talon can be closed. The pedal remains programmed to send Windows+H.

| Input                                                     | Result                                                         |
| --------------------------------------------------------- | -------------------------------------------------------------- |
| Windows+H from either supported RS pedal                  | Toggle the selected provider                                   |
| Two quick taps of left Option, with no other keys between | Toggle the selected provider                                   |
| Double Control                                            | Native Apple Dictation, independently of the selected provider |
| Right Option / AltGr                                      | Existing keyboard and screenshot behaviour                     |

Wispr uses its default **Fn+Space** hands-free shortcut. Leave Flow's shortcuts
at their defaults; Command is not used to start or stop dictation. A pedal press starts recording; the next
press stops and transcribes. Wispr Flow must be running. If it is closed, the
rule requests a notification asking you to open it, without starting Apple
Dictation instead. Notification visibility depends on macOS notification settings.

Left Option still works in ordinary keyboard combinations. Each isolated tap
must be shorter than 250 ms, with the second tap starting within 350 ms of the
first release. If another key is pressed between taps, the gesture is cancelled.
The first tap's expiry timer also limits the total gesture to 500 ms.

## Select the provider

The standalone selector lives in this repository:

```sh
~/.talon/user/joel_talon/docs/macos/dictation-provider wispr
~/.talon/user/joel_talon/docs/macos/dictation-provider macos
~/.talon/user/joel_talon/docs/macos/dictation-provider status
```

When Talon is running, these voice commands call the same selector:

- **dictation provider Wispr**
- **dictation provider Mac**
- **dictation provider status**

Select a provider between recordings. Switching during recording is outside
this setup's supported use. Existing native-dictation voice commands still
target Apple Dictation; the selected route applies to the pedal and double
left Option.

The selector updates one managed rule in the selected Karabiner profile. It
replaces the old direct-to-Apple pedal rule and preserves other rules, profiles,
and device settings. The selected provider is stored in that rule, so it
survives restarting Talon, Karabiner, or the Mac. There is no selector daemon
and no Talon process on the pedal's execution path.

The original profile file is saved once as
`~/.config/karabiner/karabiner.json.before-dictation-provider`. To return to
Apple Dictation while retaining other later configuration edits, run the
`macos` command above. For complete removal, remove the rule named
**Selected dictation provider: ...** in Karabiner and reinstall the original
[direct-to-Apple pedal rule](rs-foot-pedal-dictation.json). Restoring the whole
snapshot would also undo any later unrelated Karabiner changes.

## Talon microphone and gaze

When Talon is running, the Mac watcher recognises Apple Dictation and Wispr's
Core Audio recording processes. It pauses Talon's microphone and gaze during
recording and restores them after recording has stopped for 600 ms. Merely
leaving Flow open does not pause Talon. A separate manual Talon pause remains
in effect. Control+Option+Escape and the existing pause pedal retain their
recording-cancellation and Talon recovery behaviour. Flow's cancel shortcut
must remain Escape for that recovery path.

## Physical acceptance check

Use an editable scratch document. With Wispr selected, test the pedal twice
and then double left Option twice. Confirm recording starts and stops, text
is inserted, and Talon's microphone/gaze pause and restore when Talon is open.
Repeat with Talon closed. Keep Flow running for both checks.

Confirm double Control still starts Apple Dictation, ordinary Option+letter
combinations still work, and the right Option screenshot shortcut still works.
Select `macos` and test the pedal, then restore the desired provider.
These physical tests cannot be established by a JSON linter or simulated keys.

The double-tap rule uses Karabiner 16.3's expression variables and isolated-tap
handling. References: [double-tap examples](https://karabiner-elements.pqrs.org/docs/json/typical-complex-modifications-examples/),
[isolated taps](https://karabiner-elements.pqrs.org/docs/json/complex-modifications-manipulator-definition/to-if-alone/).
