#provide both anchored and unachored commands via 'over'
#The difference between `speak` and `phrase` is that `phrase` just emits a sequence of words, while `speak` attempts to handle punctuation & capitalization
phrase <user.text>$:
    user.add_phrase_to_history(text)
    insert(text)
phrase <user.text> {user.phrase_ender}:
    user.add_phrase_to_history(text)
    insert("{text}{phrase_ender}")
{user.prose_formatter} <user.prose>$: user.insert_formatted(prose, prose_formatter)
{user.prose_formatter} <user.prose> {user.phrase_ender}:
    user.insert_formatted(prose, prose_formatter)
    insert(phrase_ender)
<user.format_code>+$: user.insert_many(format_code_list)
<user.format_code>+ {user.phrase_ender}:
    user.insert_many(format_code_list)
    insert(phrase_ender)
<user.formatters> selection: user.formatters_reformat_selection(user.formatters)
(sink | sunk | lowercase) selection: user.formatters_reformat_selection("ALL_LOWERCASE")
<user.formatters> that: user.formatters_reformat_selection(user.formatters)
{user.word_formatter} <user.word>: user.insert_formatted(word, word_formatter)
<user.formatters> (pace | paste): user.insert_formatted(clip.text(), formatters)
recent list: user.toggle_phrase_history()
recent close: user.phrase_history_hide()
recent repeat <number_small>:
    recent_phrase = user.get_recent_phrase(number_small)
    user.add_phrase_to_history(recent_phrase)
    insert(recent_phrase)
recent copy <number_small>: clip.set_text(user.get_recent_phrase(number_small))
# Maybe the commands below should use that instead of it after all
select that: user.select_last_phrase()
before that: user.before_last_phrase()
(nope | scratch) it: user.clear_last_phrase()
nope it was <user.formatters>: user.formatters_reformat_last(formatters)
(abbreviate | abreviate | brief) {user.abbreviation}: "{abbreviation}"
<user.formatters> (abbreviate | abreviate | brief) {user.abbreviation}:
    user.insert_formatted(abbreviation, formatters)



#This one isn't needed as one can say `blank {user.prose_formatter} <user.prose>` just as well
#^pre {user.prose_formatter} <user.prose>$: 
#    key(space)
#    user.insert_formatted(prose, prose_formatter)

^post {user.prose_formatter} <user.prose>$: 
    user.insert_formatted(prose, prose_formatter)
    key(space)

#In Google docs an additional edit.extend_left() seems to be needed but not in other applications/websites
^select around$: 
    edit.word_left()
    edit.extend_word_right()
    edit.extend_word_right()
    #edit.extend_left()

^contract (word | words)$:
    edit.word_left()
    edit.extend_word_right()
    edit.extend_word_right()
    #edit.extend_left()
    user.formatters_reformat_selection("NO_SPACES")

^(sink | sunk | lowercase) word$:
    edit.select_word()
    user.formatters_reformat_selection("ALL_LOWERCASE")

^(ship | uppercase) word$:
    edit.select_word()
    user.formatters_reformat_selection("CAPITALIZE_ALL_WORDS")

# <user.formatters> word:
#     edit.select_word()
#     user.formatters_reformat_selection(user.formatters)

^(ship | uppercase) period$:
    user.navigation_literal_text("GO", "left", "AFTER", ".", 1)
    edit.word_right()
    edit.select_word()
    user.formatters_reformat_selection("CAPITALIZE_ALL_WORDS")
    #edit.left()
    edit.line_end()

^(ship | uppercase) (question | question mark)$:
    user.navigation_literal_text("GO", "left", "AFTER", "?", 1)
    edit.word_right()
    edit.select_word()
    user.formatters_reformat_selection("CAPITALIZE_ALL_WORDS")
    #edit.left()
    edit.line_end()

^(ship | uppercase) (bang | exclamation | exclamation mark)$:
    user.navigation_literal_text("GO", "left", "AFTER", "!", 1)
    edit.word_right()
    edit.select_word()
    user.formatters_reformat_selection("CAPITALIZE_ALL_WORDS")
    #edit.left()
    edit.line_end()

^(ship | uppercase) start$:
    edit.line_start()
    edit.select_word()
    user.formatters_reformat_selection("CAPITALIZE_ALL_WORDS")
    #edit.left()
    edit.line_end()

^(ship | uppercase) line$:
    edit.select_line()
    user.formatters_reformat_selection("CAPITALIZE_FIRST_WORD")
    #edit.left()
    edit.line_end()

^(sink | sunk | lowercase) start$:
    edit.line_start()
    edit.select_word()
    user.formatters_reformat_selection("ALL_LOWERCASE")
    #edit.left()
    edit.line_end()
    
^(sink | sunk | lowercase) <user.symbol_key>$:
    user.navigation_literal_text("GO", "left", "AFTER", symbol_key, 1)
    edit.word_right()
    edit.select_word()
    user.formatters_reformat_selection("ALL_LOWERCASE")
    #edit.left()
    edit.line_end()

#Replace with punctuation symbols
^replace coma$:
    user.replace_text("coma", ",")
    edit.left()
    edit.left()
    key(backspace)
    edit.line_end()

^replace call my$:
    user.replace_text("call my", ",")
    edit.left()
    edit.left()
    key(backspace)
    edit.line_end()

^replace bang$: 
    user.replace_text("bang", "!")
    edit.left()
    edit.left()
    key(backspace)
    edit.line_end()

^replace exclamation$: 
    user.replace_text("exclamation", "!")
    edit.left()
    edit.left()
    key(backspace)
    edit.line_end()

^replace question$: 
    user.replace_text("question", "?")
    edit.left()
    edit.left()
    key(backspace)
    edit.line_end()

^replace eriod$: 
    user.replace_text("eriod", ".")
    edit.left()
    edit.left()
    key(backspace)
    edit.line_end()

#Replace words with words
^replace ok$: 
    user.replace_text("OKAY", "Ok")
    edit.line_end()

#replace will: 
#    user.replace_text("we\'ll", "will")
#    edit.line_end()

^replace high$: 
    user.replace_text("High", "Hi")
    edit.line_end()

^replace one$:
    user.replace_text("1", "one")
    edit.line_end()

^replace two$:
    user.replace_text("2", "to")
    edit.line_end()

^replace four$:
    user.replace_text("4", "for")
    edit.line_end()

##########
# formatters_words = {
#     "all cap": formatters_dict["ALL_CAPS"], #THIS IS A STRING
#     "all down": formatters_dict["ALL_LOWERCASE"], #this is a string
#     "camel": formatters_dict["PRIVATE_CAMEL_CASE"], #thisIsAString
#     "dotted": formatters_dict["DOT_SEPARATED"], #this.is.a.string
#     "dub string": formatters_dict["DOUBLE_QUOTED_STRING"], #"this is a string"
#     #"dunder": formatters_dict["DOUBLE_UNDERSCORE"],
#     #"hammer": formatters_dict["PUBLIC_CAMEL_CASE"], #ThisIsAString
#     "pascal": formatters_dict["PUBLIC_CAMEL_CASE"], #ThisIsAString
#     "kebab": formatters_dict["DASH_SEPARATED"], #this-is-a-string
#     "packed": formatters_dict["DOUBLE_COLON_SEPARATED"], #this::is::a::string
#     "padded": formatters_dict["SPACE_SURROUNDED_STRING"], # this is a string 
#     "slasher": formatters_dict["SLASH_SEPARATED"], #/this/is/a/string
#     "smash": formatters_dict["NO_SPACES"], #thisisastring
#     "snake": formatters_dict["SNAKE_CASE"], #this_is_a_string, underscore separated string
#     "string": formatters_dict["SINGLE_QUOTED_STRING"], #'this is a string'
#     "title": formatters_dict["CAPITALIZE_ALL_WORDS"], #This is a String
# }

#def navigation_literal_text(
#    navigation_action: str,  # GO, EXTEND, SELECT, DELETE, CUT, COPY
#    direction: str,  # up, down, left, right
#    before_or_after: str,  # BEFORE, AFTER, DEFAULT
#    target: str,  # the literal string you're looking for
#    occurrence_number: int,
#):
