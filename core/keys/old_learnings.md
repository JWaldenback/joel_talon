# Old learnings — symbols.py legacy dicts

These two dicts (`punctuation_words` and `symbol_key_words`) used to be the source of truth in [symbols.py](symbols.py) before the refactor to the `Symbol` class + `symbols` list. They were never imported by anything after the refactor, so any entries added here had no effect at runtime — but they're kept as a reference because some of the personal additions might still be wanted in the active config someday.

To re-activate any of these spoken forms, add them to the `Symbol(...)` entries in the `symbols` list in [symbols.py](symbols.py). The 2nd constructor arg = available in dictation + command mode; the 3rd arg = command mode only.

## punctuation_words (legacy)

Available BOTH in dictation and as key names in command mode.

```python
punctuation_words = {
    # TODO: I'm not sure why we need these, I think it has something to do with
    # Dragon. Possibly it has been fixed by later improvements to talon? -rntz
    "`": "`",
    ",": ",",  # <== these things
    "back tick": "`",
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
    "number sign": "#",
    "percent sign": "%",
    "at sign": "@",
    "and sign": "&",
    "ampersand": "&",
    "amper sign": "&",
    # Currencies
    "dollar sign": "$",
    "pound sign": "£",
    "hyphen": "-",
    "L paren": "(",
    "left paren": "(",
    "R paren": ")",
    "right paren": ")",

    #My additions
    "dash sign": "-",
    "euro sign": "€",
}
```

## symbol_key_words (legacy)

Key names that should be available in command mode, but NOT during dictation.

```python
symbol_key_words = {
    "dot": ".",
    "point": ".",
    "quote": "'",
    "quest": "?",
    "question": "?",
    "apostrophe": "'",
    "L square": "[",
    "left square": "[",
    "brack": "[",
    "bracket": "[",
    "left bracket": "[",
    "square": "[",
    "R square": "]",
    "right square": "]",
    "r brack": "]",
    "r bracket": "]",
    "right bracket": "]",
    "slash": "/",
    "backslash": "\\",
    "minus": "-",
    #"dash": "-",
    "equals": "=",
    "plus": "+",
    "grave": "`",
    "tilde": "~",
    "bang": "!",
    "exclamation": "!",
    "down score": "_",
    "underscore": "_",
    "paren": "(",
    "brace": "{",
    "left brace": "{",
    "curly": "{",
    "left curly": "{",
    #"curly bracket": "{",
    #"left curly bracket": "{",
    "r brace": "}",
    "right brace": "}",
    "r curly": "}",
    "right curly": "}",
    #"r curly bracket": "}",
    #"right curly bracket": "}",
    "angle": "<",
    "left angle": "<",
    #"less than": "<",
    "rangle": ">",
    "R angle": ">",
    "right angle": ">",
    #"greater than": ">",
    #"star": "*",
    #"hash": "#", #removed this one as it was often misinterpreted as `dash`
    "percent": "%",
    #"caret": "^",
    "caret sign": "^",
    #"amper": "&",
    "pipe": "|",
    "dub quote": '"',
    "double quote": '"',
    # Currencies
    #"dollar": "$",
    #"pound": "£",

    #My additions
    #"semistack": ";",
    #"stack": ":",
    #"drip": ",",
    "vest ten": "?",
    #"vest one": "?",
    "vest ram": "?",
    "and dash": "–",
    "em dash": "—",
}
```

## Personal additions worth re-adding to the active `symbols` list

These were *not yet* present in the active list when archived:

- `"dash sign"` → `-`  (would go in `Symbol("-", ...)`, dictation-safe slot)
- `"vest ten"` → `?`   (would go in `Symbol("?", ...)`, command-only slot)
- `"vest ram"` → `?`   (would go in `Symbol("?", ...)`, command-only slot)
- `"and dash"` → `–`   (would go in `Symbol("–", ...)`, command-only slot)

Already covered in active list (no migration needed):
- `"euro sign"` — already on `Symbol("€", ...)`
- `"em dash"` — already on `Symbol("—", ...)`

---

# Old learnings — keys.py legacy structures (pre-upstream-merge)

The chunk below was found in a stashed/conflicted version of `keys.py`. The current upstream-merged `keys.py` no longer contains any of this — special keys were moved out of Python into `.talon-list` files (see [win/special_key.talon-list](win/special_key.talon-list) and [mac/special_key.talon-list](mac/special_key.talon-list)).

## Legacy wiring of `punctuation_words` / `symbol_key_words`

```python
# make punctuation words also included in {user.symbol_keys}
symbol_key_words.update(punctuation_words)
ctx.lists["self.punctuation"] = punctuation_words
ctx.lists["self.symbol_key"] = symbol_key_words
ctx.lists["self.number_key"] = {name: str(i) for i, name in enumerate(digits)}
ctx.lists["self.arrow_key"] = {
    "down": "down",
    "left": "left",
    "right": "right",
    "up": "up",
}
```

Replaced by:
```python
ctx.lists["user.punctuation"] = punctuation_dict
ctx.lists["user.symbol_key"]  = symbol_key_dict
ctx_dragon.lists["user.punctuation"] = dragon_punctuation_dict
```

## Legacy `modifier_keys` dict

```python
ctx = Context()
modifier_keys = {
    # If you find 'alt' is often misrecognized, try using 'alter'.
    #"alt": "alt",
    "control": "ctrl",  #'troll':   'ctrl',
    "shift": "shift",  #'sky':     'shift',
    "super": "super",

    #My additions
    'alt key': 'alt',
    'option': 'alt',
    'option key': 'alt',
    "control key": "ctrl",
    "shift key": "shift",
    #"win": "super", #win is often misrecognized as wheel
    'win key': 'super',
}
```

Replaced by [win/modifier_key.talon-list](win/modifier_key.talon-list) and [mac/modifier_key.talon-list](mac/modifier_key.talon-list). Personal additions (`alt key`, `option key`, `control key`, `shift key`, `win key`) and the commented-out `alt` / `win` entries with their reminder notes have been migrated back into both files.

## Legacy `simple_keys` / `alternate_keys` / `special_keys`

```python
simple_keys = [
    #"end",
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
    #"wipe": "backspace",
    #"delete": "backspace",
    #'junk': 'backspace',
    #"forward delete": "delete",
    "page up": "pageup",
    "page down": "pagedown",

    #My additions
    "void": "space",
    "blank": "space",
    "slap": "enter",
    "clear": "backspace",
    #"chuck": "backspace",
    "delete": "delete",
    "end key": "end",
    "home key": "home",
    "tab key": "tab",
}
# mac apparently doesn't have the menu key.
if app.platform in ("windows", "linux"):
    alternate_keys["menu key"] = "menu"
    alternate_keys["print screen"] = "printscr"

special_keys = {k: k for k in simple_keys}
special_keys.update(alternate_keys)
ctx.lists["self.special_key"] = special_keys
ctx.lists["self.function_key"] = {
    f"F {name}": f"f{i}" for i, name in enumerate(f_digits, start=1)
}
```

Replaced by [win/special_key.talon-list](win/special_key.talon-list) and [mac/special_key.talon-list](mac/special_key.talon-list).

## Personal additions migrated back into `special_key.talon-list` (2026-05-06)

The following were re-added to both [win/special_key.talon-list](win/special_key.talon-list) and [mac/special_key.talon-list](mac/special_key.talon-list):

- `void: space`
- `blank: space`
- `slap: enter`
- `clear: backspace`
- `end key: end`
- `home key: home`
- `tab key: tab`
- `delete: delete` (replaces previous `delete: backspace` — "delete" now means forward-delete; use "wipe" or "clear" for backspace)

---

# Legacy formatter dicts (from same conflicted file)

These came from a `core/text/formatters.py` HEAD section in the same conflicted snapshot. The current code lives in `core/formatters/formatters.py` — most of these entries should already be present there; cross-check before re-adding any.

```python
# Mapping from spoken phrases to formatter names
code_formatter_names = {
    "all cap": "ALL_CAPS",
    "all down": "ALL_LOWERCASE",
    "camel": "PRIVATE_CAMEL_CASE",
    #"dotted": "DOT_SEPARATED",
    "dub string": "DOUBLE_QUOTED_STRING",
    #"dunder": "DOUBLE_UNDERSCORE",
    "pascal": "PUBLIC_CAMEL_CASE", #changed from `hammer` to `pascal`
    "kebab": "DASH_SEPARATED",
    #"packed": "DOUBLE_COLON_SEPARATED",
    #"padded": "SPACE_SURROUNDED_STRING",
    "slasher": "ALL_SLASHES",
    "conga": "SLASH_SEPARATED",
    "smash": "NO_SPACES",
    "snake": "SNAKE_CASE",
    "string": "SINGLE_QUOTED_STRING",
    "constant": "ALL_CAPS,SNAKE_CASE",
}
prose_formatter_names = {
    #"say": "NOOP",
    "speak": "NOOP",
    "sentence": "CAPITALIZE_FIRST_WORD",
    "title": "CAPITALIZE_ALL_WORDS",
    #My additions
    #"capitalize": formatters_dict["CAPITALIZE_ALL_WORDS"],
    #"ship": formatters_dict["CAPITALIZE_ALL_WORDS"],
    #"sink": formatters_dict["ALL_LOWERCASE"],
    #"sunk": formatters_dict["ALL_LOWERCASE"],
    #"lowercase": formatters_dict["ALL_LOWERCASE"],
}
reformatter_names = {
    "cap": "CAPITALIZE",
    "list": "COMMA_SEPARATED",
    "unformat": "REMOVE_FORMATTING",
}
word_formatter_names = {
    "word": "ALL_LOWERCASE",
    "trot": "TRAILING_SPACE,ALL_LOWERCASE",
    "proud": "CAPITALIZE_FIRST_WORD",
    "leap": "TRAILING_SPACE,CAPITALIZE_FIRST_WORD",
}
```
