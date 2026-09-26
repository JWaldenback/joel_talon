import talon

if hasattr(talon, 'test_mode'):
    import importlib.util
    import sys
    from pathlib import Path
    from types import SimpleNamespace, ModuleType

    import pytest

    @pytest.mark.parametrize('recorder', ['com.apple.CoreSpeech', 'com.apple.inputmethod.ironwood'])
    def test_apple_recording_pauses_microphone_and_gaze_then_restores(monkeypatch, recorder):
        values = {'user.mic_capture_watch_enabled': True}
        state = {'mic': 'Yeti', 'gaze': True, 'owners': set()}
        now = [0.0]

        class Module:
            def setting(self, name, **kwargs):
                values['user.' + name] = kwargs['default']

            def action_class(self, cls):
                return cls

        def sleep_mouse(owner):
            state['owners'].add(owner)
            state['gaze'] = False

        def wake_mouse(owner):
            state['owners'].discard(owner)
            state['gaze'] = not state['owners']

        fake_talon = ModuleType('talon')
        fake_talon.Module = Module
        fake_talon.actions = SimpleNamespace(
            sound=SimpleNamespace(active_microphone=lambda: state['mic'],
                                  set_microphone=lambda name: state.update(mic=name)),
            user=SimpleNamespace(mouse_sleep=sleep_mouse, mouse_wake=wake_mouse))
        fake_talon.app = SimpleNamespace(platform='mac', register=lambda *a: None,
                                        notify=lambda *a: None)
        fake_talon.cron = SimpleNamespace(cancel=lambda *a: None)
        fake_talon.settings = SimpleNamespace(get=values.__getitem__)
        monkeypatch.setitem(sys.modules, 'talon', fake_talon)
        prefix = 'plugin.mic_capture_watcher'
        monkeypatch.setitem(sys.modules, prefix + '.mic_and_eye_tracker_state_log',
                            SimpleNamespace(log=lambda *a, **kw: None))
        spec = importlib.util.spec_from_file_location(
            prefix + '.watcher_test',
            Path(__file__).parents[1] / 'plugin/mic_capture_watcher/mac_dictation.py')
        watcher = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(watcher)
        monkeypatch.setattr(watcher, 'time', SimpleNamespace(monotonic=lambda: now[0]))
        audio = watcher.MacAudio.__new__(watcher.MacAudio)
        processes = {1: ('com.talonvoice.Talon', True), 2: (recorder, True)}
        audio._processes = lambda: list(processes)
        audio._bundle_id = lambda obj: processes[obj][0]
        audio._get = lambda obj, selector, typ: (typ(processes[obj][1]), 4)
        watcher._audio = audio

        watcher._tick()
        assert state['mic'] == 'None'
        assert state['gaze'] is False
        assert watcher._session.active
        processes[2] = (recorder, False)
        now[0] = 1.0
        watcher._tick()
        now[0] = 2.0
        watcher._tick()
        assert state == {'mic': 'Yeti', 'gaze': True, 'owners': set()}
        assert not watcher._session.active
