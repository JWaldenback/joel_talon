"""Optional voice controls for the standalone Karabiner provider selector."""

import subprocess
from pathlib import Path

from talon import Module, app

mod = Module()


def _select(provider):
    # The extensionless helper is not loaded as Talon code. Its saved
    # Karabiner mapping keeps working after this app quits or restarts.
    helper = Path(__file__).resolve().parents[2] / "docs/macos/dictation-provider"
    result = subprocess.run(
        [str(helper), provider], capture_output=True, text=True, check=False
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip())
    app.notify(result.stdout.strip())


@mod.action_class
class Actions:
    def mac_dictation_provider_select(provider: str):
        """Select wispr or macos for the Karabiner pedal and keyboard toggle."""
        if app.platform != "mac":
            raise RuntimeError("The Karabiner dictation selector requires macOS")
        if provider not in {"wispr", "macos"}:
            raise ValueError("Choose wispr or macos")
        _select(provider)

    def mac_dictation_provider_status():
        """Show the provider saved in the selected Karabiner profile."""
        if app.platform == "mac":
            _select("status")
