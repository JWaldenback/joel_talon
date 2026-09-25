# Mac support for custom commands

The active custom command set uses Mac shortcuts and existing Talon Mac actions
where equivalents are available. Windows implementations remain available.

## Available on Mac

- Apple Dictation handoff: `start listening`, existing dictation key switches,
  microphone/tracking pause and automatic restoration. Control-Option-Escape
  releases a stuck Dictation pause. See `plugin/mic_capture_watcher/README.md`.
- Global gaze/hiss/no-eye-tracker modes and eye selection.
- Tab duplication, Chrome profile menu, Finder icon/list views, screenshots,
  fullscreen, lock, sleep, restart and shutdown.
- Custom Codex, Claude, Google Docs/Drive/Gmail, Word and Outlook commands.
- Meet, Teams, Zoom and Slack call controls, including mapped keypad controls.
- Figma pan with held-input cleanup on stopping or switching apps.

## Commands requiring a configured shortcut

Codex chat search has no default key in its current documentation. Assign one
in Codex and set `user.codex_search_chats_key` to the same Talon key expression.

Gemini new chat, submit, cancel and newline are available. Its other custom
controls have no verified Mac shortcuts. Configure a working binding using
`user.gemini_focus_input_key`, `user.gemini_sidebar_key`,
`user.gemini_search_key`, `user.gemini_settings_key`,
`user.gemini_copy_response_key`, `user.gemini_next_chat_key`, or
`user.gemini_previous_chat_key`. Unset bindings display a notice.

## Intentionally Windows-only

Windows taskbar positions, Action Center/Do Not Disturb choreography, machine-
specific desktop sequences, Windows microphone dialogs, dictation language
routing through AutoHotkey, and custom Opera/Vivaldi UI sequences remain scoped
to Windows. Existing native Mac browser implementations still apply.
Windows Explorer icon-size commands and legacy Slack call video/invite sequences
have no equivalent enabled on Mac.

Obsolete quoted dictation implementations were removed. The active Windows
behavior was retained in `core/my_customizations/native_dictation.py`.

App-specific commands still depend on each application's current shortcuts,
focus and permissions. Automated checks do not replace testing inside an actual
call or on a Windows computer.
