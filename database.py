import sys
import sqlite3
import os

# -------------------------------
# Database Path
# -------------------------------
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
DB_PATH = os.path.join(BASE_DIR, "college.db")


# -------------------------------
# Database Connection
# -------------------------------
def connect_db():

    con = sqlite3.connect(
        DB_PATH,
        timeout=30
    )

    con.execute("PRAGMA busy_timeout = 30000")

    return con

# -------------------------------
# Create Database & Tables
# -------------------------------
def create_database():
    con = connect_db()
    cur = con.cursor()

    # Users Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # Students Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admission_no TEXT UNIQUE,
        student_name TEXT,
        father_name TEXT,
        mobile TEXT,
        course TEXT,
        year TEXT,
        total_fee INTEGER,
        paid_fee INTEGER,
        balance_fee INTEGER
    )
    """)

    # Payments Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS payments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admission_no TEXT,
        student_name TEXT,
        paid_amount INTEGER,
        payment_date TEXT
    )
    """)

    # Default Admin
    cur.execute("SELECT * FROM users WHERE username=?", ("admin",))
    if cur.fetchone() is None:
        cur.execute(
            "INSERT INTO users(username,password) VALUES(?,?)",
            ("admin", "admin123")
        )

    con.commit()
    con.close()


# -------------------------------
# Login Check
# -------------------------------
def verify_login(username, password):
    con = connect_db()
    cur = con.cursor()

    cur.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    data = cur.fetchone()
    con.close()

    return data


# -------------------------------
# Change Password
# -------------------------------
def change_password(username, new_password):
    con = connect_db()
    cur = con.cursor()

    cur.execute(
        "UPDATE users SET password=? WHERE username=?",
        (new_password, username)
    )

    con.commit()
    con.close()


# -------------------------------
# Forgot Password
# -------------------------------
def get_password(username):
    con = connect_db()
    cur = con.cursor()

    cur.execute(
        "SELECT password FROM users WHERE username=?",
        (username,)
    )

    data = cur.fetchone()
    con.close()

    return data[0] if data else None


# -------------------------------
# Insert Student
# -------------------------------
def insert_student(adm, name, father, mobile,
                   course, year,
                   total_fee, paid_fee, balance_fee):

    con = connect_db()
    cur = con.cursor()

    cur.execute("""
    INSERT INTO students(
        admission_no,
        student_name,
        father_name,
        mobile,
        course,
        year,
        total_fee,
        paid_fee,
        balance_fee
    )
    VALUES(?,?,?,?,?,?,?,?,?)
    """, (
        adm,
        name,
        father,
        mobile,
        course,
        year,
        total_fee,
        paid_fee,
        balance_fee
    ))

    con.commit()
    con.close()


# -------------------------------
# Fetch Students
# -------------------------------
def fetch_students():
    
    con = connect_db()
    cur = con.cursor()

    cur.execute("SELECT * FROM students")

    data = cur.fetchall()
    
    con.close()

    return data


# -------------------------------
# Search Student
# -------------------------------
def search_student(adm):

    con = connect_db()
    cur = con.cursor()

    cur.execute(
        "SELECT * FROM students WHERE admission_no=?",
        (adm,)
    )

    row = cur.fetchone()

    con.close()

    return row

def search_student_by_name(name):

    con = connect_db()
    cur = con.cursor()

    cur.execute("""
        SELECT *
        FROM students
        WHERE LOWER(student_name) LIKE ?
    """, (f"%{name.lower()}%",))

    rows = cur.fetchall()

    con.close()

    return rows
    
# -------------------------------
# Update Student
# -------------------------------
def update_student(adm, name, father, mobile,
                   course, year,
                   total_fee, paid_fee, balance_fee):

    con = connect_db()
    cur = con.cursor()

    cur.execute("""
    UPDATE students
    SET student_name=?,
        father_name=?,
        mobile=?,
        course=?,
        year=?,
        total_fee=?,
        paid_fee=?,
        balance_fee=?
    WHERE admission_no=?
    """, (
        name,
        father,
        mobile,
        course,
        year,
        total_fee,
        paid_fee,
        balance_fee,
        adm
    ))

    con.commit()
    con.close()


# -------------------------------
# Delete Student
# -------------------------------
def delete_student(adm):
    
    con = connect_db()
    cur = con.cursor()

    cur.execute(
        "DELETE FROM students WHERE admission_no=?",
        (adm,)
    )

    con.commit()
    con.close()


# -------------------------------
# Delete Selected Students
# -------------------------------
def delete_selected_students(admission_nos):

    if isinstance(admission_nos, (str, int)):
        admission_nos = [admission_nos]

    if not admission_nos:
        return 0

    unique_admissions = []
    for adm in admission_nos:
        if adm not in (None, "") and adm not in unique_admissions:
            unique_admissions.append(adm)

    if not unique_admissions:
        return 0

    con = connect_db()
    cur = con.cursor()

    try:
        placeholders = ", ".join("?" for _ in unique_admissions)

        cur.execute(
            f"DELETE FROM payments WHERE admission_no IN ({placeholders})",
            tuple(unique_admissions)
        )

        cur.execute(
            f"DELETE FROM students WHERE admission_no IN ({placeholders})",
            tuple(unique_admissions)
        )

        con.commit()
        return len(unique_admissions)

    finally:
        con.close()


# -------------------------------
# Fetch Pending Students
# -------------------------------
def fetch_pending_students():

    con = connect_db()
    cur = con.cursor()

    cur.execute("SELECT * FROM students WHERE balance_fee > 0")

    rows = cur.fetchall()

    con.close()

    return rows


# -------------------------------
# Fetch Fully Paid Students
# -------------------------------
def fetch_paid_students():

    con = connect_db()
    cur = con.cursor()

    cur.execute("SELECT * FROM students WHERE balance_fee = 0")

    rows = cur.fetchall()

    con.close()

    return rows


# -------------------------------
# Update Fee
# -------------------------------
def update_fee(adm, amount):

    con = connect_db()
    cur = con.cursor()

    cur.execute("""
    SELECT paid_fee, balance_fee
    FROM students
    WHERE admission_no=?
    """, (adm,))

    row = cur.fetchone()

    if row:
        new_paid = row[0] + amount
        new_balance = row[1] - amount

        cur.execute("""
        UPDATE students
        SET paid_fee=?,
            balance_fee=?
        WHERE admission_no=?
        """, (
            new_paid,
            new_balance,
            adm
        ))

    con.commit()
    con.close()


# -------------------------------
# Save Payment
# -------------------------------
def save_payment(adm, name, amount, pay_date):

    con = connect_db()
    cur = con.cursor()

    cur.execute("""
    INSERT INTO payments(
        admission_no,
        student_name,
        paid_amount,
        payment_date
    )
    VALUES(?,?,?,?)
    """, (
        adm,
        name,
        amount,
        pay_date
    ))

    con.commit()
    con.close()


# -------------------------------
# Fetch Payments
# -------------------------------
def fetch_payments(adm):

    con = connect_db()
    cur = con.cursor()

    cur.execute("""
    SELECT payment_date, paid_amount
    FROM payments
    WHERE admission_no=?
    ORDER BY id DESC
    """, (adm,))

    rows = cur.fetchall()
    con.close()

    return rows


# -------------------------------
# Create Database Automatically
# -------------------------------
def get_dashboard_data():

    con = connect_db()
    cur = con.cursor()

    cur.execute("SELECT COUNT(*) FROM students")
    total_students = cur.fetchone()[0]

    cur.execute("""
        SELECT
            SUM(total_fee),
            SUM(paid_fee),
            SUM(balance_fee)
        FROM students
    """)

    data = cur.fetchone()

    total_fee = data[0] if data[0] else 0
    paid_fee = data[1] if data[1] else 0
    balance_fee = data[2] if data[2] else 0

    con.close()

    return total_students, total_fee, paid_fee, balance_fee

# -------------------------------
# Fetch Due Students
# -------------------------------
def fetch_due_students():

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM students WHERE balance_fee > 0 ORDER BY balance_fee DESC")

    rows = cur.fetchall()
    
    conn.close()

    return rows

# -------------------------------
# Daily Collection
# -------------------------------
def get_daily_collection(date):

    con = connect_db()
    cur = con.cursor()

    cur.execute("""
        SELECT
            admission_no,
            student_name,
            paid_amount
        FROM payments
        WHERE payment_date=?
    """, (date,))

    rows = cur.fetchall()

    con.close()

    return rows

    Label(
        win,
        text="DAILY COLLECTION",
        font=("Arial",18,"bold"),
        bg="darkblue",
        fg="white",
        pady=10
    ).pack(fill=X)

    top = Frame(win, bg="white")
    top.pack(fill=X, pady=10)

    Label(
        top,
        text="Enter Date (dd-mm-yyyy)",
        bg="white",
        font=("Arial",11)
    ).pack(side=LEFT, padx=10)

    date_var = StringVar()

    Entry(
        top,
        textvariable=date_var,
        width=20
    ).pack(side=LEFT)

    Button(
        top,
        text="Search",
        bg="blue",
        fg="white",
        command=daily_collection
    ).pack(side=LEFT, padx=10)

    from tkinter import ttk

    table = ttk.Treeview(
        win,
        columns=("adm","name","amount"),
        show="headings"
    )

    table.heading("adm", text="Admission No")
    table.heading("name", text="Student Name")
    table.heading("amount", text="Paid Amount")

    table.column("adm", width=120)
    table.column("name", width=250)
    table.column("amount", width=150)

    table.pack(fill=BOTH, expand=True, padx=10, pady=10)

    total_var = StringVar()
    total_var.set("₹ 0")

    Label(
        win,
        text="Total Collection",
        font=("Arial", 13, "bold"),
        bg="white"
    ).pack()

    Label(
        win,
        textvariable=total_var,
        font=("Arial", 16, "bold"),
        fg="green",
        bg="white"
    ).pack(pady=10)

# ================= Daily History =================
def get_daily_history():

    con = connect_db()
    cur = con.cursor()

    cur.execute("""
        SELECT
            payment_date,
            COUNT(*),
            SUM(paid_amount)
        FROM payments
        GROUP BY payment_date
        ORDER BY
            substr(payment_date,7,4) DESC,
            substr(payment_date,4,2) DESC,
            substr(payment_date,1,2) DESC
    """)

    rows = cur.fetchall()

    con.close()

    return rows

def fetch_payment_history(admission_no):

    con = connect_db()
    cur = con.cursor()

    cur.execute("""
        SELECT payment_date, paid_amount
        FROM payments
        WHERE admission_no=?
        ORDER BY id DESC
    """, (admission_no,))

    rows = cur.fetchall()

    con.close()

    return rows


def get_month_collection(month):

    con = connect_db()
    cur = con.cursor()

    cur.execute("""
        SELECT
            admission_no,
            student_name,
            paid_amount
        FROM payments
        WHERE strftime('%m-%Y',
            substr(payment_date,7,4)||'-'||
            substr(payment_date,4,2)||'-'||
            substr(payment_date,1,2)
        ) = ?
    """, (month,))

    rows = cur.fetchall()

    con.close()

    return rows

def fetch_all_students():

    con = connect_db()
    cur = con.cursor()

    cur.execute("""
        SELECT
            admission_no,
            student_name,
            father_name,
            mobile,
            course,
            year,
            total_fee,
            paid_fee,
            balance_fee
        FROM students
        ORDER BY admission_no
    """)

    rows = cur.fetchall()

    con.close()

    return rows

def fetch_all_payments():

    con = connect_db()
    cur = con.cursor()

    cur.execute("""
        SELECT
            payment_date,
            admission_no,
            student_name,
            paid_amount
        FROM payments
        ORDER BY payment_date DESC
    """)

    rows = cur.fetchall()

    con.close()

    return rows

def get_month_summary():

    con = connect_db()
    cur = con.cursor()

    cur.execute("""
        SELECT
            substr(payment_date,4,7) AS month,
            SUM(paid_amount)
        FROM payments
        GROUP BY substr(payment_date,4,7)
        ORDER BY substr(payment_date,7,4),
                 substr(payment_date,4,2)
    """)

    rows = cur.fetchall()

    con.close()

    return rows

def clear_all_student_data():

    con = connect_db()
    cur = con.cursor()

    # Payments first
    cur.execute("DELETE FROM payments")

    # Students next
    cur.execute("DELETE FROM students")

    con.commit()
    con.close()

def add_student_import(
    admission_no,
    student_name,
    father_name,
    mobile,
    course,
    year,
    total_fee,
    paid_fee,
    balance_fee
):

    con = connect_db()
    cur = con.cursor()

    cur.execute("""
        INSERT OR REPLACE INTO students
        (
            admission_no,
            student_name,
            father_name,
            mobile,
            course,
            year,
            total_fee,
            paid_fee,
            balance_fee
        )
        VALUES (?,?,?,?,?,?,?,?,?)
    """, (
        admission_no,
        student_name,
        father_name,
        mobile,
        course,
        year,
        total_fee,
        paid_fee,
        balance_fee
    ))

    con.commit()
    con.close()
