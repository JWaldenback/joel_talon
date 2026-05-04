mode: command
mode: dictation
-

^dictation mode$: user.dictation_mode()
^(command mode | come on mode)$: user.command_mode()

#^dictation mode$:
#    mode.disable("sleep")
#    mode.disable("command")
#    mode.enable("dictation")
#    user.code_clear_language_mode()
#    user.gdb_disable()
#^(command mode | come on mode)$:
#    mode.disable("sleep")
#    mode.disable("dictation")
#    mode.enable("command")