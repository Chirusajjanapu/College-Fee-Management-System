from tkinter import *
from tkinter import messagebox
import tempfile
import webbrowser


# ================= Print Receipt ================= #

def print_receipt(adm, name, course, amount, date):

    html = f"""
    <html>
    <head>
        <title>College Fee Receipt</title>
    </head>

    <body style="font-family:Arial; padding:40px;">

        <h2 align="center">COLLEGE FEE RECEIPT</h2>
        <hr>

        <p><b>Admission No :</b> {adm}</p>
        <p><b>Student Name :</b> {name}</p>
        <p><b>Course :</b> {course}</p>
        <p><b>Paid Amount :</b> ₹ {amount}</p>
        <p><b>Date :</b> {date}</p>

        <br><br>

        <h3 align="center">Thank You</h3>

        <script>
            window.onload = function(){{
                window.print();
            }}
        </script>

    </body>
    </html>
    """

    file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".html",
        mode="w",
        encoding="utf-8"
    )

    file.write(html)
    file.close()

    webbrowser.open("file://" + file.name)


# ================= Receipt Window ================= #

def show_receipt(adm, name, course, amount, date):

    win = Toplevel()
    win.title("Fee Receipt")
    win.geometry("450x500")
    win.configure(bg="white")

    Label(
        win,
        text="SAI SAMATH DEGREE COLLAGE\nCOLLEGE FEE RECEIPT",
        font=("Arial",18,"bold"),
        bg="darkblue",
        fg="white",
        pady=10
    ).pack(fill=X)

    Frame(win, height=20, bg="white").pack()

    Label(
        win,
        text=f"Admission No : {adm}",
        bg="white",
        font=("Arial",12),
        anchor="w"
    ).pack(fill=X, padx=25, pady=5)

    Label(
        win,
        text=f"Student Name : {name}",
        bg="white",
        font=("Arial",12),
        anchor="w"
    ).pack(fill=X, padx=25, pady=5)

    Label(
        win,
        text=f"Course : {course}",
        bg="white",
        font=("Arial",12),
        anchor="w"
    ).pack(fill=X, padx=25, pady=5)

    Label(
        win,
        text=f"Paid Amount : ₹ {amount}",
        bg="white",
        fg="green",
        font=("Arial",12,"bold"),
        anchor="w"
    ).pack(fill=X, padx=25, pady=5)

    Label(
        win,
        text=f"Date : {date}",
        bg="white",
        font=("Arial",12),
        anchor="w"
    ).pack(fill=X, padx=25, pady=5)

    Label(
        win,
        text="Thank You\nVisit Again",
        bg="white",
        fg="blue",
        font=("Arial",14,"bold")
    ).pack(pady=25)

    Button(
        win,
        text="Print",
        bg="green",
        fg="white",
        width=15,
        command=lambda: print_receipt(
            adm,
            name,
            course,
            amount,
            date
        )
    ).pack(pady=10)

    Button(
        win,
        text="Close",
        bg="red",
        fg="white",
        width=15,
        command=win.destroy
    ).pack()
