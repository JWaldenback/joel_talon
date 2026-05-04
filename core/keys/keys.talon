<user.letter>: key(letter)
(ship | uppercase) <user.letters> [(sink | sunk | lowercase | over)]:
    user.insert_formatted(letters, "ALL_CAPS")
<user.symbol_key>: key(symbol_key)
spike <user.symbol_key>: user.end_line_with_symbol_and_start_line(symbol_key)
<user.function_key>: key(function_key)
<user.special_key>: key(special_key)
<user.keypad_key>: key(keypad_key)
<user.modifiers> <user.unmodified_key>: key("{modifiers}-{unmodified_key}")
# for key combos consisting only of modifiers, eg. `press super`.
press <user.modifiers>: key(modifiers)
# for consistency with dictation mode and explicit arrow keys if you need them.
press <user.keys>: key(keys)
# press and hold a modifier
hold <user.modifiers>:
    key("{modifiers}:down")
    user.gui_hold_modifier_toggle(1, "{modifiers}")
(lift | unhold) <user.modifiers>:
    key("{modifiers}:up")
    user.gui_hold_modifier_toggle(0, "{modifiers}")
