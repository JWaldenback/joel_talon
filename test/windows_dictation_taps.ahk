; Run with AutoHotkey v1.1 /ErrorStdOut. This never installs hooks or sends keys.
#NoEnv
#Include %A_ScriptDir%\..\plugin\dictation_router\dictation_taps.ahk

for _, key in [0xA2, 0xA3, 0xA4] {
    taps := new DictationTaps()
    taps.Down(key, 1000)
    Check(!taps.Up(key, 1050), "single tap")
    taps.Down(key, 1150)
    Check(taps.Up(key, 1200), "double tap")
    taps.Down(key, 1250)
    Check(!taps.Up(key, 1300), "third tap must not retrigger")

    taps := new DictationTaps()
    taps.Down(key, 1000)
    taps.Up(key, 1050)
    taps.Down(0x41, 1100)
    taps.Down(key, 1150)
    Check(!taps.Up(key, 1200), "letter between taps")

    taps := new DictationTaps()
    taps.Down(key, 1000)
    taps.Down(0x41, 1020)
    Check(!taps.Up(key, 1050), "modifier shortcut")
    taps.Down(key, 1150)
    Check(!taps.Up(key, 1200), "tap after modifier shortcut")

    taps := new DictationTaps()
    taps.Down(key, 1000, true)
    taps.Up(key, 1050)
    taps.Down(key, 1150)
    Check(!taps.Up(key, 1200), "another modifier already held")

    taps := new DictationTaps()
    taps.Down(key, 1000)
    taps.Up(key, 1600)
    taps.Down(key, 1700)
    Check(!taps.Up(key, 1750), "long hold")

    taps := new DictationTaps()
    taps.Down(key, 1000)
    taps.Up(key, 1050)
    taps.Down(key, 1600)
    Check(!taps.Up(key, 1650), "expired first tap")
}

; The phantom Control paired with AltGr must never count as a Control tap.
taps := new DictationTaps()
taps.Down(0xA2, 1000)
taps.Down(0xA5, 1000)
Check(!taps.Up(0xA2, 1050), "AltGr")
taps.Down(0xA2, 1150)
taps.Down(0xA5, 1150)
Check(!taps.Up(0xA2, 1200), "double AltGr")
FileAppend, Gesture checks passed`n, *
ExitApp, 0

Check(condition, name) {
    if (!condition) {
        FileAppend, % "FAIL: " . name . "`n", **
        ExitApp, 1
    }
}
