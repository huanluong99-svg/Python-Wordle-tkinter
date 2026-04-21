import tkinter as tk
from tkinter import ttk, messagebox
from wordle_gamesettings import Settings
import game_functions as gf

def run_wordle_game():
    # function to run the game

    # make the game window
    root = tk.Tk()
    settings = Settings()
    root.title("Huan's Wordle Game")
    root.geometry(settings.geometry)
    root.configure(bg=settings.screen_colour)

    # game title label
    game_title = tk.Label(
        root, text="Huan's Wordle Game", font = settings.text_font, pady=30, 
        bg=settings.screen_colour, fg = settings.text_colour
        )
    game_title.pack()

    # making rows of inputs
    def make_rows():
        
        # 5x6 grid
        
        letters_frame = tk.Frame(root)
        letters_frame.pack(pady=10)

        rows = 6
        cols = 5

        entries = [] #2D list: entries [row][col]

        for r in range(rows):
            row_entries = []

            for c in range(cols):
                e = tk.Entry(
                    letters_frame, width=2, font = settings.text_font, justify='center', 
                    bg=settings.cell_colour, fg = settings.text_colour
                    )
                e.grid(column=c,row=r)
                # apply the jump function, backspace function, and enter function
                e.bind("<KeyPress>", lambda event: gf.on_key(event, entries))

                row_entries.append(e)
            entries.append(row_entries)
        
        entries[0][0].focus_set()
        
        gf.start_new_game(entries)
        

        #start new game button
        reset_button = tk.Button(root, text='New Game', font = settings.button_font, pady=10, 
            bg=settings.screen_colour, fg = settings.text_colour,
            command=lambda: gf.start_new_game(entries)
            )
        reset_button.pack(pady=5)
        

        # Keyboard layout
        keyboard_frame = tk.Frame(root)
        keyboard_frame.pack(pady=1)
        
        keyboard_letters_list = [['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'], ['a','s','d','f','g','h','j','k','l'], ['enter', 'z','x','c','v','b','n','m', 'backspace']]
        keyboard_entries = []
        for r, row in enumerate(keyboard_letters_list):
            keyboard_row_entries = []
            for c, letter in enumerate(row):
                letter_button = tk.Button(keyboard_frame, 
                    text=letter.upper(),
                    width=1, font = settings.small_button_font, 
                    bg=settings.cell_colour, fg = settings.text_colour
                    )
                if letter == 'enter':
                    letter_button.config(
                        font=settings.smaller_button_font,
                        command=lambda: gf.on_enter(entries)
                        )
                elif letter == 'backspace':
                    letter_button.config(
                        font=settings.smaller_button_font,
                        command=lambda: gf.on_backspace(entries)
                        )
                else:
                    letter_button.config(
                        command=lambda l=letter: gf.keyboard_button(root, entries, l)
                        )

                letter_button.grid(column=c, row=r, padx=1, pady=1)
                keyboard_row_entries.append(letter_button)
            keyboard_entries.append(keyboard_row_entries)
        


    make_rows()

    root.mainloop()

run_wordle_game()