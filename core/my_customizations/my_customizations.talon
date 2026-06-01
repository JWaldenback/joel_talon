#A general advice if I may, try to find a quite idiomatic way for short commands because you risk to have difficulty to remember them when you would have 50 of them. Personally i use a y suffix for most of my short commands: lessy, listy, movy, taily, awky and so forth

#Question. In knausj_talon what is the difference between edit.find() and user.find()?
#If you find them in actions.list() they should both have descriptions

#Otherwise, you should check out events.tail() in the repl to see what's happening behind the scenes for specific commands

#Question: Is there a way to execute a system command in a Talon script file or do I need to create a Python module?
#Answer: user.system_command_nb() 
#And obviously just put the command as a string in the function call

[insert] {user.vocabulary}: auto_insert(vocabulary)
website {user.website}: auto_insert(website)
system path <user.system_path>: auto_insert(system_path)

made phrase: "Mm, "
harp phrase: "Hmm, "
air phrase: "Aa, "
(I get it | I understand) phrase: "Aha, "
oak phrase: "Oh, "
no phrase: "Nä, "
okay phrase: "OK "
ha ha phrase: "Haha "
ha ha ha phrase: "Hahaha "
good day phrase: "G'day "

(signature phrase | insert signature): 
    "Best regards"
    edit.line_insert_down()
    "Joel"

(signature phrase swedish | insert signature swedish): 
    "Med vänlig hälsning"
    edit.line_insert_down()
    "Joel"

(mic | Mike | microphone) toggle: user.toggle_talon_microphone()
key(scroll_lock): user.toggle_talon_microphone()

(end ten | ten enter): key(enter)

profile switcher open: user.open_browser_profile_switcher("Google Chrome")

talon hood (relaunch | restart):
    # Ensure the HUD and its widgets are visible and the mic + mode icons
    # are on the status bar. Idempotent — no remove-first step, so it
    # works when an icon is already missing (the previous remove-then-add
    # version silently failed in that case).
    user.hud_enable()
    user.hud_enable_id("event_log")
    user.hud_enable_id("status_bar")
    user.hud_add_single_click_mic_toggle()
    user.hud_activate_poller("mode_toggle")

program close: user.close_program()

^talon (relaunch | restart)$: user.talon_relaunch()
^talon close$: user.talon_close()

#System wide toggle huddle function. Works only if one uses the Slack desktop app, not the Slack web app
#slack (huddle | call) (new | join): 
#    user.slack_toggle_huddle()
#    sleep(300ms)
#    key(scroll_lock)

#System wide toggle huddle function. Works only if one uses the Slack desktop app, not the Slack web app
#slack (huddle | call) close: user.slack_toggle_huddle()

#This works when `control mouse (zoom)` is active
#key(f13): tracking.zoom()

do not disturb toggle:
    key(super-n)
    sleep(1000ms)
    key(enter)