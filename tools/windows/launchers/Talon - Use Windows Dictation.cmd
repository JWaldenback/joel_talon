@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0..\..\..\docs\windows\dictation-provider.ps1" windows
if errorlevel 1 (
    echo.
    echo Could not select Windows dictation. See the error above.
    pause
    exit /b 1
)
echo.
echo Windows dictation selected for the pedal and double left Alt.
timeout /t 2 /nobreak >nul
