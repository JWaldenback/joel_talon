import talon

if hasattr(talon, "test_mode"):
    import importlib.util
    import sys
    from pathlib import Path
    from types import ModuleType, SimpleNamespace

    import pytest

    VK_H = 0x48
    VK_A = 0x41

    @pytest.fixture
    def timing(monkeypatch):
        logged = []

        class Module:
            def setting(self, *args, **kwargs):
                pass

        fake_talon = ModuleType("talon")
        fake_talon.Module = Module
        fake_talon.app = SimpleNamespace(register=lambda *a: None)
        fake_talon.settings = SimpleNamespace(get=lambda *a: True, register=lambda *a: None)
        monkeypatch.setitem(sys.modules, "talon", fake_talon)
        prefix = "plugin.mic_capture_watcher"
        monkeypatch.setitem(
            sys.modules,
            prefix + ".mic_and_eye_tracker_state_log",
            SimpleNamespace(log=lambda event, **fields: logged.append((event, fields))),
        )
        path = Path(__file__).parents[1] / "plugin/mic_capture_watcher/dictation_timing.py"
        spec = importlib.util.spec_from_file_location(prefix + ".dictation_timing_test", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        clock = {"t": 0.0}
        monkeypatch.setattr(module.time, "monotonic", lambda: clock["t"])
        module.logged = logged
        module.clock = clock
        return module

    def drain(timing):
        presses = []
        while not timing._queue.empty():
            presses.append(timing._queue.get())
        return presses

    def test_only_fresh_win_h_presses_are_recorded(timing):
        # A held pedal auto-repeats H; only the first key-down is a press.
        timing.on_hook_key(VK_H, True, True, False, 15)
        timing.on_hook_key(VK_H, True, True, False, 0)
        timing.on_hook_key(VK_H, False, True, False, 0)
        # H without Win, and other keys with Win, are not dictation presses.
        timing.on_hook_key(VK_H, True, False, False, 0)
        timing.on_hook_key(VK_H, False, False, False, 0)
        timing.on_hook_key(VK_A, True, True, False, 0)
        timing.on_hook_key(VK_H, True, True, True, 900)

        assert [(delay, injected) for _t, delay, injected in drain(timing)] == [
            (15, False),
            (900, True),
        ]

    def test_presses_pair_with_dictation_and_report_misses_and_stalls(timing):
        clock = timing.clock

        # Normal start: press, then the watcher sees voice typing open.
        timing._handle_press(0.0, 15, False)
        clock["t"] = 0.8
        assert timing.on_dictation_transition() == 800
        assert timing.on_dictation_transition() is None

        # Pressing again before anything happened marks the first as missed.
        timing._handle_press(10.0, 0, False)
        timing._handle_press(11.5, 0, False)
        # A press with no open/close at all expires on a later tick.
        clock["t"] = 11.5 + timing.UNANSWERED_AFTER_S
        timing.on_watcher_tick(300)

        # A tick far later than the 300 ms poll is a Talon stall.
        clock["t"] += 0.3
        timing.on_watcher_tick(300)
        clock["t"] += 2.2
        timing.on_watcher_tick(300)

        events = [
            (event, fields.get("reason"), fields.get("waited_ms", fields.get("gap_ms")))
            for event, fields in timing.logged
        ]
        assert events == [
            ("win_h_pressed", None, None),
            ("win_h_pressed", None, None),
            ("win_h_unanswered", "pressed_again", 1500),
            ("win_h_pressed", None, None),
            ("win_h_unanswered", "no_open_or_close", 3000),
            ("watcher_tick_gap", None, 2200),
        ]
