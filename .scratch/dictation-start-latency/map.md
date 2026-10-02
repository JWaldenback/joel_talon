# Slow or missed Win+H dictation starts from the foot pedal

Outcome: understand, then reduce, the cases where pressing the foot pedal
(which sends Win+H directly; Talon does not bind it) does not start Windows
voice typing, or starts it seconds late after repeated presses.

## Tickets

- [01 Timing log for Win+H dictation starts](issues/01-timing-log.md): done.
- [02 Analyze collected timing data](issues/02-analyze-timing-data.md): blocked by 01 and a few days of data.
- [03 Tobii USB reconnects stall Talon](issues/03-tobii-usb-reconnect-stalls.md): ready-for-human.

## Findings so far (2026-10-02)

Facts from `%APPDATA%\talon\talon.log*` (Sep 26 – Oct 2) and
`mic_and_eye_tracker_state.log` (since Aug 21):

- The watcher's capture-session poll costs about 2 ms per run (measured
  standalone, 40 runs), so it is not the slowdown.
- Talon's cron/main thread stalls 2–12 s about 260 times (`[watchdog] … (stalled)`).
  The biggest source is the Tobii USB detach/attach (`USBManager.on_hotplug`,
  `CameraMenu.on_attach/on_detach`, Talon 1.0's new Camera menu), 1–13 times
  a day, often exactly every two hours at `:55:08`. Smaller stalls come from
  user-file reloads (`fs_shadow`).
- After a Tobii reattach, `talon-usb` logs `event from missing stream N`
  about 33 times a second for hours (~119k lines/hour; one log reached 52 MB).
- 3–5% of Win+H sessions close within 0.4–1.7 s and reopen within 8 s,
  consistent with a second Win+H toggling a pill that was still opening.
- Hypothesis, not yet proven: a press during a Talon stall is delayed
  because Talon's low-level keyboard hooks sit in the key-delivery path, even
  though Talon does not handle Win+H. Ticket 01 measures this.
- Eye tracker staying on during a Talon pause: caused by Talon 1.0's
  "Always On" eye-tracking option (`sys.tracking.control.always_on = true`).
  Replaying the state log showed no case of Control Mouse left on while
  paused. The owner asked whether to keep it; the agent recommended keeping
  it on (see Authorizations and deferrals).

## Decisions so far

- 2026-10-02, project default: decision policy agent-led.
- 2026-10-02, agent: put the timing capture in the existing low-level
  keyboard hook (`voice_dictation_resume.py`) rather than a second hook, and
  install that hook at startup while `user.dictation_timing_log_enabled` is
  on (default on). Consequence: one Python hook sees every keystroke
  system-wide. It only filters and enqueues; a writer thread does the file
  I/O, so Talon stalls neither delay the hook's work nor skew log timestamps.
  Turn the setting off to restore lazy installation.
- 2026-10-02, agent: fixed `GetModuleHandleW` missing `restype` in
  `voice_dictation_resume.py`. Without it the 64-bit handle was truncated and
  `SetWindowsHookExW` failed with error 126, so the existing "start listening →
  any keypress resumes Talon" hook never installed either.

## Authorizations and deferrals

- 2026-10-02, owner in chat: "you can add that small timing log". Scope:
  logging only; no behavior change to dictation. Local commits allowed by
  project rules; push needs separate permission.
- 2026-10-02, pending owner choice: whether to keep Talon's "Always On" eye
  tracking. Agent recommendation: keep it on unless ticket 02 links it to the
  stalls; the pause still turns Control Mouse off.
