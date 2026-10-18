# Project settings

## Decisions and models

Decision policy: agent-led.
Model research: on-demand.
Model evidence maximum age: 14 days.

Explicit task choices override these defaults. Record effort-specific model
pairings and authorizations in the tracker. Add standing model preferences only
when the owner has supplied them.

## Working rules

- Start from the latest commit: `git pull --ff-only`, merging when it cannot
  fast-forward (owner rule below).
- Agent-led means: make routine implementation and design choices yourself
  and record significant ones in the effort record. Ask the owner before
  anything hard to reverse, outside the agreed scope, or contradicting a
  stated requirement.
- Build for the installed Talon version. Support for older Talon versions,
  legacy data formats, or parallel old/new code paths needs the owner's
  approval first.
- Keep the change within the task. Record unrelated findings as separate
  `.scratch/` follow-ups.
- Test sparingly and at the feature level. A good test drives a whole user
  flow through the real modules, the way `test/test_windows_dictation_pedal.py`
  runs a pedal press through the watcher and the pause toggle. Add one when it
  protects behavior that could credibly regress, and check that it fails
  without the fix. One flow-level test beats several tests of small helpers.
  Behavior only Talon can exercise gets a live check instead (see
  Verification).

## Repository boundaries

The owner's personal Talon user file set: a fork (`origin`,
`JWaldenback/joel_talon`) of the community command set (`upstream`,
`talonhub/community`), used daily on Windows and macOS. Most owner code sits
in `my_customizations` folders and `plugin/mic_capture_watcher/`, but owner
edits also live inside upstream files; `git diff upstream/main --stat` shows
the full divergence. Keep edits to upstream files small so upstream merges
stay easy, and in merge conflicts keep the owner's customizations while adding
upstream's changes alongside them.

## Live Talon directory

The checkout is the running Talon user directory (Windows
`%APPDATA%\talon\user\joel_talon`, macOS `~/.talon/user/joel_talon`). It is
**live**: Talon loads every `.py` and `.talon` file anywhere inside it the
moment it is saved, and a broken file breaks the owner's voice control.

- Write each file in one complete edit, then check `talon.log` for load errors
  and fix them at once.
- One agent edits the live checkout at a time. Parallel lanes, temporary
  scripts, and git worktrees go outside the Talon user directory (for example
  the session scratchpad); inside it Talon loads them as code.
- Test files load too, so each `test/*.py` wraps its body in
  `if hasattr(talon, "test_mode"):` like the existing tests.
- The microphone, eye tracker, and Windows dictation are the owner's live
  input. Get the owner's agreement before sending keystrokes such as Win+H or
  changing mic or tracker state, and restore anything changed for a check.

Talon 1.0 gotchas:

- The user-script import hook rejects `talon.plugins.*` imports even when
  Talon has loaded the module; prefer `actions.*` and `settings`, and see
  `set_eye_mask` in `plugin/mouse/mouse.py` for the fallback when none exists.
- Threads a user script starts keep running after a reload. Name them and stop
  the previous module's thread when starting a new one, as
  `plugin/mic_capture_watcher/voice_dictation_resume.py` does.
- Python is 3.14 free-threaded. Give every ctypes function returning a handle
  an explicit `restype`; the default C int truncates 64-bit handles.

## Verification

- Tests: `python -m pytest` from the repository root. pytest is not installed
  globally on the Windows host; use a throwaway virtual environment with
  `requirements-dev.txt`.
- Lint: ruff and `pre-commit` per the repository config, also not installed
  globally. The tree has pre-existing ruff findings; changed files must add
  none.
- Live check, for behavior only Talon exercises:
  - `talon.log` and `mic_and_eye_tracker_state.log` in the Talon home
    (`%APPDATA%\talon`, macOS `~/.talon`). The state log records mic,
    eye-tracker, dictation, and Win+H timing events.
  - Read-only queries via the Talon REPL (`venv\3.14\Scripts\repl.bat` under
    the Windows Talon home, `~/.talon/bin/repl` on macOS), piping one
    expression per invocation on stdin; wrap statements in `exec("...")`.
  - Pedal, dictation, and eye-tracker behavior needs the owner's physical
    input to confirm.

## Release and external actions

No release process. Publishing is a push to `origin`, governed by the push
rule below.

## Current owner decisions

Standing owner rules (moved from `CLAUDE.md` on 2026-10-02):

- **Merge, never rebase**, when pulling from upstream or integrating parallel
  work: `git merge upstream/main` (or equivalent), accepting the merge commit.
  When the shared base's `git pull --ff-only` cannot fast-forward, merge.
  Rationale: individual commits stay distinct in the history, and no SHA
  rewrite forces a force-push.
- **Ask before every push.** Stop once the commit lands locally and get
  explicit permission before any `git push` variant (`--force`,
  `--force-with-lease`, etc.).
- **`.talon` files hold only commands.** They are voice-command grammar and
  should read as a clean list. When a comment seems genuinely needed (e.g. why
  a command is disabled), ask the owner first.
- **Comment `.py` files generously** for new logic, non-obvious control flow,
  or context future-me needs. Keep existing comments.
