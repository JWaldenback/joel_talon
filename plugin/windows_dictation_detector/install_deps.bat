@echo off
REM Installs the Python dependencies needed by the windows_dictation_detector
REM plugin into Talon's bundled Python.
REM
REM Run this once after cloning. Re-run if the dependency list changes.

set "TALON_PY=C:\Program Files\Talon\python.exe"

if not exist "%TALON_PY%" (
    echo Could not find Talon's Python at "%TALON_PY%".
    echo Edit install_deps.bat and adjust TALON_PY to point at your Talon install.
    exit /b 1
)

echo Installing comtypes into Talon's Python...
"%TALON_PY%" -m pip install --upgrade comtypes
if errorlevel 1 (
    echo.
    echo Install failed. You may need to run this script as Administrator,
    echo since Talon is installed under "Program Files".
    exit /b 1
)

echo.
echo Done. Restart Talon to pick up the new package.
