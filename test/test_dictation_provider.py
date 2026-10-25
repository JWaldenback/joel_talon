import talon

if hasattr(talon, "test_mode"):
    import json
    import subprocess
    import sys
    from pathlib import Path

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
