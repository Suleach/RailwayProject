from tkinter import *
from tkinter import ttk
from tkinter import messagebox
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

class Login():
    def __init__(self, cursor, user_id):
        self.root = Tk()
        self.root.title('Railway')
        self.root.geometry('600x600')
        self.root.resizable(width=False, height=False)
        self.font = ('Roboto', 14)

        self.Canvas = Canvas(self.root, height=600, width=600)
        self.Canvas.place(x=40, y=0)

        self.cursor = cursor
        self.user_id = user_id

        query = f"SELECT * FROM Users WHERE [user_id]={user_id}"
        profiles = self.cursor.execute(query)
        for profile in profiles:
            self.firstname = profile[1]
            self.lastname = profile[2]
            self.email = profile[3]
            self.dob = profile[4]
            self.password = profile[5]
            self.is_admin = profile[6]
        # print(self.firstname, self.lastname, self.email, self.is_admin)
        if self.is_admin:
            self.admin()
        # else:
        #     self.user()

        self.root.mainloop()
    
    def admin(self):
        hello = f"Hello {self.firstname}, {self.lastname}"
        self.title = Label(self.Canvas, text=hello, font=('Roboto', 20))
        self.title.place(relx=0, rely=0.07)

        self.frame = Frame(self.Canvas, bg='red')
        self.frame.place(height=600, width=380, x=140, y=100)

        self.btn_add = Button(self.Canvas, text='Add', font=self.font)
        self.btn_add.place(height=30,  width=120, x=400, y=50)

        self.schedule_btn = Button(self.Canvas, text='Train', font=self.font, command=self.trains)
        self.schedule_btn.place(height=30,  width=120, x=0, y=100)

        self.schedule_btn = Button(self.Canvas, text='Stations', font=self.font, command=self.stations)
        self.schedule_btn.place(height=30,  width=120, x=0, y=140)

        self.schedule_btn = Button(self.Canvas, text='Tracks', font=self.font)
        self.schedule_btn.place(height=30,  width=120, x=0, y=180)

        self.schedule_btn = Button(self.Canvas, text='Users', font=self.font)
        self.schedule_btn.place(height=30,  width=120, x=0, y=220)

        self.schedule_btn = Button(self.Canvas, text='Orders', font=self.font)
        self.schedule_btn.place(height=30,  width=120, x=0, y=260)

        self.schedule_btn = Button(self.Canvas, text='Schedule', font=self.font)
        self.schedule_btn.place(height=30,  width=120, x=0, y=300)

        self.schedule_btn = Button(self.Canvas, text='Seats', font=self.font)
        self.schedule_btn.place(height=30,  width=120, x=0, y=340)

        self.schedule_btn = Button(self.Canvas, text='Passengers', font=self.font)
        self.schedule_btn.place(height=30,  width=120, x=0, y=380)

        self.schedule_btn = Button(self.Canvas, text='Delays', font=self.font)
        self.schedule_btn.place(height=30,  width=120, x=0, y=420)
        
        
    def trains(self):
        self.frame.destroy()
        self.btn_add.destroy()

        self.btn_add = Button(self.Canvas, text='Add', font=self.font, command=self.add_train_frame)
        self.btn_add.place(height=30,  width=120, x=400, y=50)

        self.frame = Frame(self.Canvas)
        self.frame.place(height=600, width=380, x=140, y=100)

        query = f"SELECT * FROM Trains"
        trains = self.cursor.execute(query)

        i=0
        self.label_id = Label(self.frame, text='ID', font=('Roboto', 14, 'bold'))
        self.label_id.grid(row=i, column=0)

        self.label_name = Label(self.frame, text='Train name', font=('Roboto', 14, 'bold'))
        self.label_name.grid(row=i, column=1)
        for train in trains:
            i+=1
            train_id = train[0]
            train_name = train[1]

            self.label_id = Label(self.frame, text=train_id, font=self.font)
            self.label_id.grid(row=i, column=0)

            self.label_name = Label(self.frame, text=train_name, font=self.font)
            self.label_name.grid(row=i, column=1)


    def add_train_frame(self):
        self.frame.destroy()
        self.btn_add.destroy()

        self.btn_add = Button(self.Canvas, text='Add', font=self.font, command=self.add_train)
        self.btn_add.place(height=30,  width=120, x=400, y=50)

        self.frame = Frame(self.Canvas)
        self.frame.place(height=600, width=380, x=140, y=100)
        self.label = Label(self.frame, text='Name', font=self.font)
        self.label.grid(row=0, column=0)
        self.name_ent = Entry(self.frame, font=self.font)
        self.name_ent.grid(row=0, column=1)
        
    def add_train(self):
        self.train_name = self.name_ent.get()
        if self.train_name:
            query = f"INSERT INTO Trains VALUES ('{self.train_name}')"
            cursor.execute(query)
            messagebox.showinfo("Warning", f"You added {self.train_name} to the Trains table")
        else:
            messagebox.showinfo("Warning", f"Name is empty")

    def stations(self):
        self.frame.destroy()
        self.btn_add.destroy()

        self.btn_add = Button(self.Canvas, text='Add', font=self.font, command=self.add_train_frame)
        self.btn_add.place(height=30,  width=120, x=400, y=50)

        self.frame = Frame(self.Canvas)
        self.frame.place(height=600, width=380, x=140, y=100)

        query = f"SELECT * FROM Stations"
        stations = self.cursor.execute(query)

        i=0
        self.label_id = Label(self.frame, text='ID', font=('Roboto', 14, 'bold'))
        self.label_id.grid(row=i, column=0)

        self.label_name = Label(self.frame, text='Station name', font=('Roboto', 14, 'bold'))
        self.label_name.grid(row=i, column=1)

        self.label_name = Label(self.frame, text='Satation city', font=('Roboto', 14, 'bold'))
        self.label_name.grid(row=i, column=2)
        for station in stations:
            i+=1
            station_id = station[0]
            station_name = station[1]
            station_city = station[2]

            self.label_id = Label(self.frame, text=station_id, font=self.font)
            self.label_id.grid(row=i, column=0)

            self.label_name = Label(self.frame, text=station_name, font=self.font)
            self.label_name.grid(row=i, column=1)

            self.label_name = Label(self.frame, text=station_city, font=self.font)
            self.label_name.grid(row=i, column=2)

Login(cursor, 1)