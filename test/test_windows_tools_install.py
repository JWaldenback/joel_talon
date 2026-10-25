import talon

if hasattr(talon, "test_mode"):
    import json
    import os
    import shutil
    import subprocess
    import sys
    from pathlib import Path

    import pytest

    @pytest.mark.skipif(
        sys.platform != "win32", reason="Windows shortcuts and PowerShell"
    )
    def test_new_pc_tools_installation_preserves_choice_and_reinstalls(tmp_path):
        ahk = Path(os.environ["PROGRAMFILES"]) / "AutoHotkey/AutoHotkey.exe"
        if not ahk.is_file():
            pytest.skip(
                "Installed AutoHotkey 1.1 is needed for the native installer check"
            )

        repo = Path(__file__).parents[1]
        clone = tmp_path / "New checkout with spaces"
        shutil.copytree(repo / "tools/windows", clone / "tools/windows")
        for relative in (
            "docs/windows/dictation-provider.ps1",
            "plugin/dictation_router/double_tap_control.ahk",
            "plugin/dictation_router/dictation_taps.ahk",
        ):
            destination = clone / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(repo / relative, destination)

        desktop, startup, appdata = (
            tmp_path / name for name in ("Desktop", "Startup", "AppData")
        )
        for directory in (desktop, startup, appdata / "TalonDictation"):
            directory.mkdir(parents=True)
        (desktop / "keep.txt").write_text("Keep desktop content")
        (startup / "keep.txt").write_text("Keep startup content")
        choice = appdata / "TalonDictation/provider.txt"
        choice.write_bytes(b"wispr\n")
        env = {
            **os.environ,
            "APPDATA": str(appdata),
            "TOOLS_DESKTOP": str(desktop),
            "TOOLS_STARTUP": str(startup),
        }

        def powershell(*arguments):
            return subprocess.run(
                [
                    "powershell.exe",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    *arguments,
                ],
                env=env,
                input="\n",
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
                timeout=20,
            )

        install = clone / "tools/windows/install.ps1"
        for _ in range(2):
            result = powershell(
                "-File",
                str(install),
                "-DesktopDirectory",
                str(desktop),
                "-StartupDirectory",
                str(startup),
                "-AutoHotkeyPath",
                str(ahk),
            )
            assert result.returncode == 0, result.stderr
        assert choice.read_bytes() == b"wispr\n"
        assert (desktop / "keep.txt").read_text() == "Keep desktop content"
        assert (startup / "keep.txt").read_text() == "Keep startup content"
        assert len(list(startup.glob("*.lnk"))) == 1
        assert len(list((desktop / "Talon tools").glob("*.lnk"))) == 5

        # Read real Windows link metadata and execute the linked status control,
        # without opening an app, installing hooks or starting dictation.
        result = powershell(
            "-Command",
            r"""
$shell = New-Object -ComObject WScript.Shell
$status = $shell.CreateShortcut((Join-Path $env:TOOLS_DESKTOP 'Talon tools\Talon - Dictation Status.lnk'))
$startup = $shell.CreateShortcut((Join-Path $env:TOOLS_STARTUP 'double-tap-control-dictation.lnk'))
[pscustomobject]@{
    Target = $status.TargetPath
    WorkingDirectory = $status.WorkingDirectory
    StartupTarget = $startup.TargetPath
    StartupArguments = $startup.Arguments
} | ConvertTo-Json
""",
        )
        assert result.returncode == 0, result.stderr
        link = json.loads(result.stdout)
        assert Path(link["WorkingDirectory"]) == clone
        assert Path(link["StartupTarget"]) == ahk
        assert (
            link["StartupArguments"]
            == '"' + str(clone / "plugin/dictation_router/double_tap_control.ahk") + '"'
        )
        status = subprocess.run(
            ["cmd.exe", "/c", link["Target"]],
            env=env,
            input="\n",
            capture_output=True,
            text=True,
            timeout=20,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        assert status.returncode == 0, status.stderr
        assert status.stdout.splitlines()[0] == "wispr"
        assert choice.read_bytes() == b"wispr\n"

        # A missing dependency must fail before creating installation targets.
        missing_desktop = tmp_path / "Unconfigured desktop"
        result = powershell(
            "-File",
            str(install),
            "-DesktopDirectory",
            str(missing_desktop),
            "-StartupDirectory",
            str(tmp_path / "Unconfigured startup"),
            "-AutoHotkeyPath",
            str(tmp_path / "missing.exe"),
        )
        assert result.returncode != 0
        assert not missing_desktop.exists()
