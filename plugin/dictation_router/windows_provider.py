"""Optional voice controls for the standalone Windows provider selector."""

import subprocess
from pathlib import Path

from talon import Module, app

mod = Module()


def _select(provider):
    # AutoHotkey reads this saved choice even when Talon is closed. Invoke
    # the same standalone selector used from a Windows terminal.
    helper = Path(__file__).resolve().parents[2] / "docs/windows/dictation-provider.ps1"
    result = subprocess.run(
        [
            "powershell.exe",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(helper),
            provider,
        ],
        capture_output=True,
        text=True,
        check=False,
        creationflags=subprocess.CREATE_NO_WINDOW,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip())
    app.notify(result.stdout.strip())


@mod.action_class
class Actions:
    def windows_dictation_provider_select(provider: str):
        """Select wispr or windows for the pedal and double left Alt."""
        if app.platform != "windows":
            raise RuntimeError("The Windows dictation selector requires Windows")
        if provider not in {"wispr", "windows"}:
            raise ValueError("Choose wispr or windows")
        _select(provider)

    def windows_dictation_provider_status():
        """Show the provider saved for Windows AutoHotkey shortcuts."""
        if app.platform == "windows":
            _select("status")
