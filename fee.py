from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime

from receipt import show_receipt

from database import (
    search_student,
    update_fee,
    save_payment,
    fetch_payment_history
)


def open_fee():

    win = Toplevel()
    win.title("Fee Collection")
    win.geometry("1000x700")
    win.configure(bg="white")

    # ================= Variables =================

    adm_var = StringVar()
    name_var = StringVar()
    course_var = StringVar()

    total_var = StringVar()
    paid_var = StringVar()
    balance_var = StringVar()

    pay_var = StringVar()

    # ================= Search Student =================

    def search_data():

        if adm_var.get() == "":

            messagebox.showerror(
                "Error",
                "Enter Admission Number",
                parent=win
            )
            return

        row = search_student(adm_var.get())

        if row:

            name_var.set(row[2])
            course_var.set(row[5])

            total_var.set(row[7])
            paid_var.set(row[8])
            balance_var.set(row[9])

        else:

            messagebox.showerror(
                "Error",
                "Student Not Found",
                parent=win
            )

            name_var.set("")
            course_var.set("")
            total_var.set("")
            paid_var.set("")
            balance_var.set("")
            pay_var.set("")

    # ================= Pay Fee =================

    def pay_fee():

        if adm_var.get() == "":
            messagebox.showerror(
                "Error",
                "Search Student First",
                parent=win
            )
            return

        if pay_var.get() == "":
            messagebox.showerror(
                "Error",
                "Enter Pay Amount",
                parent=win
            )
            return

        try:

            amount = int(pay_var.get())
            balance = int(balance_var.get())

            if amount <= 0:
                messagebox.showerror(
                    "Error",
                    "Amount must be greater than 0",
                    parent=win
                )
                return

            if amount > balance:
                messagebox.showerror(
                    "Error",
                    "Amount cannot be greater than Balance Fee",
                    parent=win
                )
                return

            update_fee(adm_var.get(), amount)

            save_payment(
                adm_var.get(),
                name_var.get(),
                amount,
                datetime.now().strftime("%d-%m-%Y")
            )

            messagebox.showinfo(
                "Success",
                "Fee Collected Successfully",
                parent=win
            )

            show_receipt(
                adm_var.get(),
                name_var.get(),
                course_var.get(),
                amount,
                datetime.now().strftime("%d-%m-%Y")
            )

            search_data()
            pay_var.set("")

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e),
                parent=win
            )

    # ================= Payment History =================

    def payment_history():

        if adm_var.get() == "":
            messagebox.showerror(
                "Error",
                "Search Student First",
                parent=win
            )
            return

        rows = fetch_payment_history(adm_var.get())

        history = Toplevel(win)
        history.title("Payment History")
        history.geometry("450x400")

        Label(
            history,
            text="PAYMENT HISTORY",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        table = ttk.Treeview(
            history,
            columns=("date", "amount"),
            show="headings"
        )

        table.heading("date", text="Date")
        table.heading("amount", text="Amount")

        table.column("date", width=180)
        table.column("amount", width=180)

        table.pack(fill=BOTH, expand=True, padx=10, pady=10)

        total = 0

        for row in rows:
            table.insert("", END, values=row)
            total += row[1]

        Label(
            history,
            text=f"Total Paid : ₹ {total}",
            font=("Arial", 12, "bold"),
            fg="green"
        ).pack(pady=10)

    # ================= Heading =================

    Label(
        win,
        text="FEE COLLECTION",
        font=("Arial", 20, "bold"),
        bg="darkblue",
        fg="white",
        pady=10
    ).pack(fill=X)

    # ================= Form =================

    form = Frame(win, bg="white")
    form.pack(pady=20)

    Label(form, text="Admission No", bg="white", font=("Arial",12)).grid(row=0, column=0, padx=10, pady=8, sticky="w")
    Entry(form, textvariable=adm_var, width=30).grid(row=0, column=1)

    Label(form, text="Student Name", bg="white", font=("Arial",12)).grid(row=1, column=0, padx=10, pady=8, sticky="w")
    Entry(form, textvariable=name_var, width=30, state="readonly").grid(row=1, column=1)

    Label(form, text="Course", bg="white", font=("Arial",12)).grid(row=2, column=0, padx=10, pady=8, sticky="w")
    Entry(form, textvariable=course_var, width=30, state="readonly").grid(row=2, column=1)

    Label(form, text="Total Fee", bg="white", font=("Arial",12)).grid(row=3, column=0, padx=10, pady=8, sticky="w")
    Entry(form, textvariable=total_var, width=30, state="readonly").grid(row=3, column=1)

    Label(form, text="Paid Fee", bg="white", font=("Arial",12)).grid(row=4, column=0, padx=10, pady=8, sticky="w")
    Entry(form, textvariable=paid_var, width=30, state="readonly").grid(row=4, column=1)

    Label(form, text="Balance Fee", bg="white", font=("Arial",12)).grid(row=5, column=0, padx=10, pady=8, sticky="w")
    Entry(form, textvariable=balance_var, width=30, state="readonly").grid(row=5, column=1)

    Label(form, text="Pay Amount", bg="white", font=("Arial",12)).grid(row=6, column=0, padx=10, pady=8, sticky="w")
    Entry(form, textvariable=pay_var, width=30).grid(row=6, column=1)

    # ================= Buttons =================

    button_frame = Frame(win, bg="white")
    button_frame.pack(pady=15)

    Button(
        button_frame,
        text="Search",
        width=15,
        bg="blue",
        fg="white",
        command=search_data
    ).pack(side=LEFT, padx=5)

    Button(
        button_frame,
        text="Pay Fee",
        width=15,
        bg="green",
        fg="white",
        command=pay_fee
    ).pack(side=LEFT, padx=5)

    Button(
        button_frame,
        text="Payment History",
        width=18,
        bg="purple",
        fg="white",
        command=payment_history
    ).pack(side=LEFT, padx=5)

    # ================= Keyboard Focus =================

    win.focus_force()
    win.grab_set()

    # Enter key -> Search
    win.bind("<Return>", lambda e: search_data())

    # Escape key -> Close
    win.bind("<Escape>", lambda e: win.destroy())
