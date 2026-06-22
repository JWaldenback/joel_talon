# -1 because we are repeating, so the initial command counts as one
#<user.ordinals>: core.repeat_command(ordinals-1)
<number_small> times$: core.repeat_command(number_small - 1)
<number_small> slow times$: user.repeat_command_wrapper(number_small - 1)
#twice$: core.repeat_command(2-1)
#thrice$: core.repeat_command(3-1)
#repeat command <number_small> [times]: core.repeat_command(number_small)
#repeat command <number_small> slow times: user.repeat_command_wrapper(number_small)
repeat <number_small> times: core.repeat_phrase(number_small)
repeat <number_small> slow times: user.repeat_phrase_wrapper(number_small)

# -0 because we are repeating after the initial command has already been run, so now we want to repeat it as many times as one says
#^<number_small> times: core.repeat_phrase(number_small-0)
#^(repeat it | again): core.repeat_phrase(1-0)
^twice: core.repeat_phrase(2-0)
^thrice: core.repeat_phrase(3-0)

(repeat phrase | again) [<number_small> times]:
    core.repeat_partial_phrase(number_small or 1)
