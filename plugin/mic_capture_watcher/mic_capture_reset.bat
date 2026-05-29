@echo off
REM Sends user.mic_capture_reset() to the running Talon via its REPL.
REM
REM Executes immediately — no polling, no trigger files. talon_console.exe
REM connects to Talon over a per-user named pipe (\\.\pipe\talon_repl),
REM so this works without admin elevation provided Talon was started by
REM the same Windows user.

set "TALON_CONSOLE=C:\Program Files\Talon\talon_console.exe"

if not exist "%TALON_CONSOLE%" (
    echo ERROR: talon_console.exe not found at "%TALON_CONSOLE%".
    echo Edit mic_capture_reset.bat and update TALON_CONSOLE if your
    echo Talon install lives somewhere else.
    pause
    exit /b 1
)

echo actions.user.mic_capture_reset() | "%TALON_CONSOLE%" >nul
if errorlevel 1 (
    echo.
    echo Failed to reach Talon. Is it running?
    pause
    exit /b 1
)
echo Done.
timeout /t 1 /nobreak >nul
