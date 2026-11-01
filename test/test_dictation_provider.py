import talon

if hasattr(talon, "test_mode"):
    import json
    import os
    import subprocess
    import sys
    from pathlib import Path

    import pytest

    SCRIPT = Path(__file__).parents[1] / "docs/macos/dictation-provider"

    def run_selector(config, provider):
        return subprocess.run(
            [sys.executable, str(SCRIPT), provider, "--config", str(config)],
            text=True,
            capture_output=True,
        )

    def test_switching_provider_preserves_other_shortcuts_and_survives_next_invocation(
        tmp_path,
    ):
        config = tmp_path / "karabiner.json"
        unrelated = {"description": "Keep my screenshot shortcut", "manipulators": []}
        other_profile = {
            "name": "Other keyboard",
            "selected": False,
            "devices": [{"ignore": True}],
        }
        original = json.dumps(
            {
                "profiles": [
                    {
                        "name": "Default",
                        "selected": True,
                        "complex_modifications": {
                            "rules": [
                                unrelated,
                                {
                                    "description": "RS foot pedal: Windows-H sends Apple Dictation key",
                                    "manipulators": [],
                                },
                            ]
                        },
                    },
                    other_profile,
                ]
            }
        )
        config.write_text(original)
        for provider, expected in [
            ("wispr", {"key_code": "spacebar", "modifiers": ["fn"], "repeat": False}),
            ("macos", {"consumer_key_code": "dictation", "repeat": False}),
        ]:
            result = run_selector(config, provider)
            assert result.returncode == 0, result.stderr
            assert run_selector(config, "status").stdout.strip() == provider
            data = json.loads(config.read_text())
            assert data["profiles"][1] == other_profile
            rules = data["profiles"][0]["complex_modifications"]["rules"]
            assert rules[0] == unrelated
            assert len(rules) == 2
            manipulators = rules[1]["manipulators"]
            pedal = next(m for m in manipulators if m["from"]["key_code"] == "h")
            assert pedal["from"]["modifiers"]["mandatory"] == ["command"]
            assert pedal["to"][0] == expected
            keyboard = [
                m for m in manipulators if m["from"]["key_code"] == "left_option"
            ]
            assert len(keyboard) == 2
            assert keyboard[0]["to_if_alone"][0] == expected
            assert {m["from"]["key_code"] for m in manipulators} == {"h", "left_option"}
        assert (
            config.with_name("karabiner.json.before-dictation-provider").read_text()
            == original
        )

    def test_invalid_configuration_is_left_untouched(tmp_path):
        config = tmp_path / "karabiner.json"
        config.write_text("{not-json")
        result = run_selector(config, "wispr")
        assert result.returncode != 0
        assert config.read_text() == "{not-json"
        assert not config.with_name("karabiner.json.before-dictation-provider").exists()

    @pytest.mark.skipif(sys.platform != "win32", reason="Windows PowerShell selector")
    def test_windows_selection_persists_and_rejects_invalid_state(tmp_path):
        # Run the real standalone entry point with isolated machine-local
        # storage. This catches PowerShell/AutoHotkey file-format mismatches
        # without changing this machine's selected provider.
        script = Path(__file__).parents[1] / "docs/windows/dictation-provider.ps1"

        def select(provider):
            return subprocess.run(
                [
                    "powershell.exe",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(script),
                    provider,
                ],
                env={
                    **os.environ,
                    "APPDATA": str(tmp_path / "redirected-appdata"),
                    "USERPROFILE": str(tmp_path / "profile"),
                },
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )

        assert select("status").stdout.strip() == "windows"
        for provider in ("wispr", "windows", "wispr"):
            result = select(provider)
            assert result.returncode == 0, result.stderr
            assert select("status").stdout.strip() == provider
            assert (
                tmp_path / "profile/.talon-dictation/provider.txt"
            ).read_bytes() == (provider + "\n").encode("ascii")

        config = tmp_path / "profile/.talon-dictation/provider.txt"
        result = select("unknown")
        assert result.returncode != 0
        assert config.read_text().strip() == "wispr"
        config.write_text("invalid")
        assert select("status").returncode != 0
        assert config.read_text() == "invalid"

    @pytest.mark.skipif(sys.platform != "win32", reason="Native AutoHotkey reader")
    def test_windows_shortcuts_read_shared_profile_state(tmp_path):
        ahk = Path(os.environ["PROGRAMFILES"]) / "AutoHotkey/AutoHotkey.exe"
        if not ahk.is_file():
            pytest.skip("AutoHotkey 1.1 is required for the native reader check")

        # Exercise the same reader the login hook calls, without installing a
        # keyboard hook or sending keys. AppData deliberately differs from the
        # profile, as it does between packaged apps and Windows login startup.
        profile = tmp_path / "User profile with spaces"
        config = profile / ".talon-dictation/provider.txt"
        config.parent.mkdir(parents=True)
        appdata = tmp_path / "Private AppData"
        old_config = appdata / "TalonDictation/provider.txt"
        old_config.parent.mkdir(parents=True)
        old_config.write_text("windows\n")
        library = (
            Path(__file__).parents[1] / "plugin/dictation_router/dictation_provider.ahk"
        )
        script = tmp_path / "read_provider.ahk"
        script.write_text(
            f"""#NoEnv
#NoTrayIcon
#Include {library}
try {{
    provider := ReadDictationProvider()
    FileAppend, %provider%, *
    ExitApp, 0
}} catch error {{
    FileAppend, % error.Message, **
    ExitApp, 1
}}
"""
        )
        for saved, expected in (
            ("wispr\n", "wispr"),
            ("windows\n", "windows"),
            ("invalid", None),
            (None, "windows"),
        ):
            if saved is None:
                config.unlink()
            else:
                config.write_text(saved)
            result = subprocess.run(
                [str(ahk), "/ErrorStdOut", str(script)],
                env={
                    **os.environ,
                    "USERPROFILE": str(profile),
                    "APPDATA": str(appdata),
                },
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
                timeout=10,
            )
            assert result.returncode == (0 if expected is not None else 1), (
                saved,
                result.stderr,
            )
            assert result.stdout == (expected or "")
