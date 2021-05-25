from tkinter import *
from tkcalendar import *
from tkinter import messagebox
from datetime import date, datetime
from profile import Login
import pyodbc

def conn():
    # define the servername and
    server = 'DESKTOP-O7VOF2F'
    database = 'Railway'

    # define connection
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};\
                        SERVER=' + server + ';\
                        DATABASE=' + database + ';\
                        Trusted_Connection=yes;')

    conn.autocommit = True

    # create the connection cursor
    cursor = conn.cursor()

    return cursor


#connecting to database
cursor = conn()


class MainApp():
    def __init__(self):
        self.root = Tk()
        self.root.title('Railway')
        self.root.geometry('600x600')
        self.root.resizable(width=False, height=False)
        self.font = ('Roboto', 14)

        self.canvas = Canvas(self.root, height=600, width=600)
        self.canvas.pack()

        self.title = Label(self.canvas, text='Railway', font=('Roboto', 34))
        self.title.place(relwidth=0.7 , relheight=0.2, relx=0.15, rely=0.08)

        self.auth_frame = Frame(self.canvas)
        self.auth_frame.place(relwidth=0.7, relheight=0.4, relx=0.15, rely=0.35)

        self.label = Label(self.auth_frame, text='E-mail', font=self.font)
        self.label.place(height=30, relwidth=0.25, relx=0, y=0)
        self.email_ent = Entry(self.auth_frame, font=self.font)
        self.email_ent.place(height=30, relwidth=0.75, relx=0.25, y=0)

        self.label = Label(self.auth_frame, text='Password', font=self.font)
        self.label.place(height=30, relwidth=0.25, relx=0, y=45)
        self.pass_ent = Entry(self.auth_frame, font=self.font, show='*')
        self.pass_ent.place(height=30, relwidth=0.75, relx=0.25, y=45)

        self.btn_login = Button(self.auth_frame, text='Log in', font=self.font, command=self.login)
        self.btn_login.place(height=30, relwidth=0.75, relx=0.25, y=90)

        self.btn_login = Button(self.auth_frame, text='Register', font=self.font, command=self.register)
        self.btn_login.place(height=30, relwidth=0.75, relx=0.25, y=200)

        self.root.mainloop()


    def register(self):
        self.root.destroy()
        Registration()


    def login(self):
        self.email = self.email_ent.get()
        self.pwd = self.pass_ent.get()

        pwd_query = f"SELECT [user_id], [password] FROM Users WHERE [E-mail]='{self.email}'"
        passwords = cursor.execute(pwd_query)

        pwd = ''
        for password in passwords:
            user_id = password[0]
            pwd = password[1]
        if not pwd:
            messagebox.showinfo("Warning", 'User with this email is not exists')
        elif pwd!=self.pwd:
            messagebox.showinfo("Warning", 'Password is incorrect')
        else:
            self.root.destroy()
            # Login(cursor, user_id)
        
            
class Registration():
    def __init__(self):
        self.root = Tk()
        self.root.title('Railway')
        self.root.geometry('600x600')
        self.root.resizable(width=False, height=False)
        self.font = ('Roboto', 14)

        self.canvas = Canvas(self.root, height=600, width=600)
        self.canvas.pack()

        self.title = Label(self.canvas, text='Registration', font=('Roboto', 34))
        self.title.place(relwidth=0.7 , relheight=0.2, relx=0.15, rely=0.04)

        self.back_btn = Button(self.canvas, text='Back', font=self.font, command=self.back)
        self.back_btn.place(height=30, width=100, x=50, y=70)

        self.reg_frame = Frame(self.canvas)
        self.reg_frame.place(relwidth=0.7, relheight=0.7, relx=0.15, rely=0.25)

        self.label = Label(self.reg_frame, text='Firstname', font=self.font)
        self.label.place(height=30, relwidth=0.25, relx=0, y=0)
        self.fn_ent = Entry(self.reg_frame, font=self.font)
        self.fn_ent.place(height=30, relwidth=0.75, relx=0.25, y=0)

        self.label = Label(self.reg_frame, text='Lastname', font=self.font)
        self.label.place(height=30, relwidth=0.25, relx=0, y=45)
        self.ln_ent = Entry(self.reg_frame, font=self.font)
        self.ln_ent.place(height=30, relwidth=0.75, relx=0.25, y=45)

        self.label = Label(self.reg_frame, text='E-mail', font=self.font)
        self.label.place(height=30, relwidth=0.25, relx=0, y=90)
        self.email_ent = Entry(self.reg_frame, font=self.font)
        self.email_ent.place(height=30, relwidth=0.75, relx=0.25, y=90)

        self.label = Label(self.reg_frame, text='Birthday', font=self.font)
        self.label.place(height=30, relwidth=0.25, relx=0, y=135)
        self.dob_ent = DateEntry(self.reg_frame, font=self.font)
        self.dob_ent.place(height=30, relwidth=0.75, relx=0.25, y=135)

        self.label = Label(self.reg_frame, text='Password', font=self.font)
        self.label.place(height=30, relwidth=0.25, relx=0, y=200)
        self.pwd_ent = Entry(self.reg_frame, font=self.font, show='*')
        self.pwd_ent.place(height=30, relwidth=0.75, relx=0.25, y=200)

        self.label = Label(self.reg_frame, text='Repeat', font=self.font)
        self.label.place(height=30, relwidth=0.25, relx=0, y=245)
        self.pwdr_ent = Entry(self.reg_frame, font=self.font, show='*')
        self.pwdr_ent.place(height=30, relwidth=0.75, relx=0.25, y=245)

        self.btn_login = Button(self.reg_frame, text='Register', font=self.font, command=self.register)
        self.btn_login.place(height=30, relwidth=1, relx=0, y=300)

        self.root.mainloop()

    def register(self):
        self.fn = self.fn_ent.get()
        self.ln = self.ln_ent.get()
        self.email = self.email_ent.get()
        self.dob = self.dob_ent.get_date()
        self.pwd = self.pwd_ent.get()
        self.pwdr = self.pwdr_ent.get()
        age = (date.today()-self.dob).days/365.25
        warning = []
        if self.fn=="":
            warning.append("Firstname is empty")
        if self.ln=="":
            warning.append("Lastname is empty")
        if self.email=="":
            warning.append("Email is empty")
        if self.dob=="":
            warning.append("Birthday is empty")
        if self.pwd=="":
            warning.append("Password is empty")
        if self.pwdr=="":
            warning.append("Repeat is empty")
        if self.pwd!=self.pwdr:
            warning.append("Password was repeated incorrectly")
        if age<16:
            warning.append("You are too young")
            
        query = f"SELECT * FROM Users WHERE [E-mail]='{self.email}'"
        users = cursor.execute(query)

        for _ in users:
            warning.append("This email is already used")

        if warning:
            warn = '\n'.join(map(str, warning))
            messagebox.showinfo(
                "Warning", warn)

        else:
            reg_query = f"INSERT INTO Users VALUES ('{self.fn}', '{self.ln}', '{self.email}', '{self.dob}', '{self.pwd}', 0)"
            # cursor.execute(reg_query)
            messagebox.showinfo(
            "Conratulation", 'You have been registred')
            self.back()

    def back(self):
        self.root.destroy()
        MainApp()


#base settings for window
railway = MainApp()

