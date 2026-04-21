import tkinter as tk
from wordle_gamesettings import Settings
from random import randint

target_word = ''
current_row = 0
current_col = 0
settings = Settings()

word_list = []
with open('5-letter-words.txt', 'r') as file:
    words = file.readlines()
    for word in words:
        word_list.append(word.rstrip())

def on_key(event, entries):
    global current_row, current_col

    # ENTER
    if event.keysym == "Return":
        on_enter(entries)
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

def on_enter(entries):
    global target_word, current_row, current_col

    guess_word = "".join(e.get() for e in entries[current_row])

    if "" in [e.get() for e in entries[current_row]]:
        return "break"

    if guess_word.lower() not in word_list:
        for e in entries[current_row]:
            e.delete(0, tk.END)
        current_col = 0
        entries[current_row][0].focus_set()
        return "break"

    # Check if the word is correct 
    guess_list = [] 
    for letter in guess_word: 
        guess_list.append(letter)

    target_list = [] 
    for letter in target_word: 
        target_list.append(letter) 
        print(guess_list) 
        print(target_list)
    
    i = 0 
    while i < len(guess_list): 
        e = guess_list[i] 
        if e == target_list[i]: # correct_position 
            entries[current_row][i].config(disabledbackground=settings.cell_colour_correct) 
            print(e, "was correct") 
        elif e in target_list: # in word, wrong spot 
            entries[current_row][i].config(disabledbackground=settings.cell_colour_half) 
            print(e, "was in word, wrong spot") 
        elif e not in target_list: # not in word at all 
            entries[current_row][i].config(disabledbackground=settings.cell_colour_wrong) 
            print(e, "was not in word") 
        i += 1

    # check letters...
    # (your logic stays the same)

    for e in entries[current_row]:
        e.config(state="disabled")

    current_row += 1
    current_col = 0

    update_row_states(entries)

    if current_row < len(entries):
        entries[current_row][0].focus_set()

    return "break"

# function to generate a new 5-letter word
def generate_new_word():
    
    target_word = word_list[randint(0,len(word_list))]
    return target_word

# function to start a new game
def start_new_game(entries):
    settings = Settings()
    global target_word, current_row, current_col
    
    #reset game state
    current_row = 0
    current_col = 0
    
    for row in entries:
        for col in row:
            col.config(
                    state="normal",
                    bg=settings.cell_colour, 
                    fg=settings.text_colour, 
                    disabledbackground=settings.cell_colour
                )
            col.delete(0, 'end')

    # get new target word
    target_word = generate_new_word().upper()
    
    update_row_states(entries)

    entries[0][0].focus_set()
    print("Game Reset")
    print("New word set to:", target_word)
    print("ROW:", current_row, "COL:", current_col)



# function to change cell colour if found on enter
def keyboard_button(root, entries, letter):
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

    for r, row in enumerate(entries):
        for e in row:
            if r == current_row:
                e.config(state="normal")
            else:
                e.config(state="disabled")

