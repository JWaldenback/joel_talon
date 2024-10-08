# Compound of action(select, clear, copy, cut, paste, etc.) and modifier(word, line, etc.) commands for editing text.
# eg: "select line", "clear all"
<user.edit_action> <user.edit_modifier>: user.edit_command(edit_action, edit_modifier)

# Zoom
zoom in: edit.zoom_in()
zoom out: edit.zoom_out()
zoom reset: edit.zoom_reset()

# Searching
find it: edit.find()
next one: edit.find_next()
last one: edit.find_previous()

# Navigation

# The reason for these spoken forms is that "page up" and "page down" are globally defined as keys.
#scroll up: edit.page_up()
#scroll down: edit.page_down()

<<<<<<< HEAD
go word left: edit.word_left()
go pre [word]$: edit.word_left()
go word right: edit.word_right()
go post [word]$: 
    edit.word_right()
    edit.left()

go left: edit.left()
go right: edit.right()
go up: edit.up()
go down: edit.down()
=======
# go left, go left left down, go 5 left 2 down
# go word left, go 2 words right
go <user.navigation_step>+: user.perform_navigation_steps(navigation_step_list)
>>>>>>> upstream/main

go (line start | head): edit.line_start()
go (line end | tail): edit.line_end()

go way left:
    edit.line_start()
    edit.line_start()
go way right: edit.line_end()
go way up: edit.file_start()
go way down: edit.file_end()

go top: edit.file_start()
go bottom: edit.file_end()

go page up: edit.page_up()
go page down: edit.page_down()

# Selecting

select left: edit.extend_left()
select right: edit.extend_right()
select up: edit.extend_line_up()
select down: edit.extend_line_down()

select word left: edit.extend_word_left()
select word right: edit.extend_word_right()

select way left: edit.extend_line_start()
select way right: edit.extend_line_end()
select way up: edit.extend_file_start()
select way down: edit.extend_file_end()

# Indentation
indent [more]: edit.indent_more()
(indent less | dedent | out dent): edit.indent_less()

# Delete
<<<<<<< HEAD
#clear all: user.delete_all() #Removed this functionality to prevent unwanted mistakes
clear line: edit.delete_line()
clear line start: user.delete_line_start()
clear line end: user.delete_line_end()
=======
>>>>>>> upstream/main
clear left: edit.delete()
clear right: user.delete_right()

clear up:
    edit.extend_line_up()
    edit.delete()

clear down:
    edit.extend_line_down()
    edit.delete()

<<<<<<< HEAD
clear word: edit.delete_word()

(clear word left | cleft):
=======
clear word left:
>>>>>>> upstream/main
    edit.extend_word_left()
    edit.delete()

(clear word right | cright):
    edit.extend_word_right()
    edit.delete()

clear way left:
    edit.extend_line_start()
    edit.delete()

clear way right:
    edit.extend_line_end()
    edit.delete()

clear way up:
    edit.extend_file_start()
    edit.delete()

clear way down:
    edit.extend_file_end()
    edit.delete()

# Copy
<<<<<<< HEAD
(copy it | copy selection): 
    edit.copy()
    user.hud_add_log('success', 'Content copied')  
copy all: 
    user.copy_all()
    user.hud_add_log('success', 'Content copied')
copy line: 
    user.copy_line()
    user.hud_add_log('success', 'Content copied')
copy line start: 
    user.copy_line_start()
    user.hud_add_log('success', 'Content copied')
copy line end: 
    user.copy_line_end()
    user.hud_add_log('success', 'Content copied')
copy word: 
    user.copy_word()
    user.hud_add_log('success', 'Content copied')
copy word left: 
    user.copy_word_left()
    user.hud_add_log('success', 'Content copied')
copy word right: 
    user.copy_word_right()
    user.hud_add_log('success', 'Content copied')
=======
copy that: edit.copy()
copy word left: user.copy_word_left()
copy word right: user.copy_word_right()
>>>>>>> upstream/main

#to do: do we want these variants, seem to conflict
# copy left:
#      edit.extend_left()
#      edit.copy()
# copy right:
#     edit.extend_right()
#     edit.copy()
# copy up:
#     edit.extend_up()
#     edit.copy()
# copy down:
#     edit.extend_down()
#     edit.copy()

# Cut
<<<<<<< HEAD
(cut | carve) (it | selection): edit.cut()
(cut | carve) all: user.cut_all()
(cut | carve) line: user.cut_line()
(cut | carve) line start: user.cut_line_start()
(cut | carve) line end: user.cut_line_end()
(cut | carve) word: user.cut_word()
(cut | carve) word left: user.cut_word_left()
(cut | carve) word right: user.cut_word_right()
=======
cut that: edit.cut()
cut word left: user.cut_word_left()
cut word right: user.cut_word_right()
>>>>>>> upstream/main

#to do: do we want these variants
# cut left:
#      edit.select_all()
#      edit.cut()
# cut right:
#      edit.select_all()
#      edit.cut()
# cut up:
#      edit.select_all()
#     edit.cut()
# cut down:
#     edit.select_all()
#     edit.cut()

# Paste
<<<<<<< HEAD
(pace | paste) it: edit.paste()
#(pace | paste) enter:
#    edit.paste()
#    key(enter)
(pace | paste) (plain | match style): edit.paste_match_style()
(pace | paste) all: user.paste_all()
(pace | paste) line: user.paste_line()
(pace | paste) line start: user.paste_line_start()
(pace | paste) line end: user.paste_line_end()
(pace | paste) word: user.paste_word()
=======
(pace | paste) that: edit.paste()
(pace | paste) enter:
    edit.paste()
    key(enter)
paste match: edit.paste_match_style()
>>>>>>> upstream/main

# Duplication
clone that: edit.selection_clone()
clone line: edit.line_clone()

# Insert new line
new line above: edit.line_insert_up()
new line below: edit.line_insert_down()
(new line | line new): edit.line_insert_down()
(new paragraph | paragraph new): 
  edit.line_insert_down() 
  edit.line_insert_down()

# Insert padding with optional symbols
(pad | padding): user.insert_between(" ", " ")
(pad | padding) <user.symbol_key>+:
    insert(" ")
    user.insert_many(symbol_key_list)
    insert(" ")

# Undo/redo
undo it: edit.undo()
redo it: edit.redo()

# Save
(file | five) save: edit.save()
(file | five) save all: edit.save_all()

[go] line mid: user.line_middle()



#THE COMMANDS BELOW ARE FROM DICTATION_MODE.TALON
# Navigation
go up <number_small> (line|lines):
    edit.up()
    repeat(number_small - 1)
go down <number_small> (line|lines):
    edit.down()
    repeat(number_small - 1)
go left <number_small> (word|words):
    edit.word_left()
    repeat(number_small - 1)
go right <number_small> (word|words):
    edit.word_right()
    repeat(number_small - 1)
    
# Selection
select left <number_small> (word|words):
    edit.extend_word_left()
    repeat(number_small - 1)
select right <number_small> (word|words):
    edit.extend_word_right()
    repeat(number_small - 1)
select left <number_small> (character|characters):
    edit.extend_left()
    repeat(number_small - 1)
select right <number_small> (character|characters):
    edit.extend_right()
    repeat(number_small - 1)
clear left <number_small> (word|words):
    edit.extend_word_left()
    repeat(number_small - 1)
    edit.delete()
clear right <number_small> (word|words):
    edit.extend_word_right()
    repeat(number_small - 1)
    edit.delete()
clear left <number_small> (character|characters):
    edit.extend_left()
    repeat(number_small - 1)
    edit.delete()
clear right <number_small> (character|characters):
    edit.extend_right()
    repeat(number_small - 1)
    edit.delete()
new line below | slap: edit.line_insert_down()
