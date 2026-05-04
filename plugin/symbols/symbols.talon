new line: "\n"
<<<<<<< HEAD
#double dash: "--"
#triple quote: "'''"
#(triple grave | triple back tick | gravy): insert("```")
(dot dot | dotdot): ".."
ellipsis: "..."
(com space | com blank | com gap): ", "
(dot space | dot blank): ". "
(period space | period blank): ". "
(bang space | bang blank): "! "
(exclamation space | exclamation blank): "! "
#(col space | col blank): ": "
arrow: "->"
dub arrow: "=>"
empty dub string: user.insert_between('"', '"')
empty escaped (dub string | dub quotes): user.insert_between('\\"', '\\"')
empty string: user.insert_between("'", "'")
empty escaped string: user.insert_between("\\'", "\\'")
inside angles: user.insert_between(">", ">")
(inside parens | inside args): user.insert_between("(", ")")
inside (squares | brackets | square brackets | list): user.insert_between("[", "]")
inside (braces | curly | curly brackets): user.insert_between("{", "}")
inside percent: user.insert_between("%", "%")
inside (apostrophe | quotes | string): user.insert_between("'", "'")
inside (double quotes | dub quotes): user.insert_between('"', '"')
inside (graves | back ticks): user.insert_between("`", "`")
angle (it | selection):
    text = edit.selected_text()
    user.paste("<{text}>")
(square | bracket | square bracket) (it | selection):
    text = edit.selected_text()
    user.paste("[{text}]")
(brace | curly | curly bracket) (it | selection):
(parens | args) (it | selection):
    text = edit.selected_text()
    user.paste("({text})")
percent (it | selection):
    text = edit.selected_text()
    user.paste("%{text}%")
(apostrophe | quote | string) (it | selection):
    text = edit.selected_text()
    user.paste("'{text}'")
(double quote | dub quote) (it | selection):
    text = edit.selected_text()
    user.paste('"{text}"')
(grave | back tick) (it | selection):
    text = edit.selected_text()
    user.paste('`{text}`')
=======
double dash: "--"
triple quote: "'''"
triple grave | triple back tick | gravy: "```"
dot dot | dotdot: ".."
ellipsis: "..."
comma and | spamma: ", "
arrow: "->"
dub arrow: "=>"

# Insert delimiter pairs
<user.delimiter_pair>: user.delimiter_pair_insert(delimiter_pair)

# Wrap selection with delimiter pairs
<user.delimiter_pair> that: user.delimiter_pair_wrap_selection(delimiter_pair)
>>>>>>> upstream/main
