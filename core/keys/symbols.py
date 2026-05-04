# fmt: off

# define the spoken forms for symbols in command and dictation mode
punctuation_dict = {}

# for dragon, we add a couple of mappings that don't work for conformer
# i.e. dragon supports some actual symbols as the spoken form
dragon_punctuation_dict = {
    "`": "`",
    ",": ",",
}

# define the spoken forms for symbols that are intended for command mode only
symbol_key_dict = {}

# define spoken form for symbols for use in create_spoken_forms.py functionality
# we define a handful of symbol only. at present, this is restricted to one entry per symbol.
symbols_for_create_spoken_forms = {
    # for application names like "Movies & TV"
    "and": "&",
    # for emails
    "at": "@",
    "dot": ".",
    # for application names like "notepad++"
    "plus": "+",
}


class Symbol:
    character: str
    command_and_dictation_forms: list[str] = None
    command_forms: list[str] = None

    def __init__(
        self, character: str, command_and_dictation_forms=None, command_forms=None
    ):
        self.character = character

        if command_and_dictation_forms:
            self.command_and_dictation_forms = (
                [command_and_dictation_forms]
                if isinstance(command_and_dictation_forms, str)
                else command_and_dictation_forms
            )

        if command_forms:
            self.command_forms = (
                [command_forms] if isinstance(command_forms, str) else command_forms
            )

currency_symbols = [
    Symbol("$", ["dollar sign"], ["dollar"]),
    Symbol("£", ["pound sign"], ["pound"]),
    Symbol("€", ["euro sign"], ["euro"]),
]

symbols = [
    Symbol("`", ["back tick"], ["grave"]),
    Symbol(",", ["comma", "coma"]),
    Symbol(".", ["period", "full stop"], ["dot", "point"]),
    Symbol(";", ["semicolon"], ["semi"]),
    Symbol(":", ["colon"]),
    Symbol("?", ["question mark"], ["question"]),
    Symbol("!", ["exclamation mark", "exclamation point"], ["bang"]),
    Symbol("*", ["asterisk"], ["star"]),
    Symbol("#", ["hash sign", "number sign"], ["hash"]),
    Symbol("%", ["percent sign"], ["percent"]),
    Symbol("@", ["at symbol", "at sign"]),
    Symbol("°", ["degree sign"], ["degree", "degrees"]),
    Symbol("&", ["ampersand", "and sign"], ["amper"]),
    Symbol("-", ["hyphen"], ["minus", "dash"]),
    Symbol("–", ["en dash", "nut dash"]),
    Symbol("—", ["em dash", "mutton dash"]),
    Symbol("=", None, ["equals"]),
    Symbol("+", None, ["plus"]),
    Symbol("~", None, ["tilde"]),
    Symbol("_", None, ["down score", "underscore"]),
    Symbol("(", ["paren", "L paren", "left paren"]),
    Symbol(")", ["R paren", "right paren"]),
    Symbol("[", None,["brack", "L brack", "bracket", "L bracket", "left bracket", "square", "L square", "left square",],),
    Symbol("]", None, ["R brack", "R bracket", "right bracket", "R square", "right square"]),
    Symbol("/", ["forward slash"], ["slash"]),
    Symbol("\\", None, ["backslash"]),
    Symbol("{", None, ["brace", "L brace", "left brace", "curly bracket", "left curly bracket"],),
    Symbol("}", None, ["R brace", "right brace","R curly bracket", "right curly bracket"]),
    Symbol("<", None, ["angle", "L Angle", "left angle", "less than"]),
    Symbol(">", None, ["rangle", "R angle", "right angle", "greater than"]),
    Symbol("^", None, ["caret"]),
    Symbol("|", None, ["pipe"]),
    Symbol("'", None, ["quote", "apostrophe"]),
    Symbol('"', None, ["dub quote", "double quote"]),
]

# `punctuation_words` is for words you want available BOTH in dictation and as key names in command mode.
# `symbol_key_words` is for key names that should be available in command mode, but NOT during dictation.
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

# by convention, symbols should include currency symbols
symbols.extend(currency_symbols)

for symbol in symbols:
    if symbol.command_and_dictation_forms:
        for spoken_form in symbol.command_and_dictation_forms:
            punctuation_dict[spoken_form] = symbol.character
            symbol_key_dict[spoken_form] = symbol.character
            dragon_punctuation_dict[spoken_form] = symbol.character

    if symbol.command_forms:
        for spoken_form in symbol.command_forms:
            symbol_key_dict[spoken_form] = symbol.character
