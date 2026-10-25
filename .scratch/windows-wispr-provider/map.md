# Windows dictation provider

Status: ready-for-human
Claimed by: none
Blocked by: live Talon mic/gaze, remaining shortcut compatibility and fresh-login checks

## Outcome and scope

Adapt the Mac provider setup for Windows. Save the AutoHotkey source in this
repo and run it at Windows login. The Win+H pedal and double left Alt toggle
the selected provider. Double Control stays native. Wispr recording pauses
Talon's microphone and gaze and releases that pause afterward.

Robustness allowance: reject an invalid saved provider, report a closed Flow
without starting Windows dictation, and ignore modifier combinations when
recognising double taps. Keep AltGr and existing startup entries intact.
Provider switching during recording is unsupported.

## Decisions so far

- 2026-10-25, agent: reuse the installed AutoHotkey 1.1 script and its startup
  shortcut. Store the provider outside the shared repo so the Windows and Mac
  selections remain independent. Talon is optional on the shortcut path.
- 2026-10-25, agent: use Flow's Windows hands-free shortcut Ctrl+Win+Space.
  Keep native voice commands native by routing only physical Win+H input.
- 2026-10-25, agent: implement directly with focused native AutoHotkey checks
  and the existing Windows watcher/pedal test. No orchestration dispatch.
- 2026-10-25, agent: reserve isolated left Alt taps for the double-tap gesture
  by masking menu activation. Alt combinations and right Alt pass through.

## Authorizations and deferrals

- Owner requested pulling the latest repo and setting up the Windows equivalent
  of the Mac Wispr Flow setup. Then explicitly required repo-owned AutoHotkey
  source and Windows startup execution. This permits implementation, selecting
  Wispr and installing/reloading the requested startup script.
- Owner confirmed restoring Ctrl+Win+Space in Flow's shortcut settings.
- No push authorization. Recording and input-state tests require the owner's
  physical input. Talon was not running during initial process inspection.
- Preserve the pre-existing untracked control-dictation-shortcut record.
- Owner requested an Astra review: "when you're done with this could you advise
  with Astra ... if it thinks your solution is a good one." This authorizes one
  read-only Astra advisory/review agent for this implementation. No extra source
  writer or Git ownership is delegated.
- Owner subsequently requested "please commit and push". This supersedes the
  earlier no-push authorization state for this Windows effort and permits one
  commit/push to origin after review. Preserve unrelated work, integrate remote
  updates by merge when needed, and verify publication. The preceding phrase
  about "customer support to SA" was a dictation error. Owner clarified that
  they wanted instructions for switching providers; commands and guide supplied.

## Verification

- Pulled origin/main with `git pull --ff-only`, bd616178 to 1435cadd.
- Existing startup shortcut targets the repo's double_tap_control.ahk using
  installed AutoHotkey 1.1.37.02. Flow 1.6.1264 is installed and running.
- Restored shortcut independently confirmed in Flow's saved preferences as
  virtual keys 162+32+91, assigned to hands-free recording.
- Before the watcher change, the extended recording/pedal flow failed all eight
  new Wispr cases because recordings were not recognised. All 12 cases pass
  after registering Flow and extending Escape recovery.
- Final Python suite: 98 passed. Native AutoHotkey gesture checks and syntax
  parsing passed with the installed 1.1.37.02 runtime, without sending keys.
- The Windows selector test exercises real PowerShell 5.1 with isolated AppData.
  It caught a null-backup-path coercion in File.Replace; NullString fixes it.
  Switching providers survives new invocations; invalid input leaves state intact.
- Ruff passes for the new voice module and changed tests. Watcher lint compared
  with HEAD has no new findings, retaining two existing ISC002 and two SIM105.
  `git diff --check` passed. Source review found no additional changes needed.
- Selected wispr and launched the existing startup shortcut. The old instance
  was replaced, and only the requested repo-owned script was running. No disabled
  StartupApproved entry exists for the shortcut. A real login remains untested.
- Talon was closed and its log has no new entries. Its venv already contains
  comtypes 1.4.17. Live Talon loading and physical mic/gaze checks remain open;
  no automated keystrokes, recordings or input-state changes were performed.

## Resources

- Temporary environment and native check outputs were under the session's
  visualization directory, in windows-wispr-work. Removed after verification.
- Retain the installed AutoHotkey process for login shortcuts and provider
  selection in the user's AppData. These are requested runtime resources.

## Comments

- The watcher flow exercises capture detection, pause, automatic restore,
  manual pause preservation and divide-pedal recovery for Wispr. Existing tests
  only exercise Windows voice typing and Super Whisper; they cannot detect a
  missing Wispr process registration. No new production test seam is needed.
- At the initial setup checkpoint the source and documentation remained local
  and uncommitted. This was superseded by the owner's later commit/push request.

### Physical shortcut failure

- Owner reports the pedal produces Flow's "hold down Ctrl+Win" message.
  Manual Ctrl+Win+Space works, while double left Alt also fails. This isolates
  the failure to the generated Wispr chord shared by pedal and double Alt.
- Provider remains wispr and the requested AutoHotkey process is still running.
  Flow preferences still contain the correct hands-free shortcut.
- Ranked hypotheses: an instantaneous SendInput chord loses Space at Flow's
  input boundary; AutoHotkey alters modifiers; Flow filters injected input.
  Test timing first by using paced SendEvent with the same keys.
- Physical feedback is the regression check because project instructions require
  owner agreement before generated recording keys and owner input for dictation
  acceptance. Do not substitute a helper-only test for this transport failure.
- Paced SendEvent did not fix it. Owner clarified that Flow starts briefly, then
  closes immediately. A read-only 45-second key observer captured the pedal's
  physical Win+H and a complete paced generated Ctrl+Win+Space chord, plus extra
  injected Ctrl transitions before and after the chord. No text was captured.
- AutoHotkey's documented default menu-mask key is Ctrl. Around the intercepted
  physical Win+H it produces unwanted Ctrl+Win input, colliding with Flow's PTT
  shortcut. Change that mask to unassigned vkE8, preserving menu suppression.
- Temporarily selected windows to restore native routing during diagnosis, then
  selected wispr for the physical trace. Current provider is wispr.
- Temporary observer source and metadata trace live in the session visualization
  directory as wispr_key_probe.py/json. Observer exited and removed its hook.
  Remove its files and native parse outputs after verification.
- Owner confirmed after vkE8 masking: "Records, and it works" and "Yes,
  recording stayed on" for the pedal. Double Control also still starts native
  Windows dictation. Capture confirms the extra pre-chord Ctrl transitions are
  gone; complete recording toggles are emitted once per pedal press.
- Double left Alt still failed. The same observer saw only the script's
  injected Alt-up events, with no physical Alt-down delivered. AutoHotkey's
  up-only suppressing hotkey suppressed its unmatched down edge. Add explicit
  tilde/pass-through Alt-down so InputHook can recognise the gesture and normal
  Alt combinations retain their modifier event. Keep the proven output chord.
- Owner confirmed after the Alt-down fix: "Yes, double left Alt works" and
  "Double control still open regular windows dictation which it should".
  Final acceptance message: "everything seems to work now". Pedal and double
  left Alt now provide the requested latched start/finish behaviour.
- Final AutoHotkey syntax check passed before reloading the corrected source.
  No Python/runtime watcher changes were made after the 98-test passing run.
  The native observer completed and removed its hook; no diagnostic process
  remains. Live Talon mic/gaze and actual login checks remain separate gaps.
- Astra is reviewing the working candidate read-only as /root/astra_review.
  Source is frozen for the review; main remains at 1435cadd with local changes.
- Astra review completed. Verdict: the approach is sound and proportionate,
  with no concrete in-scope defect requiring a code change and no source-review
  blockers. Reviewer checked the tracked and untracked candidate against 1435cadd
  and all five supplied source hashes matched. No reviewer edits or resources.
  Keep menu masking, Alt-down pass-through and the paced chord together.
- Reviewer reiterated live Talon capture/mic/gaze/manual-pause/divide recovery,
  actual startup at login, ordinary Alt/AltGr shortcuts, selected-Windows pedal
  routing and Talon's injected native voice routing as remaining acceptance gaps.
  The owner has confirmed pedal, left Alt and Control; no broader live acceptance
  is inferred from mocked tests. These gaps do not block the authorized publication.
- Owner requested saving commands to the Desktop, then clarified they also
  wanted double-clickable controls. Installed three small .cmd wrappers calling
  the repo selector: Talon - Use Wispr, Talon - Use Windows Dictation, and Talon -
  Dictation Status. Updated Dictation provider commands.txt with their purpose
  and the literal PowerShell equivalents. Wrappers are host-local convenience
  files; repo source and the reviewed selector remain the execution path.
- Temporary observer source/metadata and native parse output files were removed.
  All owned diagnostic processes completed and unhooked. Retain only the requested
  startup AutoHotkey instance, provider choice and Desktop controls.
- Desktop status wrapper executed successfully with exit 0 and reported wispr.
  The selection wrappers were inspected without changing the owner's provider.
- Publication checkpoint: source review passed and origin/main still equals
  accepted base 1435cadd. Publish this reviewed Windows effort as one commit on
  main, excluding the pre-existing untracked control-dictation-shortcut record.
  Verify origin/main matches the resulting local commit after the authorized push.
