# Portable Windows tools

Status: done
Claimed by: none
Blocked by: none

## Outcome and scope

Keep a discoverable catalog and runnable Windows controls in the repo, with
one setup command for a replacement PC. Include the AutoHotkey helpers and
the three dictation provider controls created in the preceding effort.

Robustness allowance: validate the required source files and installed
AutoHotkey 1.1 before writing shortcuts. Repeated installation updates the
same managed shortcut names without touching unrelated Desktop/startup files.
Do not launch recording, change provider selection or install third-party apps.

## Decisions so far

- 2026-10-25, agent: keep runnable source in tools/windows and link the existing
  plugin sources rather than moving them. Desktop shortcuts point to repo-owned
  commands so updating the repo also updates their implementation.
- 2026-10-25, agent: install controls in a Desktop folder named Talon tools and
  reuse the existing startup filename. Mark the old AltGr helper as optional,
  because automatically enabling it would conflict with right-Alt shortcuts.

## Authorizations and deferrals

- Owner asked to save Talon executables in the repo so a new PC is easier to
  set up and the available tools are easier to identify. Owner added that the
  AutoHotkey files are good candidates. This covers the catalog, runnable
  wrappers, installer and installation on the current machine.
- The preceding effort's one authorized push completed as aaebe714. This
  follow-up has no new push authorization. Preserve the unrelated untracked
  control-dictation-shortcut record.

## Verification

- Started from aaebe714; git pull --ff-only reported already up to date.
- Full suite: 99 passed. The installer flow ran native Windows PowerShell 5.1,
  copied the real tools to a checkout path containing spaces, installed twice,
  read real .lnk metadata, checked the AutoHotkey startup target/arguments, and
  executed the linked status control. Choice and unrelated files were preserved.
  Missing AutoHotkey failed before any destination was created.
- Corrected one lint-only environment-variable spelling in the new test;
  focused installer test passed again. Ruff reports no findings for that file.
  `git diff --check` passes. No Talon load errors appeared after adding the
  guarded test file; runtime Talon input and AutoHotkey source were not changed.
- Ran the real installer successfully on this PC. The Desktop Talon tools
  folder has the five expected links, with source targets in this repo. The
  established startup link points at AutoHotkey 1.1 and the existing script.
  Provider choice was compared before/after and remains unchanged.

## Resources

- Session-owned temporary Desktop/startup folders and the test environment
  under windows-tools-check were removed after verification. Retain the real Desktop
  links and existing startup entry. Do not start another AutoHotkey process.

## Comments

- Existing active helper is plugin/dictation_router/double_tap_control.ahk.
  Its adjacent dictation_taps.ahk is a library, not another background app.
  The old double_tap_altgr.ahk is optional and is not enabled by this setup.
- One native installation flow test protects the new-PC contract: a checkout
  with spaces installs and reinstalls valid Windows links, preserves unrelated
  files and provider selection, and executes the real linked status control.
  Existing provider/watcher tests do not cover shortcut installation. It uses
  the installer's actual destination parameters; no test-only runtime seam.
- Source inspection confirmed repeat installation only saves its managed .lnk
  names, no source copies or new services. Original loose Desktop controls and
  unrelated content are preserved. Guide links use Notepad so a replacement PC
  needs no Markdown file association. No additional backward-compatibility path.
- Outcome: catalog, runnable controls and installer are complete locally. Commit
  this effort as a separate checkpoint. A fresh push needs owner authorization
  under docs/agents/project.md's ask-before-every-push rule.
