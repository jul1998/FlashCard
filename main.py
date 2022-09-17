import random

BACKGROUND_COLOR = "#B1DDC6"
from tkinter import *
import pandas






#--------------------------------Read CSV-----------------------------------------------------

try:
    data = pandas.read_csv("./data/known_words.csv")
except FileNotFoundError:
    data = pandas.read_csv("./data/german_words.csv")
    dict_data = data.to_dict(orient="records")
else:
    dict_data = data.to_dict(orient="records")
finally:
    current_title_and_word = {}

#--------------------------------Functions-----------------------------------------------------

def show_next_word():
    global flip_timer
    global current_title_and_word

    # Pick a random pair from dict_data
    current_title_and_word = random.choice(dict_data)

    # Change word from canvas
    canvas.itemconfig(word, text=current_title_and_word["German"], fill="black")

    # Change canvas image to front image
    canvas.itemconfig(front_image_canvas, image=front_image)

    # Change title from canvas
    canvas.itemconfig(language, text="German", fill="black")

    # Once button is pressed, flip_timer (the one outside this function) is cancelled, then
    # flip_timer stores a new 3s timer
    wn.after_cancel(flip_timer)
    flip_timer = wn.after(3000, flip_card)

def flip_card():
    canvas.itemconfig(front_image_canvas, image=back_image)
    canvas.itemconfig(language, text="English", fill="white")
    canvas.itemconfig(word, text=current_title_and_word["English"], fill="white")

def word_is_known():
    # Removes words that user knows
    dict_data.remove(current_title_and_word)

    # Calling this function causes that current_title_and_word dict will not be empty
    show_next_word()

    # Creates a new csv file, but with words that are known are not included
    new_data = pandas.DataFrame(dict_data)

    # Stores this new data in a new csv file
    new_data.to_csv("./data/known_words.csv")

    print(len(dict_data))

#--------------------------------GUI-----------------------------------------------------

#Set up window
wn = Tk()
wn.title("Flash card")
wn.config(bg=BACKGROUND_COLOR, padx=50, pady=20)
flip_timer = wn.after(3000, flip_card)
#Create canvas
canvas = Canvas(height=526, width=800, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

#Create front image for canvas
front_image = PhotoImage(file="./images/card_front.png")
front_image_canvas = canvas.create_image(405, 270, image=front_image)

#Create back image for canvas
back_image = PhotoImage(file="./images/card_back.png")

#Create text in canvas
language = canvas.create_text(400, 150, text="German", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text="Start", font=("Ariel", 60, "bold"))

#Create button for right image
right_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=word_is_known)
right_button.grid(column=0, row=1)

#Create button for wrong image
wrong_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=show_next_word)
wrong_button.grid(column=1, row=1)


show_next_word()


wn.mainloop()
