^system shutdown$:
    user.system_shutdown()
^system (relaunch | restart)$:
    user.system_restart()
^system hibernate$:
    user.system_hibernate()
^system lock$:
    user.system_lock()

#open {user.launch_command}:
#    user.exec(launch_command)