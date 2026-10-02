# 03 Tobii USB reconnects stall Talon

Status: ready-for-human
Claimed by:
Blocked by:

## Problem

The Tobii 5 detaches and reattaches over USB 1–13 times a day, often exactly
every two hours at `:55:08` (e.g. 02:55, 04:55, 06:55, 18:55 on Sep 28).
Each event stalls Talon's cron thread for 4–12 s in Talon's own
`USBManager.on_hotplug` / `CameraMenu.on_attach|on_detach`. After a reattach,
`talon-usb` logs `event from missing stream N` ~33 times a second for hours.

## Why human

The likely fixes are system or vendor actions outside this repository:
USB selective-suspend / power management for the tracker's port or hub, a
different port or cable, finding what fires on the two-hour schedule, and
reporting the stall and log flood to Talon. These are system settings and
external reports, which the agent does not change or send on its own.

## Acceptance criteria

- [ ] Cause of the regular two-hour detach identified or ruled out.
- [ ] Detach count per day drops, checked with
      `grep "Tobii 5 detached" %APPDATA%\talon\talon.log*`.
- [ ] Optional: Talon report filed for the hotplug stall and the
      `event from missing stream` flood.
