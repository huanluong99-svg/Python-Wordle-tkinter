import tkinter as tk

class Settings():
    # Class to define design choices, text colour, bg color, font

    root = tk.Tk()
    def __init__(self):
        self.screen_width = 720
        self.screen_height = 1280
        self.geometry = str(self.screen_width) + "x" + str(self.screen_height)
        self.screen_colour = "#FFE2C3"
        self.cell_colour = "#FBF2ED"
        self.cell_colour_correct = "#C0FFC0"
        self.cell_colour_half = "#FCF18F"
        self.cell_colour_wrong = "#FF6767"
        self.text_colour = "#252525"
        self.text_font = ("Helvetica", 40)
        self.title_font = ("Helvetica Bold", 50)
        self.label_font = ("Helvetica Bold", 30)
        self.button_font = ("Helvetica", 30)
        self.small_button_font = ("Helvetica", 20)
        self.smaller_button_font = ("Helvetica", 10)