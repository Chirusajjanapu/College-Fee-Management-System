from tkinter import *
from PIL import Image, ImageTk


def add_header(win, title):

    top = Frame(win, bg="darkblue", height=90)
    top.pack(fill=X)

    img = Image.open("college_logo.png")
    img = img.resize((60, 60))

    logo = ImageTk.PhotoImage(img)

    logo_label = Label(
        top,
        image=logo,
        bg="darkblue"
    )
    logo_label.image = logo
    logo_label.pack(side=LEFT, padx=15, pady=10)

    text_frame = Frame(top, bg="darkblue")
    text_frame.pack(side=LEFT, padx=10)

    Label(
        text_frame,
        text="SAI SAMATH DEGREE & INTER COLLEGE",
        font=("Arial", 18, "bold"),
        bg="darkblue",
        fg="white"
    ).pack(anchor="w")

    Label(
        text_frame,
        text=title,
        font=("Arial", 12, "bold"),
        bg="darkblue",
        fg="white"
    ).pack(anchor="w")
