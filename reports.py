from tkinter import *
from tkinter import ttk
from database import (
    fetch_students,
    fetch_pending_students,
    fetch_paid_students,
    fetch_due_students
)


def open_reports():

    win = Toplevel()
    win.title("Student Reports")
    win.geometry("1100x650")
    win.configure(bg="white")

    # ================= Title =================

    Label(
        win,
        text="STUDENT REPORTS",
        font=("Arial", 20, "bold"),
        bg="darkblue",
        fg="white",
        pady=10
    ).pack(fill=X)

    # ================= Buttons =================

    button_frame = Frame(win, bg="white")
    button_frame.pack(fill=X, pady=10)

    # ================= Table =================

    table_frame = Frame(win)
    table_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

    columns = (
        "adm",
        "name",
        "course",
        "year",
        "total",
        "paid",
        "balance"
    )

    report_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    report_table.heading("adm", text="Admission No")
    report_table.heading("name", text="Student Name")
    report_table.heading("course", text="Course")
    report_table.heading("year", text="Year")
    report_table.heading("total", text="Total Fee")
    report_table.heading("paid", text="Paid Fee")
    report_table.heading("balance", text="Balance Fee")

    report_table.column("adm", width=110)
    report_table.column("name", width=220)
    report_table.column("course", width=120)
    report_table.column("year", width=80)
    report_table.column("total", width=110)
    report_table.column("paid", width=110)
    report_table.column("balance", width=110)

    scrollbar = Scrollbar(
        table_frame,
        orient=VERTICAL,
        command=report_table.yview
    )

    report_table.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side=RIGHT, fill=Y)
    report_table.pack(fill=BOTH, expand=True)

    # ================= Functions =================

    def show_rows(rows):

        report_table.delete(*report_table.get_children())

        for row in rows:

            report_table.insert(
                "",
                END,
                values=(
                    row[1],   # Admission No
                    row[2],   # Student Name
                    row[5],   # Course
                    row[6],   # Year
                    row[7],   # Total Fee
                    row[8],   # Paid Fee
                    row[9]    # Balance Fee
                )
            )

    def all_students():
        show_rows(fetch_students())

    def pending_students():
        show_rows(fetch_pending_students())

    def paid_students():
        show_rows(fetch_paid_students())

    def due_students():
        show_rows(fetch_due_students())

    # ================= Buttons =================

    Button(
        button_frame,
        text="All Students",
        width=15,
        bg="blue",
        fg="white",
        command=all_students
    ).pack(side=LEFT, padx=5)

    Button(
        button_frame,
        text="Pending Fee",
        width=15,
        bg="orange",
        fg="white",
        command=pending_students
    ).pack(side=LEFT, padx=5)

    Button(
        button_frame,
        text="Paid Students",
        width=15,
        bg="green",
        fg="white",
        command=paid_students
    ).pack(side=LEFT, padx=5)

    Button(
        button_frame,
        text="Due Students",
        width=15,
        bg="purple",
        fg="white",
        command=due_students
    ).pack(side=LEFT, padx=5)

    Button(
        button_frame,
        text="Refresh",
        width=15,
        command=all_students
    ).pack(side=LEFT, padx=5)

    Button(
        button_frame,
        text="Close",
        width=15,
        bg="red",
        fg="white",
        command=win.destroy
    ).pack(side=RIGHT, padx=5)

    # ================= Default =================

    all_students()
