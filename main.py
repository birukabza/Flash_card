from tkinter import *
from tkinter import messagebox
import pandas
import os
from random import choice
import pygame

BACKGROUND_COLOR = "#B1DDC6"
try:
    data = pandas.read_csv("data/progress.csv")
    to_learn = data.to_dict(orient="records")
except FileNotFoundError:
    original_data = pandas.read_csv("data/Spanish_to_English.csv")
    to_learn = original_data.to_dict(orient="records")

current_card = {}
pygame.mixer.init()


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(to_learn)
    canvas.itemconfig(language, text="Spanish", fill="black")
    canvas.itemconfig(word, text=current_card["Spanish"], fill="black")
    canvas.itemconfig(image, image=card_front)
    flip_timer = window.after(4000, func=flip_card)
    play_sound()


def flip_card():
    pygame.mixer.music.pause()
    canvas.itemconfig(language, text="English", fill="white")
    canvas.itemconfig(word, text=current_card["English"], fill="white")
    canvas.itemconfig(image, image=card_back)


def is_known():
    global current_card
    play_sound()
    if len(to_learn) > 1:
        to_learn.remove(current_card)
        df = pandas.DataFrame(to_learn)
        df.to_csv("data/progress.csv", index=False)
        next_card()
    else:
        messagebox.showinfo(title="There's no word to learn",
                            message="Congratulation! You know all the words!\nkeep up the good work!")
        os.remove("data/progress.csv")


def play_sound():
    tick_sound_path = "music/tick_sound.wav"
    pygame.mixer.music.load(tick_sound_path)
    pygame.mixer.music.play(-1)


window = Tk()
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
window.title("Flash Card")
flip_timer = window.after(3000, func=flip_card)

# canvas
canvas = Canvas(width=800, height=526, highlightthickness=0)
card_back = PhotoImage(file="images/card_back.png")
card_front = PhotoImage(file="images/card_front.png")
image = canvas.create_image(400, 263, image=card_front)
language = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR)
canvas.grid(row=0, column=0, columnspan=2, )

# Buttons
wrong_img = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=wrong_img, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

right_img = PhotoImage(file="images/right.png")
known_button = Button(image=right_img, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

next_card()

window.mainloop()
