import talon

if hasattr(talon, "test_mode"):
    import plistlib
    import pytest
    from plugin.mic_capture_watcher.dictation_session import InputPause, DictationSession
    from plugin.mic_capture_watcher.mac_dictation_shortcut import dictation_shortcut

    def fixture_pause(microphone="Mic"):
        state = {"mic": microphone, "mouse": set()}
        pause = InputPause(lambda: state["mic"], lambda value: state.update(mic=value),
                           state["mouse"].add, state["mouse"].discard)
        return state, pause

    def test_overlapping_manual_pause_survives_dictation_stop():
        state, pause = fixture_pause()
        session = DictationSession(pause)
        session.start(0)
        session.observe(True, 1)
        pause.acquire("manual")
        session.observe(False, 2)
        session.observe(False, 3)
        assert state == {"mic": "None", "mouse": {"manual"}}
        pause.release("manual")
        assert state == {"mic": "Mic", "mouse": set()}

    def test_start_timeout_and_stop_debounce():
        state, pause = fixture_pause()
        session = DictationSession(pause)
        session.start(0)
        assert session.observe(False, 4.9) is None
        assert session.observe(False, 5) == "start_failed"
        assert state["mic"] == "Mic"
        session.observe(True, 6)
        session.observe(False, 7)
        session.observe(True, 7.2)
        session.observe(False, 8)
        assert session.observe(False, 8.5) is None
        assert session.observe(False, 9) == "finished"

    def test_partial_mouse_failure_rolls_back_both_inputs():
        state, pause = fixture_pause()
        def fail(owner):
            state["mouse"].add(owner)
            raise RuntimeError("failed after acquiring mouse")
        pause.sleep_mouse = fail
        with pytest.raises(RuntimeError):
            pause.acquire("dictation")
        assert state == {"mic": "Mic", "mouse": set()}
        assert not pause.owners
        assert pause.saved_microphone is None

    @pytest.mark.parametrize("initial,selected,expected", [
        ("None", "None", "None"), ("Mic", "Other mic", "Other mic"),
    ])
    def test_restore_respects_existing_mute_and_new_microphone(initial, selected, expected):
        state, pause = fixture_pause(initial)
        pause.acquire("dictation")
        state["mic"] = selected
        pause.release("dictation")
        assert state["mic"] == expected

    @pytest.mark.parametrize("value,expected", [
        ({"type": "modifier", "parameters": [262144, 2**63-1]}, ["ctrl", "ctrl"]),
        ({"type": "standard", "parameters": [100, 2, 1 << 23]}, ["fn-d"]),
        ({"type": "standard", "parameters": [32, 49, 1 << 20]}, ["cmd-space"]),
    ])
    def test_configured_shortcuts(tmp_path, value, expected):
        path = tmp_path / "keys.plist"
        path.write_bytes(plistlib.dumps({"AppleSymbolicHotKeys": {"164": {
            "enabled": True, "value": value}}}))
        assert dictation_shortcut(path=path) == expected

    def test_shortcut_override_needs_no_plist(tmp_path):
        assert dictation_shortcut("ctrl ctrl", tmp_path / "missing") == ["ctrl", "ctrl"]

    def test_disabled_shortcut_fails_before_handoff(tmp_path):
        path = tmp_path / "keys.plist"
        path.write_bytes(plistlib.dumps({"AppleSymbolicHotKeys": {"164": {"enabled": False}}}))
        with pytest.raises(ValueError):
            dictation_shortcut(path=path)
