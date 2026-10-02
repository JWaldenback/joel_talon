# 01 Timing log for Win+H dictation starts

Status: in-review
Claimed by:
Blocked by:

## Outcome

`mic_and_eye_tracker_state.log` records enough to tell, for each pedal
press, whether the keystroke was delayed, whether Talon was stalled, and how
long Windows voice typing took to open, or that it never opened.

## Scope

- In: `plugin/mic_capture_watcher/dictation_timing.py` (new),
  `voice_dictation_resume.py` (feeds the hook, startup install, reload hygiene),
  `mic_capture_watcher.py` (tick gaps, `since_win_h_ms`), README.
- Out: changing how dictation starts or stops.

## Events

- `win_h_pressed`: `hook_delay_ms` (Windows' event timestamp to our hook,
  ~16 ms resolution), `injected` (AutoHotkey/SendInput vs physical device).
- `dictation_detected` / `dictation_cleared`: `since_win_h_ms`.
- `win_h_unanswered`: `reason` = `pressed_again` or `no_open_or_close` (3 s).
- `watcher_tick_gap`: `gap_ms` when the 300 ms watcher tick ran ≥ 1 s late.

## Acceptance criteria

- [x] Auto-repeat while the pedal is held logs a single press; H without Win
      and other Win+keys are ignored (`test/test_dictation_timing.py`).
- [x] Presses pair with the next open/close; repeated or unanswered presses
      and late ticks are logged (`test/test_dictation_timing.py`).
- [x] The hook installs in the running Talon (`_state["hook"]` set) and a
      reload does not leave a duplicate hook thread.
- [ ] A real pedal press produces `win_h_pressed` followed by
      `dictation_detected … since_win_h_ms=…` (owner presses the pedal).

## Comments

2026-10-02, agent: `python -m pytest`: 85 passed (83 before, plus 2 new).
ruff: no new findings in changed files (one pre-existing SIM102 in
`voice_dictation_resume.py` removed). Live: after the `GetModuleHandleW`
fix the hook installed (handle changes on each reload); after a forced reload
there was exactly one `voice_dictation_resume_hook` thread. Two
`dictation_timing_writer` threads from loads before the reload fix remain
idle until Talon restarts. No Win+H was sent by the agent, to avoid opening
dictation on the owner's machine.
