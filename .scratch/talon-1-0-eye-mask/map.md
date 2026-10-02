# Talon 1.0: eye-mask commands

Outcome: `use both eyes`, `use only left eye`, `use only right eye`, and the
eye selection made by `gaze mode` / `hiss mode` work again on Talon 1.0.

## Tickets

- [01 Restore eye-mask commands on Talon 1.0](issues/01-restore-eye-mask-commands.md): done.

## Decisions so far

- 2026-10-02, project default: decision policy agent-led.
- 2026-10-02, agent: call Talon's own `set_eye_mask` through `sys.modules`
  at call time instead of importing it. Reason: Talon 1.0 refuses the import
  from user scripts and offers no public action or setting for the eye mask.
  The function still drives Talon's own tray-menu items. Consequence: this
  depends on a Talon internal; if a future Talon renames it, the command
  prints and notifies instead of failing silently. Revisit when Talon exposes
  a public API (see ticket 01).

## Authorizations and deferrals

- 2026-10-02, owner in chat: "write a ticket and have that fixed". Scope: the
  eye-mask commands. Local commits allowed by project rules; push needs
  separate permission.
