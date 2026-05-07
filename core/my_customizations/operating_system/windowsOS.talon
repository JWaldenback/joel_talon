os: windows
-
windows search: key(super-s)

#(start | stop) dictation: user.start_stop_dictation()

start listening:
    #set keyboard to English
    key(alt-shift-1)
    user.toggle_dictation_voice_command()

#börja lyssna/starta diktering
(burial listener | burial alister):
#| start attic theory | start the theory | start ate theory | start a dig theory | start a the theory):
    #set keyboard to Swedish
    key(alt-shift-2)
    user.toggle_dictation_voice_command()

(lang | language) change: key(alt-shift)
#https://www.digitalcitizen.life/keyboard-language-shortcut/
[lang | language] english: key(alt-shift-1)
[lang | language] swedish: key(alt-shift-2)
#nine dash: key(alt-shift-2)

#The program SoundSwitch enables hotkeys for changing input and output devices: https://github.com/Belphemur/SoundSwitch
input [device] change: key(alt-ctrl-f7)
output [device] change: key(alt-ctrl-f11)

virtual keyboard: key(super-ctrl-o)
#Check if there are better options of virtual keyboards than the Microsoft built in
#https://www.makeuseof.com/windows-best-virtual-keyboards/
#Maybe it's possible to launch the eye control keyboard with a keyboard shortcut
#https://support.microsoft.com/en-us/windows/eye-control-basics-in-windows-97d68837-b993-8462-1f9d-3c957117b1cf
#https://blakewatson.com/journal/writing-and-coding-with-the-macos-accessibility-keyboard/

clipboard [open | history | windows]: key(super-v)

show desktop: key(super-d)