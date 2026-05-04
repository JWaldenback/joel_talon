not tag: user.screenshot_disabled
-

^grab screen$: 
    user.engine_mimic("event log clear logs")
    user.screenshot()
#^grab screen <number_small>$: user.screenshot(number_small)
#^grab window$: user.screenshot_window()
#Commented out the command below in favor for the setup in gamen_computer.talon
#^grab selection$: 
    #user.engine_mimic("event log clear logs")
    #user.screenshot_selection()
#The command below can be used instead of `grab screen selection`
^grab selection clip$:
    user.engine_mimic("event log clear logs")
    user.screenshot_selection_clip()
#^grab settings$: user.screenshot_settings()
^grab screen clip$: 
    user.engine_mimic("event log clear logs")
    user.screenshot_clipboard()
^grab screen <number_small> clip$: 
    user.engine_mimic("event log clear logs")
    user.screenshot_clipboard(number_small)
^grab window clip$: 
    user.engine_mimic("event log clear logs")
    user.screenshot_window_clipboard()
