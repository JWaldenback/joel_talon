import talon

if hasattr(talon, "test_mode"):
    import importlib.util
    import sys
    from pathlib import Path
    from types import ModuleType, SimpleNamespace

    import pytest

    @pytest.mark.parametrize(
        "service, process",
        [
            ("win_h_dictation", "TextInputHost.exe"),
            ("wispr_flow", "Wispr Flow.exe"),
            ("wispr_flow", "Wispr Flow Helper.exe"),
        ],
    )
    @pytest.mark.parametrize(
        "pause_kind, other_capture",
        [
            ("watcher", False),
            ("manual", False),
            ("voice_command", False),
            ("watcher", True),
        ],
    )
    def test_divide_closes_windows_dictation_and_restores_talon(
        monkeypatch, pause_kind, other_capture, service, process
    ):
        state = {
            "mic": "Yeti",
            "speech": True,
            "owners": set(),
            "keys": [],
            "recording": False,
            "other_recording": other_capture,
        }

        class Module:
            def setting(self, *args, **kwargs):
                pass

            def action_class(self, cls):
                return cls

        class Context:
            def action_class(self, *args):
                return lambda cls: cls

        fake_talon = ModuleType("talon")
        fake_talon.Module = Module
        fake_talon.Context = Context
        fake_talon.imgui = SimpleNamespace(
            open=lambda **kwargs: lambda f: f, GUI=object
        )
        fake_talon.ui = SimpleNamespace()
        fake_talon.app = SimpleNamespace(
            platform="windows", register=lambda *a: None, notify=lambda *a: None
        )
        fake_talon.cron = SimpleNamespace(cancel=lambda *a: None)
        fake_talon.settings = SimpleNamespace(
            get=lambda *a: 300, register=lambda *a: None
        )
        fake_talon.scope = SimpleNamespace(get=lambda *a: set())
        fake_talon.actions = SimpleNamespace(
            key=state["keys"].append,
            sound=SimpleNamespace(active_microphone=lambda: state["mic"]),
            speech=SimpleNamespace(
                set_microphone=lambda name: state.update(mic=name),
                enabled=lambda: state["speech"],
                enable=lambda: state.update(speech=True),
            ),
            tracking=SimpleNamespace(
                control_enabled=lambda: True,
                control_zoom_enabled=lambda: True,
                control1_enabled=lambda: True,
            ),
            user=SimpleNamespace(
                mouse_sleep=state["owners"].add,
                mouse_wake=state["owners"].discard,
                mouse_sleep_held=lambda owner: owner in state["owners"],
                voice_dictation_disarm_keypress_resume=lambda: None,
                mic_and_eye_tracker_state_log=lambda *a: None,
            ),
        )
        monkeypatch.setitem(sys.modules, "talon", fake_talon)
        prefix = "plugin.mic_capture_watcher"
        monkeypatch.setitem(
            sys.modules,
            prefix + ".mic_and_eye_tracker_state_log",
            SimpleNamespace(log=lambda *a, **kw: None),
        )
        root = Path(__file__).parents[1]

        def load(name, path):
            spec = importlib.util.spec_from_file_location(name, root / path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module

        watcher = load(
            prefix + ".windows_pedal_test",
            "plugin/mic_capture_watcher/mic_capture_watcher.py",
        )
        toggle = load(
            "windows_pedal_toggle_test", "core/my_customizations/my_customizations.py"
        )

        def capture_sessions():
            sessions = []
            if state["recording"]:
                sessions.append((123, process, 1))
            if state["other_recording"]:
                sessions.append((456, "superwhisper.exe", 1))
            # A running Flow app with an inactive capture session must not
            # keep Talon paused after recording ends.
            sessions.append((789, "Wispr Flow.exe", 0))
            return sessions

        monkeypatch.setattr(
            watcher,
            "_import_monitor",
            lambda: (
                SimpleNamespace(list_active_capture_sessions=capture_sessions),
                None,
            ),
        )
        fake_talon.actions.user.windows_dictation_pedal_recover = (
            watcher.Actions.windows_dictation_pedal_recover
        )
        fake_talon.actions.user.mic_capture_watcher_holds_tracker_pause = (
            watcher.Actions.mic_capture_watcher_holds_tracker_pause
        )
        fake_talon.actions.user.toggle_talon_sleep_holds_tracker_pause = (
            toggle.UserActions.toggle_talon_sleep_holds_tracker_pause
        )

        if pause_kind == "manual":
            toggle.UserActions.toggle_talon_sleep()
            assert state["owners"] == {"toggle"}
        elif pause_kind == "voice_command":
            state["owners"].add("dictation")
        state["recording"] = True
        watcher._tick()
        assert state["mic"] == "None"
        assert watcher.is_service_active(service)

        if not other_capture:
            # Exercise a normal recording finish before pedal recovery.
            # A manual pause must survive; an automatic pause must release.
            state["recording"] = False
            watcher._tick()
            assert not watcher.is_service_active(service)
            if pause_kind == "manual":
                assert state["mic"] == "None"
                assert state["owners"] == {"toggle"}
            else:
                assert state["mic"] == "Yeti"
                assert "watcher" not in state["owners"]
            state["recording"] = True
            watcher._tick()
            assert state["mic"] == "None"

        # A voice-command handoff can also disable Talon's speech engine.
        if not other_capture:
            state["speech"] = False
        toggle.UserActions.toggle_talon_sleep()
        assert state["keys"] == ["escape"]
        assert not watcher.is_service_active(service)
        if other_capture:
            assert state["mic"] == "None"
            assert state["owners"] == {"watcher"}
            state["recording"] = False
            watcher._tick()
            assert state["mic"] == "None"
            state["other_recording"] = False
            watcher._tick()
            assert state["mic"] == "Yeti"
            assert state["owners"] == set()
            return
        assert state["mic"] == "Yeti"
        assert state["speech"] is True
        assert state["owners"] == set()
        assert not toggle._toggle_owns_sleep

        # A lingering capture session must not re-pause Talon. A new session
        # after it ends should still be detected normally.
        watcher._tick()
        assert state["mic"] == "Yeti"
        state["recording"] = False
        watcher._tick()
        state["recording"] = True
        watcher._tick()
        assert state["mic"] == "None"
        assert watcher.is_service_active(service)
