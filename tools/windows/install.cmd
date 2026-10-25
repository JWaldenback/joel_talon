@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1"
if errorlevel 1 (
    echo.
    echo Setup did not complete. See the error above.
    pause
    exit /b 1
)
echo.
echo Setup complete. Open the Talon tools folder on your Desktop.
pause
