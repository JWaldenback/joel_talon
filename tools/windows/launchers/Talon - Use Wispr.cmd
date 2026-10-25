@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0..\..\..\docs\windows\dictation-provider.ps1" wispr
if errorlevel 1 (
    echo.
    echo Could not select Wispr Flow. See the error above.
    pause
    exit /b 1
)
echo.
echo Wispr Flow selected for the pedal and double left Alt.
timeout /t 2 /nobreak >nul
