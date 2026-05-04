new line: "\n"
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

# Insert delimiter pairs
<user.delimiter_pair>: user.delimiter_pair_insert(delimiter_pair)

# Wrap selection with delimiter pairs
<user.delimiter_pair> (it | selection): user.delimiter_pair_wrap_selection(delimiter_pair)
