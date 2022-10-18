from talon import Context, Module, actions, app

#http://www.yougowords.com/start-with-e/1-syllables
#near
#kid could replace crunch
#eel elk eagle
#onyx adder oesten
#spun 
#urge is often misrecognized as args
#red is a color so better to use ram
#risk
#pink is a color so better to use perk
#each is often misrecognized as ice...
#bat is often misrecognized as whale/dot/it/space and many more commands... Trying out `batch` and `bill` instead
default_alphabet = "air batch cap drum east fine gust harp ice judge crunch look made net odd perk quench ram sun trap urn vest whale x yank zip onyx elk eagle".split(
    " "
)
letters_string = "abcdefghijklmnopqrstuvwxyzåäö"

default_digits = "zero one two three four five six seven eight nine".split(" ")
numbers = [str(i) for i in range(10)]
default_f_digits = (
    "one two three four five six seven eight nine ten eleven twelve".split(" ")
)

mod = Module()
mod.list("letter", desc="The spoken phonetic alphabet")
mod.list("symbol_key", desc="All symbols from the keyboard")
mod.list("arrow_key", desc="All arrow keys")
mod.list("number_key", desc="All number keys")
mod.list("modifier_key", desc="All modifier keys")
mod.list("function_key", desc="All function keys")
mod.list("special_key", desc="All special keys")
mod.list("punctuation", desc="words for inserting punctuation into text")


@mod.capture(rule="{self.modifier_key}+")
def modifiers(m) -> str:
    "One or more modifier keys"
    return "-".join(m.modifier_key_list)


@mod.capture(rule="{self.arrow_key}")
def arrow_key(m) -> str:
    "One directional arrow key"
    return m.arrow_key


@mod.capture(rule="<self.arrow_key>+")
def arrow_keys(m) -> str:
    "One or more arrow keys separated by a space"
    return str(m)


@mod.capture(rule="{self.number_key}")
def number_key(m) -> str:
    "One number key"
    return m.number_key


@mod.capture(rule="{self.letter}")
def letter(m) -> str:
    "One letter key"
    return m.letter


@mod.capture(rule="{self.special_key}")
def special_key(m) -> str:
    "One special key"
    return m.special_key


@mod.capture(rule="{self.symbol_key}")
def symbol_key(m) -> str:
    "One symbol key"
    return m.symbol_key


@mod.capture(rule="{self.function_key}")
def function_key(m) -> str:
    "One function key"
    return m.function_key


@mod.capture(rule="( <self.letter> | <self.number_key> | <self.symbol_key> )")
def any_alphanumeric_key(m) -> str:
    "any alphanumeric key"
    return str(m)


@mod.capture(
    rule="( <self.letter> | <self.number_key> | <self.symbol_key> "
    "| <self.arrow_key> | <self.function_key> | <self.special_key> )"
)
def unmodified_key(m) -> str:
    "A single key with no modifiers"
    return str(m)


@mod.capture(rule="{self.modifier_key}* <self.unmodified_key>")
def key(m) -> str:
    "A single key with optional modifiers"
    try:
        mods = m.modifier_key_list
    except AttributeError:
        mods = []
    return "-".join(mods + [m.unmodified_key])


@mod.capture(rule="<self.key>+")
def keys(m) -> str:
    "A sequence of one or more keys with optional modifiers"
    return " ".join(m.key_list)


@mod.capture(rule="{self.letter}+")
def letters(m) -> str:
    "Multiple letter keys"
    return "".join(m.letter_list)


ctx = Context()
modifier_keys = {
    # If you find 'alt' is often misrecognized, try using 'alter'.
    #"alt": "alt",  
    'alter': 'alt',
    "control": "ctrl",  #'troll':   'ctrl',
    "shift": "shift",  #'sky':     'shift',
    "super": "super",
    #"win": "super", #win is often misrepresented as wheel so I'm opting out of this one
}
if app.platform == "mac":
    modifier_keys["command"] = "cmd"
    modifier_keys["option"] = "alt"
ctx.lists["self.modifier_key"] = modifier_keys
alphabet = dict(zip(default_alphabet, letters_string))
ctx.lists["self.letter"] = alphabet

# `punctuation_words` is for words you want available BOTH in dictation and as key names in command mode.
# `symbol_key_words` is for key names that should be available in command mode, but NOT during dictation.
punctuation_words = {
    "back tick": "`",
    "grave": "`",
    "comma": ",",
    # Workaround for issue with conformer b-series; see #946
    "coma": ",",
    "period": ".",
    "full stop": ".",
    "semicolon": ";",
    "colon": ":",
    "forward slash": "/",
    "question mark": "?",
    "exclamation mark": "!",
    "exclamation": "!",
    #"exclamation point": "!",
    "asterisk": "*",
    "hash sign": "#",
    #"number sign": "#",
    "percent sign": "%",
    "at sign": "@",
    "and sign": "&",
    "ampersand": "&",
    "amper sign": "&",
    # Currencies
    "dollar sign": "$",
    "pound sign": "£",
}
symbol_key_words = {
    "void": " ",
    "dot": ".",
    #"semistack": ";",
    #"stack": ":",
    "drip": ",",
    
    "point": ".",
    "quote": "'",
    "apostrophe": "'",
    "L square": "[",
    "left square": "[",
    "square": "[",
    "R square": "]",
    "right square": "]",
    "slash": "/",
    "backslash": "\\",
    "minus": "-",
    "dash": "-",
    "equals": "=",
    "plus": "+",
    "tilde": "~",
    "question": "?",
    "bang": "!",
    "exclamation": "!",
    "down score": "_",
    "underscore": "_",
    "paren": "(",
    "L paren": "(",
    "left paren": "(",
    "R paren": ")",
    "right paren": ")",
    "curly": "{",
    "left curly": "{",
    #"brack": "{",
    #"bracket": "{",
    #"left bracket": "{",
    "r curly": "}",
    "right curly": "}",
    #"r brack": "}",
    #"r bracket": "}",
    #"right bracket": "}",
    "angle": "<",
    "left angle": "<",
    #"less than": "<",
    "rangle": ">",
    "R angle": ">",
    "right angle": ">",
    #"greater than": ">",
    #"star": "*",
    "hash": "#",
    "percent": "%",
    #"caret": "^",
    "caret sign": "^",
    #"amper": "&",
    "pipe": "|",
    "dubquote": '"',
    "double quote": '"',
    # Currencies
    #"dollar": "$",
    #"pound": "£",
}

# make punctuation words also included in {user.symbol_keys}
symbol_key_words.update(punctuation_words)
ctx.lists["self.punctuation"] = punctuation_words
ctx.lists["self.symbol_key"] = symbol_key_words
ctx.lists["self.number_key"] = dict(zip(default_digits, numbers))
ctx.lists["self.arrow_key"] = {
    "down": "down",
    "left": "left",
    "right": "right",
    "up": "up",
}

simple_keys = [
    "end",
    "enter",
    "escape",
    "home",
    "insert",
    "pagedown",
    "pageup",
    "space",
    #"tab",
]

alternate_keys = {
    "slap": "enter",
    "wipe": "backspace",
    "clear": "backspace",
    #"chuck": "backspace",
    #"delete": "backspace",
    #'junk': 'backspace',
    #"forward delete": "delete",
    "delete": "delete",
    "page up": "pageup",
    "page down": "pagedown",
    "tabber": "tab",
}
# mac apparently doesn't have the menu key.
if app.platform in ("windows", "linux"):
    alternate_keys["menu key"] = "menu"
    alternate_keys["print screen"] = "printscr"

special_keys = {k: k for k in simple_keys}
special_keys.update(alternate_keys)
ctx.lists["self.special_key"] = special_keys
ctx.lists["self.function_key"] = {
    f"F {default_f_digits[i]}": f"f{i + 1}" for i in range(12)
}


@mod.action_class
class Actions:
    def move_cursor(s: str):
        """Given a sequence of directions, eg. 'left left up', moves the cursor accordingly using edit.{left,right,up,down}."""
        for d in s.split():
            if d in ("left", "right", "up", "down"):
                getattr(actions.edit, d)()
            else:
                raise RuntimeError(f"invalid arrow key: {d}")