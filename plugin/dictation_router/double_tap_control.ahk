; Double-tap either Control key to start Windows voice typing.
;
; AutoHotkey v1.1. Run this script instead of double_tap_altgr.ahk if you
; want Control to be the dictation shortcut. Both scripts can also run together.
; Normal Control presses and shortcuts pass through unchanged.
;
; To disable: close it from the tray, and remove its shortcut from shell:startup.

#NoEnv
#SingleInstance Force
#InstallKeybdHook
SendMode Input
SetBatchLines -1

; Maximum gap between taps and maximum length of each tap, in milliseconds.
DOUBLE_TAP_MS := 400
MAX_HOLD_MS := 500

; Win+H opens Windows voice typing.
TRIGGER := "#h"

; Log key events to %TEMP%\double_tap_control.log and beep on a double-tap.
DEBUG := false
LOG_FILE := A_Temp . "\double_tap_control.log"

controlDownTime := 0
controlKey := 0
comboUsed := false
lastTapTime := 0

; Observe key-down events without suppressing them. This distinguishes a tap
; from Control held for another key and from the synthetic left Control that
; Windows sends with AltGr on some keyboard layouts.
ih := InputHook("V")
ih.KeyOpt("{All}", "N")
ih.OnKeyDown := Func("WatchKey")
ih.Start()
return

Log(msg) {
    global DEBUG, LOG_FILE
    if (DEBUG) {
        FormatTime, ts,, HH:mm:ss
        FileAppend, %ts% %msg%`n, %LOG_FILE%
    }
}

WatchKey(ih, VK, SC) {
    global controlDownTime, controlKey, comboUsed

    if (VK = 0xA2 || VK = 0xA3) {  ; left or right Control
        if (!controlDownTime) {
            controlDownTime := A_TickCount
            controlKey := VK
            comboUsed := GetKeyState("RAlt", "P")
            Log("Control down VK=" . VK)
        } else if (VK != controlKey) {
            comboUsed := true  ; both Control keys held together
        }
        return
    }

    ; Ignore the generic Control event, but count every other key (including
    ; AltGr/RAlt) pressed while Control is physically held as a shortcut.
    if (VK != 0x11 && (GetKeyState("LControl", "P") || GetKeyState("RControl", "P"))) {
        comboUsed := true
        Log("  combo key VK=" . VK)
    }
}

~*LControl up::
    HandleControlUp(0xA2)
return

~*RControl up::
    HandleControlUp(0xA3)
return

HandleControlUp(VK) {
    global controlDownTime, controlKey, comboUsed, lastTapTime
    global DOUBLE_TAP_MS, MAX_HOLD_MS, TRIGGER, DEBUG

    if (VK != controlKey)
        return

    held := controlDownTime ? A_TickCount - controlDownTime : 0
    gap := A_TickCount - lastTapTime
    wasCombo := comboUsed || GetKeyState("RAlt", "P")
    controlDownTime := 0
    controlKey := 0
    comboUsed := false
    Log("Control up VK=" . VK . " held=" . held . "ms gap=" . gap . "ms combo=" . wasCombo)

    if (wasCombo || held > MAX_HOLD_MS) {
        lastTapTime := 0
        return
    }
    if (gap <= DOUBLE_TAP_MS) {
        lastTapTime := 0
        Log("  double tap: sending " . TRIGGER)
        if (DEBUG)
            SoundBeep, 1200, 120
        Send, %TRIGGER%
    } else {
        lastTapTime := A_TickCount
    }
}
