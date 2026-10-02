# 02 Analyze collected timing data

Status: blocked
Claimed by:
Blocked by: 01, and a few days of normal pedal use

## Outcome

A data-backed answer to "why does the pedal sometimes not start dictation":
the share of slow or missed starts caused by (a) a delayed keystroke
(`hook_delay_ms`), (b) a Talon stall (`watcher_tick_gap` around the press),
(c) Windows voice typing itself (large `since_win_h_ms` with no stall), or
(d) a second press closing a pill that was still opening (`pressed_again`
followed by a short session). Then recommend fixes for the dominant cause.

## Acceptance criteria

- [ ] Per-cause counts and latency distribution over the collection window.
- [ ] Correlation with `talon.log` watchdog stalls and Tobii attach/detach.
- [ ] Recommendation recorded in the map, with follow-up tickets if warranted.
