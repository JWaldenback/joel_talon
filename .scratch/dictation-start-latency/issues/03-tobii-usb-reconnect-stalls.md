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

- [x] Cause of the regular detaches identified (Modern Standby DRIPS mitigation; see Comments).
- [ ] Detach count per day drops, checked with
      `grep "Tobii 5 detached" %APPDATA%\talon\talon.log*`.
- [ ] Optional: Talon report filed for the hotplug stall and the
      `event from missing stream` flood.

## Comments

2026-10-02, agent: cause found. The detaches are Windows Modern Standby's
"DRIPS blocking device" mitigation. While the PC is idle or asleep, Windows
flags the Tobii (`VID 0x2104 PID 0x313`) as draining power (System log,
`Microsoft-Windows-USB-USBHUB3` event 196) and on wake port-cycles it
(event 205). Talon's `Tobii 5 detached` lines follow event 205 within
seconds (e.g. 2026-09-30 05:07:44 → 05:07:48, 14:04:40 → 14:04:44,
2026-10-01 11:22:23 → 11:22:23). 53 such Tobii events in 8 days. At
14:17:35 on 2026-10-02 the port cycle left the tracker absent from Windows
entirely (blinking, not enumerated) until replugged, so gaze mode stopped working.
Owner-side fixes to try (system settings, so the owner applies them): in
Device Manager, untick "Allow the computer to turn off this device to save
power" on the Tobii's USB Composite Device and its parent hub; disable USB
selective suspend in the power plan; or plug the tracker directly into the
PC instead of the USB4 dock/hub.
