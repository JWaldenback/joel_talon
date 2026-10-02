# 01 Restore eye-mask commands on Talon 1.0

Status: done
Claimed by:
Blocked by:

## Problem

Since Talon 1.0.0, `talon.log` shows on every load of `plugin/mouse/mouse.py`:

    [mouse] eye_mouse_2 import failed (talon.plugins.eye_mouse_2); set_eye_mask disabled

The fallback then made `user.set_eye_tracking_mask` a no-op. As a result
`use both eyes` / `use only left eye` / `use only right eye`
(`core/my_customizations/eye_modes.talon`) did nothing, and neither did the eye
selection inside `gaze mode` ("both") and `hiss mode` ("left").

## Root cause

Talon 1.0's user-script import hook (`app\resources\init.py`, `import_hook`)
raises `ImportError('talon.plugins.eye_mouse_2')` for
`from talon.plugins.eye_mouse_2 import set_eye_mask`. This was confirmed with a
temporary diagnostic script in `talon/user/` (since removed). Talon itself
has the module loaded: `sys.modules["talon.plugins.eye_mouse_2"].set_eye_mask(mask: str)`
exists and backs the tray menu items `both_eyes_item` / `left_eye_item` /
`right_eye_item`. The registry has no `tracking.*` action or setting for the
eye mask; Talon only persists it internally as `sys.tracking.eye_mask`.

## Scope

- In: `plugin/mouse/mouse.py` eye-mask lookup.
- Out: asking Talon for a public API (possible follow-up), and the
  `eye_tracking_settings.py` zoom-mouse config (already fully commented out).

## Acceptance criteria

- [x] `mouse.py` loads on Talon 1.0 without the import-failure line.
- [x] `user.set_eye_tracking_mask("left")` switches Talon's tray menu to
      "Only Left Eye", and `"both"` switches it back.
- [x] If Talon no longer provides the function, the command prints and
      notifies instead of failing silently.

## Comments

2026-10-02, agent: implemented a call-time lookup through `sys.modules` in
`set_eye_mask` (`plugin/mouse/mouse.py`). Live check against the running
Talon 1.0.0 via `repl.bat`: before `left_eye_item.checked=False,
both_eyes_item.checked=True`; after `set_eye_tracking_mask("left")`
`True/False`; after `set_eye_tracking_mask("both")` restored `False/True`.
`talon.log` shows the clean reload. `python -m pytest`: 85 passed. ruff shows
no new findings (the one SIM105 at `_log_tracker_event` predates this change).
No unit test was added: the failure only exists under Talon's real import
hook, which the test stubs cannot reproduce, so a stub test would only prove
the mock.

Possible follow-up (needs-triage): ask in the Talon community for a public
eye-mask action so this stops relying on an internal function.
