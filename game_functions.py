import tkinter as tk
from wordle_gamesettings import Settings
from random import randint
from collections import Counter

target_word = ''
current_row = 0
current_col = 0
correct_letters = set()   # green
present_letters = set()   # yellow
wrong_letters = set()     # grey
target_list = []
settings = Settings()

word_list = []
with open('5-letter-words.txt', 'r') as file:
    words = file.readlines()
    for word in words:
        word_list.append(word.rstrip())

def on_key(event, entries, keyboard_entries, label):
    global current_row, current_col

    # ENTER
    if event.keysym == "Return":
        on_enter(entries, keyboard_entries, label)
        return "break"

    # BACKSPACE
    if event.keysym == "BackSpace":
        on_backspace(entries)
        return "break"

    # ignore non letters
    if not event.char.isalpha():
        return "break"

    # safety
    if current_row >= len(entries):
        return "break"

    if current_col < len(entries[current_row]):
        cell = entries[current_row][current_col]
        cell.config(state="normal")
        cell.delete(0, "end")
        cell.insert(0, event.char.upper())
        current_col += 1

    return "break"

def on_backspace(entries):
    global current_row, current_col

    if current_col <= 0:
        return

    current_col -= 1

    cell = entries[current_row][current_col]
    cell.config(state="normal")
    cell.delete(0, "end")

def on_enter(entries, keyboard_entries, label):
    global target_word, current_row, current_col, target_list, guessed_letters

    # set up the guess word from entries
    guess_word = "".join(e.get() for e in entries[current_row])

    # reset the statement
    change_statement_label(label, "")

    # check that there are no empty cells
    if "" in [e.get() for e in entries[current_row]]:
        return "break"

    # check that the guessed word is included in the list
    if guess_word.lower() not in word_list:
        for e in entries[current_row]:
            e.delete(0, tk.END)
        current_col = 0
        entries[current_row][0].focus_set()
        change_statement_label(label, "Word does not exist in list")
        return "break"

    # Check if the word is correct 
    guess_list = [] 
    for letter in guess_word: 
        guess_list.append(letter)
    

    print(guess_list)
    print(target_list)

    # This part is for avoiding the assumption of double letters in a guess
    # creates a counter of each unique letter in the word
    target_letter_count = Counter(target_list)
    print(target_letter_count)

    # configure each field colour to green yellow or red
    i = 0 
    while i < len(guess_list): 
        e = guess_list[i]
        if e == target_list[i]: # correct_position 
            entries[current_row][i].config(disabledbackground=settings.cell_colour_correct) 
            target_letter_count[e] -= 1
            print(e, "was correct")
            print(e, "count reduced by 1")
            print(target_letter_count)

        elif e in target_list and target_letter_count[e] != 0: # in word, wrong spot 
            entries[current_row][i].config(disabledbackground=settings.cell_colour_half) 
            print(e, "was in word, wrong spot") 
        else: # not in word at all 
            entries[current_row][i].config(disabledbackground=settings.cell_colour_wrong) 
            print(e, "was not in word") 
        if e == target_list[i]:
            correct_letters.add(e)
        elif e in target_list:
            present_letters.add(e)
        else:
            wrong_letters.add(e)
        i += 1
    
    # win statement
    if guess_list == target_list:
        change_statement_label(label, "You win!")

    # lose statement, show the answer word
    """if guess_list != target_list and current_row == 6:
        change_statement_label(label, "You lose! The answer was", target_word)
    """
    # disable the current row to avoid being changed, then move to the next row
    for e in entries[current_row]:
        e.config(state="disabled")

    current_row += 1
    current_col = 0

    update_row_states(entries)

    if current_row < len(entries):
        entries[current_row][0].focus_set()
    else:
        lose_statement = "You lose! The answer was " + target_word
        change_statement_label(label, lose_statement)
    
    change_keyboard_colour(keyboard_entries)

    return "break"

def change_statement_label(label, statement):
    label.config(text=statement)

def change_keyboard_colour(keyboard_entries):
    # change colours of keyboard to indicate what letters have been used
    print("CHANGING KEYBOARD COLOURS")
    print(correct_letters)
    print(present_letters)
    print(wrong_letters)

    for row in keyboard_entries:
        for label in row:
            
            key = label["text"].lower()

            if key in ["ent", "bksp"]:
                continue

            if key.upper() in correct_letters:
                colour = settings.cell_colour_correct
            elif key.upper() in present_letters:
                colour = settings.cell_colour_half
            elif key.upper() in wrong_letters:
                colour = settings.cell_colour_wrong
            else:
                continue
            
            label.config(bg=colour)
            
    # make sure that the keyboard actually changes colour
    keyboard_entries[0][0].update_idletasks()

# function to generate a new 5-letter word
def generate_new_word():
    global target_list
    
    target_list.clear()

    target_word = word_list[randint(0, len(word_list)-1)]

    for letter in target_word: 
        target_list.append(letter.upper())

    return target_word

# function to start a new game
def start_new_game(entries, keyboard_entries, label):
    settings = Settings()
    global target_word, current_row, current_col
    global correct_letters, present_letters, wrong_letters, target_list
    
    change_statement_label(label, "")
    
    # reset everything
    current_row = 0
    current_col = 0
    correct_letters.clear()
    present_letters.clear()
    wrong_letters.clear()
    target_list.clear()
    
    for row in entries:
        for col in row:
            col.config(
                    state="normal",
                    bg=settings.cell_colour, 
                    fg=settings.text_colour, 
                    disabledbackground=settings.cell_colour
                )
            col.delete(0, 'end')
    
    for row in keyboard_entries:
        for label in row:
            label.config(bg=settings.cell_colour)

    # get new target word
    target_word = generate_new_word().upper()
    
    update_row_states(entries)

    entries[0][0].focus_set()
    print("Game Reset")
    print("New word set to:", target_word)
    print("ROW:", current_row, "COL:", current_col)


# function to change cell colour if found on enter
def keyboard_button(entries, letter):
    global current_row, current_col

    if current_row >= len(entries):
        return

    if current_col >= len(entries[current_row]):
        return

    cell = entries[current_row][current_col]

    cell.config(state="normal")
    cell.delete(0, "end")
    cell.insert(0, letter.upper())

    current_col += 1

    if current_col < len(entries[current_row]):
        entries[current_row][current_col].focus_set()

def update_row_states(entries):
    global current_row

    # sets current row state to normal and disables the others
    for r, row in enumerate(entries):
        for e in row:
            if r == current_row:
                e.config(state="normal")
            else:
                e.config(state="disabled")
