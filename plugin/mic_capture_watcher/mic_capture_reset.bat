@echo off
REM Triggers Talon's user.mic_capture_reset() action.
REM
REM Use this if mic_capture_watcher leaves Talon's speech engine stuck
REM disabled and voice commands aren't responding. Double-click this
REM file and Talon should re-enable speech within ~1 second.
REM
REM How it works: this script creates a trigger file in %TEMP%.
REM mic_capture_reset_trigger.py polls every 1 second and runs the
REM reset action when it sees the trigger, then deletes the file.

set "TRIGGER=%TEMP%\mic_capture_reset.trigger"
type nul > "%TRIGGER%"

echo Trigger created at %TRIGGER%.
echo Waiting for Talon to pick it up...
timeout /t 3 /nobreak >nul

if exist "%TRIGGER%" (
    echo.
    echo WARNING: Trigger file is still present after 3 seconds.
    echo Is Talon running and the mic_capture_watcher plugin loaded?
    echo You can manually delete the trigger file if needed.
    pause
) else (
    echo Done. Talon speech and mouse have been reset.
    timeout /t 2 /nobreak >nul
)
