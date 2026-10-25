# Mac dictation provider trial

Status: ready-for-human
Claimed by: none
Blocked by: physical confirmation of the reset-default Fn+Space route

## Outcome and scope

Select Wispr Flow or Apple Dictation for the existing Windows+H pedal and
double left Alt using Karabiner. Work with Talon closed. Keep double Control
native and right Alt/AltGr screenshot shortcuts intact. When Talon is running,
pause its microphone and gaze during Wispr recording, then restore them.

Robustness allowance: preserve unrelated Karabiner settings, save one original
profile snapshot, reject an invalid or concurrently edited profile, report
missing Wispr without silently starting native Dictation. No provider switching
during recording, no new service, no hardware programming changes.

## Decisions so far

- 2026-10-25, owner: pedal toggles; switching providers during recording is not
  part of supported use. Double Control stays native; double left Alt selects
  the configured provider. AltGr is reserved for existing screenshot tools.
- 2026-10-25, agent: provider choice is stored in one managed Karabiner rule,
  installed by an extensionless standalone selector. No Talon dependency or
  runtime-only selection variable, and no duplicated Karabiner profiles.
- 2026-10-25, agent: initially reuse Flow's existing Control+Space hands-free
  shortcut and Escape cancellation. Superseded below after the owner reset
  Flow's shortcuts to defaults. Optional Talon commands call the selector.
- 2026-10-25, agent: Orchestrate Light, agent-led, one source writer and one
  combined independent review. Stage source and tests outside Talon's live tree.

## Authorizations and deferrals

- Owner: "Go ahead and implement it, with Wispr selected for now. Keep double
  Control for Mac dictation and use double left Alt for the selected provider."
  Authorizes source changes and installation of these specific live rules.
- Owner will supply physical pedal/keyboard acceptance. No recorded audio or
  automated recording starts are required for software verification.
- Initial implementation had no push authorization. Superseded by the owner's
  later request: "can you commit and push and merge with main?" This authorizes
  committing the dictation implementation, integrating current origin/main by
  merge if necessary, and pushing main once verification passes. Do not change
  the shared dotagents workflow.

## Verification

- Base `f813baef`: 85 tests passed before changes.
- Existing watcher flow extended for both observed Wispr helper bundle IDs.
  Both new cases failed before the production fix, with Talon's mic still on.
- Focused selector/watcher checks: 8 passed on the initial candidate.
- Final staged and installed full suites: 89 passed. New Python files are ruff
  clean. Touched existing files retain only their original SIM105 and I001
  findings; no new lint findings. `git diff --check` passed.
- Installed Karabiner 16.3 linter accepted generated native and Wispr rules.
  Previewing against the actual profile preserved all fields outside the
  selected profile's managed rules. Generated notification shell syntax passed.
- Independent combined review found no actionable issues. Candidate manifest
  SHA256: `9b80731f6e020ee3c7762ae8db3e9790595d4b8a0a64fb0f5dea9f3351e80a35`.
- Installed source atomically while no known dictation process was recording.
  Talon log confirmed clean module reloads; read-only REPL confirmed both
  provider actions, Wispr watcher defaults, and native shortcut `ctrl ctrl`.
- Live Karabiner selector reports `wispr`; pre-change snapshot exists.
- Before the shortcut reset, owner confirmed **both pedal and double left Alt start/stop Wispr and insert
  text**. State log records dictation detection and release while retaining an
  existing manual Talon pause.
- Owner subsequently reported "Everything seems to work" in response to the
  Talon-closed/native-fallback acceptance check. Right Option alone has no
  visible action; the exact pre-existing screenshot shortcut is unverified.
  Source/config inspection confirms no right-Option or Control binding was
  added or changed. Investigating that unrelated app shortcut is deferred.

## Resources

- Removed the owned isolated source copy, test virtual environment, preview,
  generated lint file, and candidate manifest after acceptance. No lane process
  remains running. The final source and verification record remain in this repo.
- Retain the host-only pre-change Karabiner snapshot for rollback.

## Comments

- `git pull --ff-only` confirmed `joel_talon` was up to date and clean.
- User separately requested pulling `~/code/dotagents`. It fast-forwarded to
  `8f62f7f`, matching installed `~/.agents`. Neither shared copy was edited.

- Initial implementation completed locally with Wispr selected, without a
  commit or push at that point.

## Follow-up: match Wispr defaults

- Owner reset Flow's shortcuts to defaults to remove Command from activation
  and requested: "Can you make Carrabinor work with that?"
- UI inspection confirmed default push-to-talk is Fn and hands-free is
  Fn+Space. Karabiner still emitted Control+Space, explaining the mismatch.
- Extend the existing selector flow's independent shortcut contract to expect
  Fn+Space. Before the fix, it failed on the emitted `left_control` modifier.
- The fix changes the Wispr output only; native Dictation, pedal identity,
  double left Option recognition and right Option are unchanged.
- Updated installed Karabiner outputs for both pedal and double left Option
  to Fn+Space; selector still reports Wispr. Flow settings remain at defaults.
- Narrow independent review found no actionable issues; native Karabiner 16.3
  lint accepts the Fn modifier and rejects an invalid-modifier negative control.
- Final suite: 89 tests passed. All repo pre-commit hooks passed after their
  formatting and a behaviour-preserving `suppress(Exception)` replacement of
  the existing try/except/pass lint finding. The selector, provider-command,
  and selector-test ASTs are unchanged by formatting.
- The owner explicitly authorized commit, push and integration with main.
  The checked base and origin/main were `f813baef`; publish as one commit on
  main, merging any remote advance without rebasing. Remote publication is
  verified separately after the push.
- Pending: owner physical confirmation of the updated Fn+Space route. Earlier
  physical acceptance covered Control+Space, not this reset-default route.
- Temporary follow-up source, venv, pre-commit environments and lint artifact
  are owned by Codex and removed at the end of this publishing turn.
