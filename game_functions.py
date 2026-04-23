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
game_over = False

word_list = []
with open('5-letter-words.txt', 'r') as file:
    words = file.readlines()
    for word in words:
        word_list.append(word.rstrip())

def on_key(event, entries, keyboard_entries, label):
    global current_row, current_col, game_over

    # break if the game_over flag is true
    if game_over:
        return "break"

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
    
    # store result states
    results = [''] * len(guess_list)

    # pass 1 - greens first
    
    for i in range(len(guess_list)):
        e = guess_list[i]
        if e == target_list[i]: # correct_position 
            entries[current_row][i].config(disabledbackground=settings.cell_colour_correct) 
            target_letter_count[e] -= 1
            results[i] = "green"
            print(e, "was correct")
            print(e, "count reduced by 1")
            print(target_letter_count)
        

    # pass 2 - yellows and reds next
    for i in range(len(guess_list)):
        e = guess_list[i]
        if results[i] == "green":
            continue
        
        if e in target_list and target_letter_count[e] > 0: # in word, wrong spot, no duplicates in correct spot
            entries[current_row][i].config(disabledbackground=settings.cell_colour_half) 
            print(e, "was in word, wrong spot") 
            results[i] = "yellow"

        else: # not in word at all 
            entries[current_row][i].config(disabledbackground=settings.cell_colour_wrong) 
            print(e, "was not in word")

            results[i] = "red"

    # add to correct letters if correct
    # add to present letters only if doesn't meet correct letters
    # add to wrong letters only if correct letters don't have them
    for i in range(len(guess_list)):
        e = guess_list[i]
        if e == target_list[i]:
            correct_letters.add(e)
        if e in target_list and e not in correct_letters:
            present_letters.add(e)
        if e not in target_list and e not in correct_letters and e not in present_letters:
            wrong_letters.add(e)
    
    # disable the current row to avoid being changed, then move to the next row
    for e in entries[current_row]:
        e.config(state="disabled")

    current_row += 1
    current_col = 0

    # win statement
    if guess_list == target_list:
        global game_over
        game_over = True
        change_statement_label(label, "You win!")
        
        # disable all cells
        for row in entries:
            for col in row:
                col.config(state="disabled")
    else:
        update_row_states(entries)

    if current_row < len(entries) and guess_list != target_list:
        entries[current_row][0].focus_set()
    
    if current_row >= len(entries) and not game_over:
        game_over = True
        lose_statement = "You lose! The answer was " + target_word
        change_statement_label(label, lose_statement)
    
    change_keyboard_colour(keyboard_entries)

    return "break"

def change_statement_label(label, statement):
    label.config(text=statement)

def change_keyboard_colour(keyboard_entries):
    # change colours of keyboard to indicate what letters have been used
    print("CHANGING KEYBOARD COLOURS")
    print("correct:", correct_letters)
    print("present:", present_letters)
    print("wrong:", wrong_letters)

    for row in keyboard_entries:
        for label in row:
            
            key = label["text"].lower()

            if key in ["ent", "bksp"]:
                continue

            
            if key.upper() in wrong_letters:
                colour = settings.cell_colour_wrong
            elif key.upper() in present_letters and key.upper() not in correct_letters:
                colour = settings.cell_colour_half
            elif key.upper() in correct_letters:
                colour = settings.cell_colour_correct
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
    global game_over
    game_over = False
    
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
    global current_row, current_col, game_over

    if game_over:
        return

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
