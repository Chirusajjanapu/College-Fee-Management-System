from tkinter import *
from tkinter import ttk, messagebox
from header import add_header

from database import (
    insert_student,
    fetch_students,
    search_student,
    update_student,
    delete_student,
    delete_selected_students
)


def open_student():

    win = Toplevel()
    win.title("Student Master")
    win.state("zoomed")
    win.configure(bg="white")

    add_header(win, "STUDENT MASTER")

    # ================= Variables =================

    adm_var = StringVar()
    name_var = StringVar()
    father_var = StringVar()
    mobile_var = StringVar()
    course_var = StringVar()
    year_var = StringVar()

    total_fee_var = StringVar()
    paid_fee_var = StringVar(value="0")
    balance_fee_var = StringVar(value="0")

    # ================= Header =================

    Label(
        win,
        text="STUDENT MASTER",
        bg="#0B5ED7",
        fg="white",
        font=("Arial", 22, "bold"),
        pady=12
    ).pack(fill=X)

    # ================= Main Frame =================

    main_frame = Frame(win, bg="#ecf0f1")
    main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

    # ================= Left Form =================

    left = Frame(
        main_frame,
        bg="white",
        bd=2,
        relief=RIDGE
    )

    left.pack(side=LEFT, fill=Y, padx=(0,10))

    Label(
        left,
        text="Student Details",
        bg="#34495e",
        fg="white",
        font=("Arial",15,"bold"),
        pady=8
    ).pack(fill=X)

    form = Frame(left, bg="white")
    form.pack(padx=15, pady=15)

    # Admission

    Label(form,
          text="Admission No",
          bg="white",
          font=("Arial",11,"bold")
          ).grid(row=0,column=0,sticky="w",pady=8)

    Entry(
        form,
        textvariable=adm_var,
        width=28,
        font=("Arial",11)
    ).grid(row=0,column=1,pady=8)

    # Student Name

    Label(form,
          text="Student Name",
          bg="white",
          font=("Arial",11,"bold")
          ).grid(row=1,column=0,sticky="w",pady=8)

    Entry(
        form,
        textvariable=name_var,
        width=28,
        font=("Arial",11)
    ).grid(row=1,column=1,pady=8)

    # Father Name

    Label(form,
          text="Father Name",
          bg="white",
          font=("Arial",11,"bold")
          ).grid(row=2,column=0,sticky="w",pady=8)

    Entry(
        form,
        textvariable=father_var,
        width=28,
        font=("Arial",11)
    ).grid(row=2,column=1,pady=8)

    # Mobile
    Label(
        form,
        text="Mobile",
        bg="white",
        font=("Arial", 11, "bold")
    ).grid(row=3, column=0, sticky="w", pady=8)


    def validate_mobile(value):
        if value == "":
            return True
        if value.isdigit() and len(value) <= 10:
            return True
        return False


    vcmd = (win.register(validate_mobile), "%P")

    Entry(
        form,
        textvariable=mobile_var,
        font=("Arial", 11),
        width=28,
        validate="key",
        validatecommand=vcmd
    ).grid(row=3, column=1, pady=8)
    
    # Course

    Label(form,
          text="Course",
          bg="white",
          font=("Arial",11,"bold")
          ).grid(row=4,column=0,sticky="w",pady=8)

    course = ttk.Combobox(
        form,
        textvariable=course_var,
        width=26,
        state="readonly"
    )

    course["values"] = (
        "B.Sc",
        "B.Com",
        "B.A",
        "BBA",
        "BCA"
    )

    course.current(0)
    course.grid(row=4,column=1,pady=8)

    # Year

    Label(form,
          text="Year",
          bg="white",
          font=("Arial",11,"bold")
          ).grid(row=5,column=0,sticky="w",pady=8)

    year = ttk.Combobox(
        form,
        textvariable=year_var,
        width=26,
        state="readonly"
    )

    year["values"] = (
        "1st Year",
        "2nd Year",
        "3rd Year"
    )

    year.current(0)
    year.grid(row=5,column=1,pady=8)

    # Total Fee

    Label(form,
          text="Total Fee",
          bg="white",
          font=("Arial",11,"bold")
          ).grid(row=6,column=0,sticky="w",pady=8)

    Entry(
        form,
        textvariable=total_fee_var,
        width=28,
        font=("Arial",11)
    ).grid(row=6,column=1,pady=8)

    # Paid Fee

    Label(form,
          text="Paid Fee",
          bg="white",
          font=("Arial",11,"bold")
          ).grid(row=7,column=0,sticky="w",pady=8)

    Entry(
        form,
        textvariable=paid_fee_var,
        width=28,
        font=("Arial",11)
    ).grid(row=7,column=1,pady=8)

    # Balance Fee

    Label(form,
          text="Balance Fee",
          bg="white",
          font=("Arial",11,"bold")
          ).grid(row=8,column=0,sticky="w",pady=8)

    Entry(
        form,
        textvariable=balance_fee_var,
        width=28,
        state="readonly",
        font=("Arial",11)
    ).grid(row=8,column=1,pady=8)

    # Buttons Frame

    btn_frame = Frame(left, bg="white")
    btn_frame.pack(padx=10, pady=10, fill=X)

    # ================= Functions =================

    def clear():
        adm_var.set("")
        name_var.set("")
        father_var.set("")
        mobile_var.set("")
        course.current(0)
        year.current(0)
        total_fee_var.set("")
        paid_fee_var.set("0")
        balance_fee_var.set("0")


    def calculate_balance():
        try:
            total = int(total_fee_var.get())
            paid = int(paid_fee_var.get())

            balance_fee_var.set(str(total - paid))
        except:
            balance_fee_var.set("0")


    def save_data():

        if adm_var.get() == "" or name_var.get() == "":
            messagebox.showerror(
                "Error",
                "Admission No and Student Name Required",
                parent=win
            )
            return

        try:

            calculate_balance()

            insert_student(
                adm_var.get(),
                name_var.get(),
                father_var.get(),
                mobile_var.get(),
                course_var.get(),
                year_var.get(),
                int(total_fee_var.get()),
                int(paid_fee_var.get()),
                int(balance_fee_var.get())
            )

            messagebox.showinfo(
                "Success",
                "Student Saved Successfully",
                parent=win
            )

            clear()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e),
                parent=win
            )


    def search_data():

        row = search_student(adm_var.get())

        if row:

            adm_var.set(row[1])
            name_var.set(row[2])
            father_var.set(row[3])
            mobile_var.set(row[4])
            course_var.set(row[5])
            year_var.set(row[6])
            total_fee_var.set(row[7])
            paid_fee_var.set(row[8])
            balance_fee_var.set(row[9])

        else:
            messagebox.showerror(
                "Error",
                "Student Not Found",
                parent=win
            )


    def update_data():

        try:

            calculate_balance()

            update_student(
                adm_var.get(),
                name_var.get(),
                father_var.get(),
                mobile_var.get(),
                course_var.get(),
                year_var.get(),
                int(total_fee_var.get()),
                int(paid_fee_var.get()),
                int(balance_fee_var.get())
            )

            fetch_data()

            messagebox.showinfo(
                "Success",
                "Student Updated Successfully",
                parent=win
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e),
                parent=win
            )


    def delete_data():

        if adm_var.get() == "":
            messagebox.showerror(
                "Error",
                "Select Student First",
                parent=win
            )
            return

        if messagebox.askyesno(
            "Delete",
            "Delete this student?",
            parent=win
        ):

            delete_student(adm_var.get())

            messagebox.showinfo(
                "Success",
                "Student Deleted Successfully",
                parent=win
            )

            clear()

    def selected_all_students():
        student_table.selection_set(student_table.get_children())


    def delete_selected_data():

        selected_items = student_table.selection()

        if not selected_items:
            messagebox.showwarning(
                "Warning",
                "Please select at least one student to delete.",
                parent=win
            )
            return

        selected_admissions = []

        for item in selected_items:
            values = student_table.item(item, "values")
            if values and values[0] not in (None, ""):
                admission_no = values[0]
                if admission_no not in selected_admissions:
                    selected_admissions.append(admission_no)

        if not selected_admissions:
            messagebox.showwarning(
                "Warning",
                "No valid student selected.",
                parent=win
            )
            return

        if messagebox.askyesno(
            "Delete Selected Students",
            f"Delete {len(selected_admissions)} selected student(s)?\n\n"
            "This will also delete their related payment records.",
            parent=win
        ):

            deleted_count = delete_selected_students(selected_admissions)

            messagebox.showinfo(
                "Success",
                f"{deleted_count} selected student(s) deleted successfully.",
                parent=win
            )

            clear()
            fetch_data()


    # ================= Buttons =================

    Button(
        btn_frame,
        text="Save",
        width=12,
        bg="green",
        fg="white",
        command=save_data
    ).grid(row=0, column=0, padx=3, pady=3)

    Button(
        btn_frame,
        text="Search",
        width=12,
        bg="#0B5ED7",
        fg="white",
        command=search_data
    ).grid(row=0, column=1, padx=3, pady=3)

    Button(
        btn_frame,
        text="Update",
        width=12,
        bg="orange",
        fg="white",
        command=update_data
    ).grid(row=1, column=0, padx=3, pady=3)

    Button(
        btn_frame,
        text="Delete",
        width=12,
        bg="red",
        fg="white",
        command=delete_data
    ).grid(row=1, column=1, padx=3, pady=3)

    Button(
        btn_frame,
        text="Clear",
        width=12,
        command=clear
    ).grid(row=1, column=2, columnspan=2, padx=3, pady=3)

    # ================= Style =================

    style = ttk.Style()

    style.theme_use("clam")

    style.configure(
        "Treeview",
        rowheight=28,
        font=("Arial",10)
    )

    style.configure(
        "Treeview.Heading",
        font=("Arial",11,"bold")
    )

    # ================= Table =================

    right = Frame(
        main_frame,
        bg="white",
        bd=2,
        relief=RIDGE
    )

    right.pack(side=LEFT, fill=BOTH, expand=True)
    
    Label(
        right,
        text="Student Records",
        bg="#34495e",
        fg="white",
        font=("Arial", 15, "bold"),
        pady=8
    ).pack(fill=X)
       
    table_frame = Frame(right, bg="white")
    table_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
    scroll_y = Scrollbar(table_frame, orient=VERTICAL)
    
    student_table = ttk.Treeview(
        table_frame,
        columns=(
            "adm",
            "name",
            "father",
            "mobile",
            "course",
            "year",
            "total",
            "paid",
            "balance"
        ),
        xscrollcommand=scroll_x.set,
        yscrollcommand=scroll_y.set,
        selectmode="extended"
    )

    scroll_x.pack(side=BOTTOM, fill=X)
    scroll_y.pack(side=RIGHT, fill=Y)
    
    scroll_x.config(command=student_table.xview)
    scroll_y.config(command=student_table.yview)

    student_table.heading("adm", text="Admission No")
    student_table.heading("name", text="Student Name")
    student_table.heading("father", text="Father Name")
    student_table.heading("mobile", text="Mobile")
    student_table.heading("course", text="Course")
    student_table.heading("year", text="Year")
    student_table.heading("total", text="Total Fee")
    student_table.heading("paid", text="Paid Fee")
    student_table.heading("balance", text="Balance Fee")

    student_table["show"] = "headings"

    student_table.column("adm", width=110)
    student_table.column("name", width=180)
    student_table.column("father", width=180)
    student_table.column("mobile", width=120)
    student_table.column("course", width=100)
    student_table.column("year", width=100)
    student_table.column("total", width=100)
    student_table.column("paid", width=100)
    student_table.column("balance", width=100)

    student_table.pack(fill=BOTH, expand=True)

    # ================= Selection Buttons =================

    action_frame = Frame(right, bg="white")
    action_frame.pack(fill=X, padx=10, pady=5)

    Button(
        action_frame,
        text="Select All",
        bg="#6C757D",
        fg="white",
        width=15,
        command=selected_all_students
    ).pack(side=LEFT, padx=5)

    Button(
        action_frame,
        text="Delete Selected Students",
        bg="darkred",
        fg="white",
        width=25,
        command=delete_selected_data
    ).pack(side=LEFT, padx=5)

    Button(
        action_frame,
        text="Clear Selection",
        width=15,
        command=lambda: student_table.selection_remove(
            student_table.selection()
        )
    ).pack(side=LEFT, padx=5)

    # ================= Fetch Data =================

    def fetch_data():

        student_table.delete(*student_table.get_children())

        rows = fetch_students()

        for row in rows:

            student_table.insert(
                "",
                END,
                values=(
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[6],
                    row[7],
                    row[8],
                    row[9]
                )
            )

    # ================= Cursor =================

    def get_cursor(event=""):

        cursor = student_table.focus()

        contents = student_table.item(cursor)

        row = contents["values"]

        if len(row) == 0:
            return

        adm_var.set(row[0])
        name_var.set(row[1])
        father_var.set(row[2])
        mobile_var.set(row[3])
        course_var.set(row[4])
        year_var.set(row[5])
        total_fee_var.set(row[6])
        paid_fee_var.set(row[7])
        balance_fee_var.set(row[8])

    student_table.bind("<ButtonRelease-1>", get_cursor)

    # ================= Auto Refresh =================

    fetch_data()
