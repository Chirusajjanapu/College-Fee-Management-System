from database import (
    get_dashboard_data,
    search_student,
    search_student_by_name,
    fetch_payment_history,
    get_daily_collection,
    get_month_collection,
    fetch_due_students
)
from datetime import datetime
from openai import OpenAI

client = OpenAI()

def ai_chat(command):

    try:

        response = client.responses.create(
            model="gpt-5-mini",
            input=(
                "You are JARVIS, a friendly assistant inside a "
                "College Fee Management System. "
                "Call the operator boss. "
                "Keep replies short, natural and helpful.\n\n"
                f"User: {command}"
            )
        )

        return response.output_text

    except Exception as e:

        error_text = str(e).lower()

        if "credit_balance_exhausted" in error_text:
            return (
                "Sorry boss, AI chat credits are currently unavailable. "
                "College database commands are still working."
            )

        if "rate limit" in error_text or "429" in error_text:
            return (
                "Sorry boss, AI service is temporarily unavailable. "
                "Please try again later."
            )

        if "connection" in error_text:
            return (
                "Sorry boss, I can't connect to the AI service right now."
            )

        return (
            "Sorry boss, I couldn't process that AI request."
        )

# ================= STUDENT DETAILS =================

def student_details(admission_no):

    student = search_student(admission_no)

    if not student:
        return f"Sorry boss, student {admission_no} not found."

    return (
        f"Student: {student[2]}\n"
        f"Admission No: {student[1]}\n"
        f"Father: {student[3]}\n"
        f"Mobile: {student[4]}\n"
        f"Course: {student[5]}\n"
        f"Year: {student[6]}\n"
        f"Total Fee: ₹{student[7]}\n"
        f"Paid Fee: ₹{student[8]}\n"
        f"Balance: ₹{student[9]}"
    )


# ================= NAME SEARCH =================

def name_search(name):

    students = search_student_by_name(name)

    if not students:
        return f"Sorry boss, student {name} not found."

    if len(students) > 1:

        result = f"I found {len(students)} students:\n\n"

        for student in students:

            result += (
                f"Admission No: {student[1]}\n"
                f"Student Name: {student[2]}\n"
                f"Course: {student[5]}\n"
                f"Balance: ₹{student[9]}\n\n"
            )

        return result

    return student_details(students[0][1])

def find_student_by_name(name):

    students = search_student_by_name(name)

    if not students:
        return None

    return students[0]

# ================= PAYMENT HISTORY =================

def payment_history(admission_no):

    student = search_student(admission_no)

    if not student:
        return f"Sorry boss, student {admission_no} not found."

    rows = fetch_payment_history(admission_no)

    if not rows:
        return (
            f"No payment history found for "
            f"{student[2]}."
        )

    result = (
        f"Payment History: {student[2]}\n"
        f"Admission No: {admission_no}\n\n"
    )

    total = 0

    for date, amount in rows:

        result += f"Date: {date}  |  Amount: ₹{amount}\n"

        total += amount

    result += f"\nTotal Payments: ₹{total}"

    return result

def today_collection():

    date = datetime.now().strftime("%d-%m-%Y")

    rows = get_daily_collection(date)

    if not rows:
        return (
            f"Today's Collection: ₹0\n"
            f"Payments: 0"
        )

    total = sum(row[2] for row in rows)

    result = (
        f"Today's Collection: ₹{total}\n"
        f"Payments: {len(rows)}\n\n"
    )

    for admission_no, student_name, amount in rows:
        result += (
            f"{admission_no} | "
            f"{student_name} | "
            f"₹{amount}\n"
        )

    return result

def monthly_collection():

    month = datetime.now().strftime("%m-%Y")

    rows = get_month_collection(month)

    if not rows:
        return (
            f"This Month Collection: ₹0\n"
            f"Payments: 0"
        )

    total = sum(row[2] for row in rows)

    result = (
        f"This Month Collection: ₹{total}\n"
        f"Payments: {len(rows)}\n\n"
    )

    for admission_no, student_name, amount in rows:
        result += (
            f"{admission_no} | "
            f"{student_name} | "
            f"₹{amount}\n"
        )

    return result

# ================= PAYMENT HISTORY BY NAME =================

def payment_history_by_name(name):

    students = search_student_by_name(name)

    if not students:
        return f"Sorry boss, student {name} not found."

    if len(students) > 1:

        result = (
            f"I found {len(students)} students with the name {name}:\n\n"
        )

        for student in students:
            result += (
                f"Admission No: {student[1]}\n"
                f"Student Name: {student[2]}\n"
                f"Course: {student[5]}\n\n"
            )

        return result

    student = students[0]

    return payment_history(student[1])

# ================= PENDING STUDENTS =================

def students_with_balance():

    students = fetch_due_students()

    if not students:
        return "Good news boss! No students have pending balance."

    result = (
        f"Students with Balance: {len(students)}\n\n"
    )

    total_balance = 0

    for student in students:
        result += (
            f"{student[1]} | "
            f"{student[2]} | "
            f"Balance: ₹{student[9]}\n"
        )

        total_balance += student[9]

    result += (
        f"\nTotal Pending Amount: ₹{total_balance}"
    )

    return result

def normal_chat(command):

    if command in ["hello", "hi", "hey", "hello jarvis"]:
        return "Hello boss, how can I help you?"

    elif command in ["how are you", "how are you jarvis"]:
        return "I'm doing great boss. I'm ready to help you."

    elif command in ["good morning"]:
        return "Good morning boss! Have a great day."

    elif command in ["good afternoon"]:
        return "Good afternoon boss!"

    elif command in ["good evening"]:
        return "Good evening boss!"

    elif command in ["thank you", "thanks", "thank you jarvis"]:
        return "You're welcome boss."

    elif command in ["what can you do", "what can you do jarvis"]:
        return (
            "I can help you with student details, fee information, "
            "payment history, daily collection, monthly collection "
            "and college reports."
        )

    elif command in ["who are you", "who are you jarvis"]:
        return "I'm Jarvis, your college fee management assistant."

    elif command in ["bye", "goodbye", "bye jarvis"]:
        return "Goodbye boss. I'll be ready when you need me."

    return None

def ask_jarvis(command):

    command = command.lower().strip()

    # ================= GREETING =================

    if command in ["hello", "hi", "hey"]:
        return "Hello, how can I help you boss?"

    elif command in [
        "who has balance",
        "who has pending balance",
        "students with balance",
        "who has fee balance",
        "which students have balance"
    ]:
        return students_with_balance()

    # ================= TODAY COLLECTION =================

    elif command in [
        "today collection",
        "today's collection",
        "how much collected today"
    ]:
        return today_collection()

    # ================= MONTHLY COLLECTION =================

    elif command in [
        "this month collection",
        "monthly collection",
        "how much collected this month"
    ]:
        return monthly_collection()

    # ================= PAYMENT HISTORY BY NAME =================

    elif "payment history" in command and not command.startswith("payment history "):

        clean = command.replace("?", "").strip()

        for phrase in [
            "what is ",
            "show me ",
            "show ",
            "tell me ",
            "please show ",
            "please tell me ",
            "payment history of ",
            "payment history"
        ]:
            clean = clean.replace(phrase, " ")

        name = " ".join(clean.split()).strip()

        if name:
            return payment_history_by_name(name)

        return "Please provide a student name boss."

    # ================= PAYMENT HISTORY BY ADMISSION =================

    elif command.startswith("payment history "):

        admission_no = command.replace(
            "payment history ", "", 1
        ).strip()

        if admission_no.isdigit():
            return payment_history(admission_no)

        return "Please provide a valid admission number boss."

    # ================= STUDENT NAME SEARCH =================

    elif command.startswith("student name "):

        name = command.replace(
            "student name ", "", 1
        ).strip()

        if name:
            return name_search(name)

        return "Please enter a student name boss."

    # ================= FIND STUDENT =================

    elif command.startswith("find student "):

        name = command.replace(
            "find student ", "", 1
        ).strip()

        if name:
            return name_search(name)

        return "Please enter a student name boss."

    # ================= NATURAL BALANCE =================

    elif "balance" in command:

        clean = command.replace("?", "").strip()

        for phrase in [
            "what is ",
            "what's ",
            "tell me ",
            "please tell me ",
            "please ",
            "the ",
            "balance of ",
            "balance"
        ]:
            clean = clean.replace(phrase, " ")

        name = " ".join(clean.split()).strip()

        student = find_student_by_name(name)

        if student:
            return (
                f"{student[2]}'s Balance Fee = "
                f"₹{student[9]}"
            )

        return f"Sorry boss, student {name} not found."

    # ================= NATURAL TOTAL FEE =================

    elif "total fee" in command:

        clean = command.replace("?", "").strip()

        for phrase in [
            "what is ",
            "what's ",
            "tell me ",
            "please tell me ",
            "please ",
            "the ",
            "total fee of ",
            "total fee"
        ]:
            clean = clean.replace(phrase, " ")

        name = " ".join(clean.split()).strip()

        student = find_student_by_name(name)

        if student:
            return (
                f"{student[2]}'s Total Fee = "
                f"₹{student[7]}"
            )

        return f"Sorry boss, student {name} not found."

    # ================= NATURAL PAID FEE =================

    elif "paid fee" in command:

        clean = command.replace("?", "").strip()

        for phrase in [
            "what is ",
            "what's ",
            "tell me ",
            "please tell me ",
            "please ",
            "the ",
            "paid fee of ",
            "paid fee"
        ]:
            clean = clean.replace(phrase, " ")

        name = " ".join(clean.split()).strip()

        student = find_student_by_name(name)

        if student:
            return (
                f"{student[2]}'s Paid Fee = "
                f"₹{student[8]}"
            )

        return f"Sorry boss, student {name} not found."

    # ================= PENDING BALANCE =================

    elif command in [
        "who has balance",
        "who has pending balance",
        "students with balance",
        "who has fee balance"
    ]:

        return students_with_balance()

    elif command in [
        "how many students have balance",
        "how many students have pending fee",
        "pending students count"
    ]:

        students = fetch_due_students()

        return (
            f"Boss, {len(students)} students "
            f"have pending balance."
        )

    # ================= DASHBOARD =================

    elif command == "total students":

        total_students, total_fee, paid_fee, balance_fee = (
            get_dashboard_data()
        )

        return f"Total Students = {total_students}"

    elif command == "total fee":

        total_students, total_fee, paid_fee, balance_fee = (
            get_dashboard_data()
        )

        return f"Total Fee = ₹{total_fee}"

    elif command == "paid fee":

        total_students, total_fee, paid_fee, balance_fee = (
            get_dashboard_data()
        )

        return f"Paid Fee = ₹{paid_fee}"

    elif command == "balance fee":

        total_students, total_fee, paid_fee, balance_fee = (
            get_dashboard_data()
        )

        return f"Balance Fee = ₹{balance_fee}"

    # ================= STUDENT + NUMBER =================

    elif command.startswith("student "):

        admission_no = command.replace(
            "student ", "", 1
        ).strip()

        if admission_no.isdigit():
            return student_details(admission_no)

        return "Please enter a valid admission number boss."

    # ================= ADMISSION NUMBER =================

    elif command.startswith("admission no "):

        admission_no = command.replace(
            "admission no ", "", 1
        ).strip()

        if admission_no.isdigit():
            return student_details(admission_no)

        return "Please enter a valid admission number boss."

    elif command.startswith("admission number "):

        admission_no = command.replace(
            "admission number ", "", 1
        ).strip()

        if admission_no.isdigit():
            return student_details(admission_no)

        return "Please enter a valid admission number boss."

    # ================= DIRECT NUMBER =================

    elif command.isdigit():

        return student_details(command)

    # ================= UNKNOWN =================

    else:

        response = normal_chat(command)

        if response:
            return response

        return ai_chat(command)
