import os
import tkinter as tk
from tkinter import messagebox
import db
from Backend import CheckPassword as cp


class Login(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.master.iconbitmap('images/icon.ico')
        self.master.title("PassLock")
        self.master.geometry("500x500")
        self.master.resizable(0, 0)
        # ---------------------------StringVar
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        # ---------------------------frame1
        self.frame1 = tk.Frame(
            self.master, bg="pale turquoise", relief="ridge")
        self.frame1.pack(side="top", expand='true', fill='both', anchor='c')
        # ---------------------------title label
        self.title_label = tk.Label(self.frame1, text="Login", font="Impact 30 bold",
                                    bg="pale turquoise")
        self.title_label.grid(
            row=1, column=0, columnspan=2, sticky='n', pady=40)
        # ---------------------------image
        # Add image file
        self.img = tk.PhotoImage(file="images/logo.png")
        # ---------------------------canvas
        self.canvas = tk.Canvas(self.frame1, height=110, bg="white", width=500)
        self.canvas.grid(row=0, column=0, columnspan=2)
        self.canvas.create_image(250, 60, image=self.img)
        # ---------------------------Program UI
        self.username_label = tk.Label(self.frame1, text="                                    Username:",
                                       font="Arial 10 bold", bg="pale turquoise")
        self.username_entry = tk.Entry(
            self.frame1, width=25, textvariable=self.username)
        self.password_label = tk.Label(self.frame1, text="                                "
                                                         "     Password:", font="Arial 10 bold",
                                       bg="pale turquoise")
        self.password_entry = tk.Entry(
            self.frame1, width=25, show="*", textvariable=self.password)
        # Grid on the screen
        self.username_label.grid(
            row=2, column=0, columnspan=2, sticky='w', pady=10)
        self.username_entry.grid(
            row=2, column=1, columnspan=2, sticky='e', pady=10, padx=130)
        self.password_label.grid(
            row=3, column=0, columnspan=2, sticky='w', pady=10)
        self.password_entry.grid(
            row=3, column=1, columnspan=2, sticky='e', pady=10, padx=130)

        # Enter btn
        self.btn_reset_pass = tk.Button(self.frame1, text="Forgot your password?", font="Arial 10",
                                        bg='pale turquoise',
                                        command=self.change_reset, activebackground='pale turquoise', activeforeground="blue2",
                                        border="0")
        self.btn_reset_pass.grid(row=4, column=0, columnspan=2, pady=7)

        self.btn_signup_pass = tk.Button(self.frame1, text="Signup", font="Arial 10",
                                        bg='pale turquoise',
                                        command=self.change_signup, activebackground='pale turquoise', activeforeground="blue2",
                                        border="0")
        self.btn_signup_pass.grid(row=6, column=0, columnspan=2, pady=7)

        self.btn_enter = tk.Button(self.frame1, text="Enter", font="Arial 10 bold", width=7,
                                   bg="#0001a7", fg='white', command=self.change_app,
                                   activeforeground='white', activebackground='#00dee1')
        self.btn_enter.grid(row=5, column=0, columnspan=2, pady=14)

        # -------------------------------Events
        self.master.bind('<Return>', self.change_app)

    def change_app(self, *_):
        # store the new password in Database
        username = self.username.get()
        currPassword = self.password.get()
        # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        val, whiceError = cp.password_check(currPassword)
        if val:
            checkPassword = db.Fetchall("account")
            print(checkPassword)
            for i in range(len(checkPassword)):
                if username== checkPassword[i][0] and currPassword == checkPassword[i][1]:
                    self.master.destroy()
                    os.system(f'python Application.py {username} {currPassword}')

            messagebox.showerror("PassLock", "Invalid Username or Password")
            
        else:
            if whiceError == 1:
                messagebox.showerror("PassLock", "length should be at least 8")
            elif whiceError == 2:
                messagebox.showerror(
                    "PassLock", "length should be not be greater than 100")
            elif whiceError == 3:
                messagebox.showerror(
                    "PassLock", "Password should have at least one numeral")
            elif whiceError == 4:
                messagebox.showerror(
                    "PassLock", "Password should have at least one uppercase letter")
            elif whiceError == 5:
                messagebox.showerror(
                    "PassLock", "Password should have at least one lowercase letter")
            elif whiceError == 6:
                messagebox.showerror(
                    "PassLock", "Password should have at least one of the symbols $@#")

    def change_reset(self):
        self.master.destroy()
        os.system('python ResetPassword.py')
    def change_signup(self):
        self.master.destroy()
        os.system('python Signup.py')


if __name__ == "__main__":
    form = tk.Tk()
    app = Login(form)
    # Adjust size
    form.mainloop()
