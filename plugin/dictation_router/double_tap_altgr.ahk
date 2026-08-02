; Double-tap AltGr -> start dictation.
;
; AutoHotkey v1.1 (installed at C:\Program Files\AutoHotkey\AutoHotkey.exe).
;
; Tapping AltGr twice quickly sends Win+H, opening Windows' voice typing pill.
;
; AltGr itself is never swallowed: the "~" prefix passes every press straight
; through to Windows, so AltGr+7 = { etc. keep working even if this script
; crashes or is not running.
;
; To disable: close it from the tray, and remove its shortcut from shell:startup.

#NoEnv
#SingleInstance Force
#InstallKeybdHook
SendMode Input
SetBatchLines -1

; ============================== CONFIG ===============================
; Max gap between the two taps, in ms. Raise if double-taps get missed.
DOUBLE_TAP_MS := 400

; A tap must be shorter than this, in ms. Holding AltGr never counts.
MAX_HOLD_MS := 500

; What to send on a double-tap. "#h" = Win+H, Windows voice typing.
TRIGGER := "#h"

; Set to true to log every AltGr event to %TEMP%\double_tap_altgr.log and beep
; on a detected double-tap. Useful if this ever stops firing.
DEBUG := false
; =====================================================================

LOG_FILE := A_Temp . "\double_tap_altgr.log"

comboUsed := false
altGrDownTime := 0
lastTapTime := 0

; A "~RAlt::" down-hotkey does NOT fire on AltGr layouts -- Windows delivers
; AltGr as LCtrl+RAlt and AHK never runs the down variant. So the key-down
; edge comes from this InputHook instead, which sees the raw event.
; The same hook tells "AltGr tapped alone" apart from "AltGr held as a
; modifier" (AltGr+7 = {, AltGr+2 = @, ...); without that, typing "{{" in JSX
; would look identical to a double-tap.
; "V" = visible: the hook only observes, it never suppresses keys.
ih := InputHook("V")
ih.KeyOpt("{All}", "N")
ih.OnKeyDown := Func("WatchKey")
ih.Start()
Log("--- started, InputHook.InProgress=" . ih.InProgress . " ---")
return

Log(msg) {
    global DEBUG, LOG_FILE
    if (DEBUG) {
        FormatTime, ts,, HH:mm:ss
        FileAppend, %ts% %msg%`n, %LOG_FILE%
    }
}

WatchKey(ih, VK, SC) {
    global comboUsed, altGrDownTime
    ; AltGr / RAlt going down: start the hold timer (ignore auto-repeat).
    if (VK = 0xA5) {
        if (!altGrDownTime) {
            altGrDownTime := A_TickCount
            comboUsed := false
            Log("AltGr down")
        }
        return
    }
    ; Ignore the phantom LCtrl that Windows synthesizes alongside AltGr,
    ; plus generic ctrl/alt, so they never count as a combo partner.
    if (VK = 0xA2 || VK = 0x11 || VK = 0x12)
        return
    ; Any real key pressed while AltGr is physically held means AltGr was
    ; used as a modifier, not tapped. Physical state is checked directly so
    ; this stays correct even if the down edge above is ever missed.
    if (GetKeyState("RAlt", "P")) {
        comboUsed := true
        Log(Format("  combo key during hold: VK={:X} SC={:X}", VK, SC))
    }
}

~RAlt up::
    ; held is 0 when the down edge was missed -- treat that as "not too long"
    ; rather than dropping the tap.
    held := altGrDownTime ? A_TickCount - altGrDownTime : 0
    gap := A_TickCount - lastTapTime
    wasCombo := comboUsed
    altGrDownTime := 0
    comboUsed := false
    Log("AltGr up  held=" . held . "ms gap=" . gap . "ms combo=" . wasCombo)
    ; Used as a modifier, or held down: not a tap. Reset the sequence.
    if (wasCombo || held > MAX_HOLD_MS) {
        lastTapTime := 0
        return
    }
    if (gap <= DOUBLE_TAP_MS) {
        lastTapTime := 0
        Log("  >>> DOUBLE TAP -- sending " . TRIGGER)
        if (DEBUG)
            SoundBeep, 1200, 120
        Send, %TRIGGER%
    } else {
        lastTapTime := A_TickCount
    }
return
