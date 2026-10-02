# Project settings

## Decisions and models

Decision policy: agent-led.
Model research: on-demand.
Model evidence maximum age: 14 days.

Explicit task choices override these defaults. Record effort-specific model
pairings and authorizations in the tracker. Add standing model preferences only
when the owner has supplied them.

## Repository boundaries

This is the owner's personal Talon user file set: a fork
(`origin` = `JWaldenback/joel_talon`) of the community command set
(`upstream` = `talonhub/community`). It lives inside the running Talon user
directory (`%APPDATA%\talon\user\joel_talon` on Windows), so it is the owner's
daily voice, eye-tracker, and pedal input system, used on Windows and macOS
([MACOS_SUPPORT.md](../../MACOS_SUPPORT.md), [docs/macos](../macos/README.md)).

- Owner customizations: `core/my_customizations/`, `plugin/my_customizations/`,
  `apps/my_customizations/`, `plugin/mic_capture_watcher/` (Windows/macOS
  dictation and mic/eye-tracker pause coordination, see its
  [README](../../plugin/mic_capture_watcher/README.md)), `plugin/dictation_router/`,
  and owner edits in `plugin/mouse/mouse.py`.
- Everything else tracks upstream. Keep changes there minimal so upstream
  merges stay easy; upstream conventions are in [CONTRIBUTING.md](../../CONTRIBUTING.md)
  and [PRACTICES.md](../../PRACTICES.md).
- `private/`, `stored_state/` and the per-host lists in `.gitignore` are local
  data and stay out of Git.

## Verification

- Unit tests: `python -m pytest` from the repository root (pytest 9.0.3 per
  [requirements-dev.txt](../../requirements-dev.txt); `pyproject.toml` puts
  `test/stubs` on the path). pytest is not installed globally on the Windows
  host; use a throwaway virtual environment.
- Lint: ruff per `pyproject.toml`, and `pre-commit run --all-files` per
  [.pre-commit-config.yaml](../../.pre-commit-config.yaml). Neither tool is
  installed globally on the Windows host. The tree has pre-existing ruff
  findings; judge changes by not adding new ones.
- Live check (required for behavior that only Talon can exercise): Talon
  reloads files on save. Read `%APPDATA%\talon\talon.log` for load errors and
  `%APPDATA%\talon\mic_and_eye_tracker_state.log` for mic, eye-tracker, and
  dictation events. Read-only queries against the running Talon can go
  through `%APPDATA%\talon\venv\3.14\Scripts\repl.bat`, one expression per
  invocation via stdin. Pedal, dictation, and eye-tracker behavior needs the
  owner's physical input to confirm.

## Shared resources

- The running Talon instance. Every save reloads it immediately, and a broken
  file breaks the owner's voice control until fixed. Write each file in one
  complete edit, check `talon.log` after saving, and fix load errors at once.
- The owner's microphone, eye tracker, and Windows dictation. Do not send
  keystrokes such as Win+H, mute or switch the microphone, or change tracker
  state without the owner's agreement; restore any state changed for
  verification.
- One agent edits the checkout at a time; it is the live Talon directory, not
  a disposable worktree.

## Release and external actions

There is no release process. Publishing means pushing to `origin`, which
needs the owner's explicit permission for each push (see below). Never push
to `upstream`.

## Current owner decisions

Standing owner rules (moved verbatim from `CLAUDE.md` on 2026-10-02 so every
agent reads them):

### Git

- **Always merge, never rebase** when pulling from upstream or integrating
  parallel work. Use `git merge upstream/main` (or equivalent) and accept the
  merge commit. Rationale: I want individual commits to stay distinct in the
  history, not blended into a linear sequence. Rebase rewrites commit SHAs
  and forces a force-push, which I don't want. When the shared base's
  `git pull --ff-only` cannot fast-forward, merge instead.

- **Don't push to any remote without explicit permission.** Stop after the
  commit lands locally and ask before running `git push`. Same applies to
  any push variant (`--force`, `--force-with-lease`, etc.).

### Code style

- **Don't add comments to `.talon` files without asking first.** They're
  voice-command grammar files; I want them to stay minimal and read like
  a clean list of commands. If you think a comment is genuinely needed
  (e.g. to explain why a command is disabled), check with me before
  adding it.

- **Comments in `.py` files are fine and encouraged** when you're adding
  new logic, non-obvious control flow, or anything that needs context
  for future-me to understand. Default to keeping them.
