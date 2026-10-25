@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0..\..\..\docs\windows\dictation-provider.ps1" status
if errorlevel 1 (
    echo.
    echo Could not read the dictation provider. See the error above.
    pause
    exit /b 1
)
echo.
echo The provider above is used by the pedal and double left Alt.
pause
