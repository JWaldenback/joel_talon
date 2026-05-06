hostname: Gamen
-
#the carrot "^" indicates there is nothing before and the dollar "$" that nothing comes after it, so if you say "copy copy" it won't trigger the voice command "^copy$: edit.copy()"

#Windows key + Ctrl + (number). Switch to the last active window of the app pinned to the taskbar in the position indicated by the number.
#^focus <number_small>: key("super-ctrl-{number_small}")
^focus [file] explorer: key(super-ctrl-1)
^focus chrome: key(super-ctrl-2)
^focus edge: key(super-ctrl-3)
^focus gemini: key(super-ctrl-7)
#^focus notes: user.open_specific_tab("Google Chrome", "iCloud")
#^focus notes: user.switcher_focus("Opera Internet Browser")
#^focus notes: key(super-ctrl-5)
#^focus chat gpt: user.open_specific_tab("Microsoft Edge", "chatGPT")
^focus chat gpt: key(super-ctrl-8)
#^focus copilot: key(super-ctrl-7)
#^focus (slack | lack | like): user.open_specific_tab("Microsoft Edge", "Slack")
^focus (slack | lack | like): key(super-ctrl-4)
#^focus whatsapp: key(super-ctrl-9)
#^focus messenger: key(super-ctrl-8)
#^focus figma: key(super-ctrl-5)

^focus outlook: user.open_specific_tab("Google Chrome", "outlook.live.com")
^focus google calendar: user.open_specific_tab("Google Chrome", "calendar.google.com")
^focus google calendar work: user.open_specific_tab("Microsoft Edge", "calendar.google.com")
^focus claude design: user.open_specific_tab("Microsoft Edge", "claude.ai/design")

#Can improve this voice command by first checking if the snipping tool is in focus, and if it is just run key(ctrl-n) 
^grab screen selection$:
    user.toggle_talon_microphone()
    mimic("event log clear logs")
    key(super-ctrl-1)
    sleep(300ms)
    key(ctrl-n)

gaze mode:
    user.enable_gaze_control()

no eye tracker mode:
    user.enable_no_eye_tracker_mode()

hiss mode:
    user.enable_hiss_control()

^use both eyes$:
    user.set_eye_tracking_mask("both")

^use only left eye$:
    user.set_eye_tracking_mask("left")

^use only right eye$:
    user.set_eye_tracking_mask("right")