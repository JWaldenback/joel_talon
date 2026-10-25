; Windows dictation provider shortcuts, independent of Talon.
; The existing Windows startup shortcut runs this repo-owned script.
; Win+H and double left Alt use the saved provider; double Control stays native.
; Run docs/windows/dictation-provider.ps1 to select wispr or windows.

#NoEnv
#SingleInstance Force
#InstallKeybdHook
; The default Ctrl menu mask also matches Flow's Ctrl+Win push-to-talk.
; Use an unassigned key to suppress Start/menu activation without recording.
#MenuMaskKey vkE8
#Include %A_ScriptDir%\dictation_taps.ahk
SendMode Input
SetBatchLines -1

PROVIDER_FILE := A_AppData . "\TalonDictation\provider.txt"
taps := new DictationTaps()

; Only observe key-down events here. The up hotkeys below handle dispatch.
; I1 ignores this script's level-zero SendEvent output as well as SendInput,
; preventing the paced Wispr chord from entering the modifier-tap detector.
; L0 disables text collection; only key notifications are needed.
ih := InputHook("V I1 L0")
ih.KeyOpt("{All}", "N")
ih.OnKeyDown := Func("WatchKey")
ih.Start()
return

WatchKey(ih, vk, sc) {
    global taps
    ; The hook reports sided modifiers. Ignore their generic counterparts.
    if (vk = 0x11 || vk = 0x12)
        return
    taps.Down(vk, A_TickCount, OtherModifierHeld(vk))
}

OtherModifierHeld(vk) {
    for _, key in [0xA0, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5, 0x5B, 0x5C] {
        if (key != vk && GetKeyState(Format("vk{:X}", key), "P"))
            return true
    }
    return false
}

~*LControl up::
    if (taps.Up(0xA2, A_TickCount, OtherModifierHeld(0xA2)))
        SendInput, #h
return

~*RControl up::
    if (taps.Up(0xA3, A_TickCount, OtherModifierHeld(0xA3)))
        SendInput, #h
return

; An up-only suppressing hotkey also suppresses its unmatched down event.
; Explicitly pass down through so InputHook sees the first edge of each tap
; and ordinary Alt combinations still reach the foreground application.
~*LAlt::
return

$*LAlt up::
    ; Pass Alt combinations through, but prevent isolated left Alt taps
    ; from opening an application's menu before the dictation shortcut.
    ; Right Alt/AltGr is never intercepted.
    if (taps.keys[0xA4].down && !taps.keys[0xA4].used)
        SendInput, {Blind}{vkE8}{LAlt up}
    else
        SendInput, {Blind}{LAlt up}
    if (taps.Up(0xA4, A_TickCount, OtherModifierHeld(0xA4)))
        ToggleSelectedProvider()
return

; The pedal sends physical Win+H. Leave Talon's injected native-dictation
; voice commands alone. The $ hook also keeps our native SendInput from
; re-entering this hotkey. Wait for release so a held pedal toggles once.
#If GetKeyState("LWin", "P") || GetKeyState("RWin", "P")
$#h::
    KeyWait, h
    KeyWait, LWin
    KeyWait, RWin
    ToggleSelectedProvider()
return
#If

ToggleSelectedProvider() {
    global PROVIDER_FILE
    if (!FileExist(PROVIDER_FILE)) {
        provider := "windows"
    } else {
        FileRead, provider, %PROVIDER_FILE%
        if (ErrorLevel) {
            TrayTip, Dictation unavailable, Cannot read the saved provider., 5, 2
            return
        }
        provider := Trim(provider, " `t`r`n")
    }
    if (provider = "windows") {
        SendInput, #h
    } else if (provider = "wispr") {
        Process, Exist, Wispr Flow.exe
        if (!ErrorLevel) {
            TrayTip, Dictation unavailable, Open Wispr Flow and try again., 5, 2
            return
        }
        ; Pace the full hands-free combination so Space is held alongside
        ; both modifiers before any of them are released. The vkE8 menu mask
        ; above prevents extra Ctrl+Win presses around this intended chord.
        ; Flow itself owns the recording state for the start/finish toggle.
        SetKeyDelay, 30, 30
        SendEvent, {LControl down}{LWin down}{Space down}{Space up}{LWin up}{LControl up}
    } else {
        TrayTip, Dictation unavailable, Select wispr or windows with the provider selector., 5, 2
    }
}
