from tkinter import *
from tkinter import messagebox, simpledialog
from database import verify_login, change_password, get_password

# ---------------- Login Function ----------------
def login():

    username = txt_user.get()
    password = txt_pass.get()

    if verify_login(username, password):
        root.destroy()
        import main
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")


# ---------------- Forgot Password ----------------
def forgot_password():

    username = simpledialog.askstring(
        "Forgot Password",
        "Enter Username"
    )

    if username is None:
        return

    password = get_password(username)

    if password:
        messagebox.showinfo(
            "Password",
            f"Password : {password}"
        )
    else:
        messagebox.showerror(
            "Error",
            "Username Not Found"
        )


# ---------------- Change Password ----------------
def change_pass():

    username = txt_user.get()

    if username == "":
        messagebox.showwarning(
            "Warning",
            "Enter Username First"
        )
        return

    old = simpledialog.askstring(
        "Change Password",
        "Enter Old Password",
        show="*"
    )

    if old is None:
        return

    if not verify_login(username, old):
        messagebox.showerror(
            "Error",
            "Old Password Incorrect"
        )
        return

    new = simpledialog.askstring(
        "Change Password",
        "Enter New Password",
        show="*"
    )

    if new is None:
        return

    confirm = simpledialog.askstring(
        "Change Password",
        "Confirm New Password",
        show="*"
    )

    if confirm is None:
        return

    if new != confirm:
        messagebox.showerror(
            "Error",
            "Passwords Do Not Match"
        )
        return

    change_password(username, new)

    messagebox.showinfo(
        "Success",
        "Password Changed Successfully"
    )


# ---------------- Window ----------------

root = Tk()

root.title("College Fee Management System - Login")
root.geometry("500x380")
root.resizable(False, False)
root.configure(bg="white")

title = Label(
    root,
    text="COLLEGE FEE MANAGEMENT SYSTEM",
    font=("Arial",18,"bold"),
    bg="darkblue",
    fg="white",
    pady=10
)

title.pack(fill=X)

frame = Frame(root, bg="white")
frame.pack(pady=40)

Label(
    frame,
    text="Username",
    bg="white",
    font=("Arial",12)
).grid(row=0,column=0,padx=10,pady=10)

txt_user = Entry(
    frame,
    font=("Arial",12),
    width=25
)

txt_user.grid(row=0,column=1)

Label(
    frame,
    text="Password",
    bg="white",
    font=("Arial",12)
).grid(row=1,column=0,padx=10,pady=10)

txt_pass = Entry(
    frame,
    font=("Arial",12),
    width=25,
    show="*"
)

txt_pass.grid(row=1,column=1)

Button(
    root,
    text="LOGIN",
    font=("Arial",12,"bold"),
    bg="green",
    fg="white",
    width=18,
    command=login
).pack(pady=10)

Button(
    root,
    text="Forgot Password",
    fg="blue",
    bd=0,
    cursor="hand2",
    command=forgot_password
).pack()

Button(
    root,
    text="Change Password",
    fg="blue",
    bd=0,
    cursor="hand2",
    command=change_pass
).pack(pady=5)

root.mainloop()
