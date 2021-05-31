from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
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

class Admin():
    def __init__(self, cursor, user_id):
        self.root = Tk()
        self.root.title('Railway')
        self.root.geometry('1000x600')
        self.root.resizable(width=False, height=False)
        self.font = ('Roboto', 14)

        self.Canvas = Canvas(self.root, height=600, width=900)
        self.Canvas.place(x=50, y=0)

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
        

        Label(self.Canvas, text=f"Hello, {self.firstname} {self.lastname}", font=self.font).place(x=0, y=20)
        
        Button(self.Canvas, text="Trains", font=self.font, command=self.train).place(x=0, y=60, width=100, height=30)
        Button(self.Canvas, text="Stations", font=self.font, command=self.station).place(x=100, y=60, width=100, height=30)
        Button(self.Canvas, text="Tracks", font=self.font, command=self.track).place(x=200, y=60, width=100, height=30)
        Button(self.Canvas, text="Users", font=self.font, command=self.user).place(x=300, y=60, width=100, height=30)
        Button(self.Canvas, text="Schedule", font=self.font, command=self.schedule).place(x=400, y=60, width=100, height=30)

        self.create_frame()

        self.root.mainloop()
    
    def create_frame(self):
        self.frame = Frame(self.Canvas, bg='red')
        self.frame.place(height=600, width=900, y=100)

    def train(self):
        self.frame.destroy()
        self.create_frame()
        Trains(self) 

    def station(self):
        self.frame.destroy()
        self.create_frame()
        Stations(self)

    def track(self):
        self.frame.destroy()
        self.create_frame()
        Tracks(self)

    def user(self):
        self.frame.destroy()
        self.create_frame()
        Users(self)

    def schedule(self):
        self.frame.destroy()
        self.create_frame()
        Schedule(self)

class Trains():
    def __init__(self, admin):
        self.cursor = admin.cursor
        Label(admin.frame, text='ID', font=admin.font).place(x=0, y=0, height=30, width=100)
        Label(admin.frame, text='Train name', font=admin.font).place(x=0, y=30, height=30, width=100)

        self.id_ent = Entry(admin.frame, font=admin.font)
        self.id_ent.place(x=100, y=0, height=30, width=150)
        self.name_ent = Entry(admin.frame, font=admin.font)
        self.name_ent.place(x=100, y=30, height=30, width=150)

        Button(admin.frame, text='Add', font=admin.font, command=self.add_train).place(x=0, y=60, height=30, width=250)
        Button(admin.frame, text='Update', font=admin.font, command=self.update_train).place(x=0, y=90, height=30, width=250)
        Button(admin.frame, text='Delete', font=admin.font, command=self.del_train).place(x=0, y=120, height=30, width=250)
        # Button(self.frame, text='Search', font=self.font, command=self.train_search).place(x=0, y=150, height=30, width=100)
        

        cols = ('id', 'Train_name')
        self.listbox = ttk.Treeview(admin.frame, columns=cols, show='headings')

        for col in cols:
            self.listbox.heading(col, text=col)
            self.listbox.place(x=250, y=0, height=600, width=650)

        cursor.execute('SELECT * FROM Trains')
        Trains = cursor.fetchall()
        for i , (id, train_name) in enumerate(Trains, start=1):
            self.listbox.insert("", "end", values=(id, train_name))
        self.listbox.bind('<Double-Button-1>', self.TrainSetValue)

    def add_train(self):
        self.id = self.id_ent.get()
        self.name =self.name_ent.get()
        if self.name:
            query = f"INSERT INTO Trains VALUES ('{self.name}')"
            cursor.execute(query)
        else:
            messagebox.showinfo("Warning", f"Can not add")

        self.id_ent.delete(0, END)
        self.name_ent.delete(0, END)

    def del_train(self):
        self.id = self.id_ent.get()
        self.name =self.name_ent.get()
        
        if self.id and self.name:
            query = f"DELETE FROM Trains WHERE Train_ID={self.id} AND Train_name='{self.name}'"
        elif self.id:
            query = f"DELETE FROM Trains WHERE Train_ID={self.id}"
        elif self.name:
            query = f"DELETE FROM Trains WHERE Train_name='{self.name}'"
        else:
            query = ""
            messagebox.showinfo("Warning", f"Can not delete")
        if query:
            cursor.execute(query)
            messagebox.showinfo("Warning", f"Successfully deleted")
        self.id_ent.delete(0, END)
        self.name_ent.delete(0, END)    

    def update_train(self):
        self.id = self.id_ent.get()
        self.name =self.name_ent.get()

        if self.name and self.id:
            query = f"UPDATE Trains SET Train_name='{self.name}' WHERE Train_ID={self.id}"
            cursor.execute(query)
        else:
            messagebox.showinfo("Warning", f"Can not update")    

    def TrainSetValue(self, event):
        self.id_ent.delete(0, END)
        self.name_ent.delete(0, END)
        row_id = self.listbox.selection()[0]
        select = self.listbox.set(row_id)
        self.id_ent.insert(0, select['id'])
        self.name_ent.insert(0, select['Train_name'])    

class Stations():
    def __init__(self, admin):
        self.cursor = admin.cursor
        Label(admin.frame, text='ID', font=admin.font).place(x=0, y=0, height=30, width=100)
        Label(admin.frame, text='Name', font=admin.font).place(x=0, y=30, height=30, width=100)
        Label(admin.frame, text='City', font=admin.font).place(x=0, y=60, height=30, width=100)

        self.id_ent = Entry(admin.frame, font=admin.font)
        self.id_ent.place(x=100, y=0, height=30, width=150)
        self.name_ent = Entry(admin.frame, font=admin.font)
        self.name_ent.place(x=100, y=30, height=30, width=150)
        self.city_ent = Entry(admin.frame, font=admin.font)
        self.city_ent.place(x=100, y=60, height=30, width=150)

        Button(admin.frame, text='Add', font=admin.font, command=self.add_station).place(x=0, y=90, height=30, width=250)
        Button(admin.frame, text='Update', font=admin.font, command=self.upd_station).place(x=0, y=120, height=30, width=250)
        Button(admin.frame, text='Delete', font=admin.font, command=self.del_station).place(x=0, y=150, height=30, width=250)

        cols = ('ID', 'Station_name', 'Station_city')
        self.listbox = ttk.Treeview(admin.frame, columns=cols, show='headings')

        for col in cols:
            self.listbox.heading(col, text=col)
            self.listbox.place(x=250, y=0, height=600, width=650)

        self.cursor.execute('SELECT * FROM Stations')
        Stations = cursor.fetchall()
        for i, (id, Station_name, Station_city) in enumerate(Stations, start=1):
            self.listbox.insert("", "end", values=(id, Station_name, Station_city))
        self.listbox.bind('<Double-Button-1>', self.StationSetValues)

    def StationSetValues(self, event):
        self.id_ent.delete(0, END)
        self.name_ent.delete(0, END)
        self.city_ent.delete(0, END)
        row_id = self.listbox.selection()[0]
        select = self.listbox.set(row_id)
        self.id_ent.insert(0, select['ID'])
        self.name_ent.insert(0, select['Station_name'])
        self.city_ent.insert(0, select['Station_city'])

    def add_station(self):
        self.id = self.id_ent.get()
        self.name = self.name_ent.get()
        self.city = self.city_ent.get()
        if self.name:
            query = f"INSERT INTO Stations VALUES ('{self.name}', '{self.city}')"
            self.cursor.execute(query)
            messagebox.showinfo("Warning", f"You successfully add {self.name}")
        else:
            messagebox.showinfo("Warning", f"Can not add")

        self.id_ent.delete(0, END)
        self.name_ent.delete(0, END)
        self.city_ent.delete(0, END)

    def upd_station(self):
        self.id = self.id_ent.get()
        self.name = self.name_ent.get()
        self.city = self.city_ent.get()
        if self.id:
            query = f"""UPDATE Stations 
                        SET Station_name = '{self.name}', Station_city='{self.city}' 
                        WHERE Station_ID={self.id}"""
            self.cursor.execute(query)
            messagebox.showinfo("Warning", f"You successfully UPDATED {self.name}")
        else:
            messagebox.showinfo("Warning", f"Can not delete")
        self.id_ent.delete(0, END)
        self.name_ent.delete(0, END)
        self.city_ent.delete(0, END)

    def del_station(self):
        self.id = self.id_ent.get()
        self.name = self.name_ent.get()
        self.city = self.city_ent.get()
        if self.id:
            query = f"DELETE FROM Stations WHERE Station_ID = {self.id}"
            self.cursor.execute(query)
            messagebox.showinfo("Warning", f"You successfully deleted {self.name}")
        else:
            messagebox.showinfo("Warning", f"Can not delete")
        self.id_ent.delete(0, END)
        self.name_ent.delete(0, END)
        self.city_ent.delete(0, END)

class Tracks():
    def __init__(self, admin):
        self.cursor = admin.cursor
        Label(admin.frame, text='ID', font=admin.font).place(x=0, y=0, height=30, width=100)
        Label(admin.frame, text='Station 1', font=admin.font).place(x=0, y=30, height=30, width=100)
        Label(admin.frame, text='Station 2', font=admin.font).place(x=0, y=60, height=30, width=100)

        self.id_ent = Entry(admin.frame, font=admin.font)
        self.id_ent.place(x=100, y=0, height=30, width=150)

        query = "SELECT * FROM Stations"
        cursor.execute(query)
        self.stations = cursor.fetchall()
        self.stas = [station[1] for station in self.stations]

        self.station1_ent = ttk.Combobox(admin.frame, values=self.stas, font=admin.font)
        self.station1_ent.place(x=100, y=30, height=30, width=150)

        self.station2_ent = ttk.Combobox(admin.frame, values=self.stas, font=admin.font)
        self.station2_ent.place(x=100, y=60, height=30, width=150)

        Button(admin.frame, text='Add', font=admin.font, command=self.track_add).place(x=0, y=90, height=30, width=250)
        Button(admin.frame, text='Update', font=admin.font, command=self.track_upd).place(x=0, y=120, height=30, width=250)
        Button(admin.frame, text='Delete', font=admin.font, command=self.track_del).place(x=0, y=150, height=30, width=250)

        cols = ('ID', 'Station_dep', 'Station_arr')
        self.listbox = ttk.Treeview(admin.frame, columns=cols, show='headings')

        for col in cols:
            self.listbox.heading(col, text=col)
        self.listbox.place(x=250, y=0, height=600, width=650)

        self.cursor.execute('EXEC select_tracks')
        Stations = cursor.fetchall()
        for i, (id, Station_dep, Station_arr) in enumerate(Stations, start=1):
            self.listbox.insert("", "end", values=(id, Station_dep, Station_arr))
        self.listbox.bind('<Double-Button-1>', self.TrackSetValues)

    def track_add(self):
        self.station1 = self.station1_ent.get()
        self.station2 = self.station2_ent.get()
        if self.station1 and self.station2:
            self.station1_id = self.stations[self.stas.index(self.station1)][0]
            self.station2_id = self.stations[self.stas.index(self.station2)][0]
            query = f'INSERT INTO Tracks VALUES ({self.station1_id}, {self.station2_id}), ({self.station2_id}, {self.station1_id})'
            # cursor.execute(query)
            messagebox.showinfo("Warning", f"You successfuly add track {self.station1} {self.station2}")
        else:
            messagebox.showinfo("Warning", f"Can not add")

    def track_upd(self):
        self.id = self.id_ent.get()
        self.station1 = self.station1_ent.get()
        self.station2 = self.station2_ent.get()
        if self.id and self.station1 and self.station2:
            self.station1_id = self.stations[self.stas.index(self.station1)][0]
            self.station2_id = self.stations[self.stas.index(self.station2)][0]
            query = f"""UPDATE Tracks 
                        SET Station_ID_dep = {self.station1_id}, Station_ID_arr={self.station2_id} 
                        WHERE Track_ID={self.id}"""
            self.cursor.execute(query)
            messagebox.showinfo("Warning", f"You successfully UPDATED")
        else:
            messagebox.showinfo("Warning", f"Can not update")

    def track_del(self):
        self.id = self.id_ent.get()
        if self.id:
            query = f"DELETE FROM Tracks WHERE Track_ID={self.id}"
            cursor.execute(query)
            messagebox.showinfo("Warning", f"Successfully deleted")
        else:
            messagebox.showinfo("Warning", f"Can not update")

    def TrackSetValues(self, event):
        self.id_ent.delete(0, END)
        self.station1_ent.delete(0, END)
        self.station2_ent.delete(0, END)
        row_id = self.listbox.selection()[0]
        select = self.listbox.set(row_id)
        self.id_ent.insert(0, select['ID'])
        self.station1_ent.insert(0, select['Station_dep'])
        self.station2_ent.insert(0, select['Station_arr'])

class Users():
    def __init__(self, admin):
        self.cursor = admin.cursor
        self.frame = admin.frame
        Label(admin.frame, text='ID', font=admin.font).place(x=0, y=0, height=30, width=100)

        self.id_ent = Entry(admin.frame, font=admin.font)
        self.id_ent.place(x=100, y=0, height=30, width=150)

        cols = ('ID', 'Firstname', 'Lastname', 'E-mail', 'IsAdmin')
        self.listbox = ttk.Treeview(admin.frame, columns=cols, show='headings')
        Button(admin.frame, text='Orders', font=admin.font, command=self.orders).place(x=0, y=30, height=30, width=250)
        Button(admin.frame, text='Passengers', font=admin.font, command=self.passengers).place(x=0, y=60, height=30, width=250)
        Button(admin.frame, text='Discount Card', font=admin.font, command=self.discount_cards).place(x=0, y=90, height=30, width=250)

        for col in cols:
            self.listbox.heading(col, text=col)

        self.cursor.execute('SELECT * FROM Users')
        Users = cursor.fetchall()
        for user in Users:
            user_id = user[0]
            user_fn = user[1]
            user_ln = user[2]
            user_email = user[3]
            user_ia = user[6]
            values = (user_id, user_fn, user_ln, user_email, user_ia)
            self.listbox.insert('',END, values=values)
        self.listbox.place(x=250, y=0, height=600, width=650)
        self.listbox.bind('<Double-Button-1>', self.SetUserValues)

    def SetUserValues(self, event):
        self.id_ent.delete(0, END)
        row_id = self.listbox.selection()[0]
        select = self.listbox.set(row_id)
        self.user_name = [select['Firstname'], select['Lastname']]
        self.id_ent.insert(0, select['ID'])

    def orders(self):
        self.id = self.id_ent.get()
        if self.id:
            self.listbox.destroy()
            query = f"SELECT * FROM Orders WHERE [User_ID]={self.id}"
            cursor.execute(query)
            orders = cursor.fetchall()
            cols = ('ID', 'Creation', 'Paid', 'User')
            self.listbox = ttk.Treeview(self.frame, columns=cols, show='headings')

            for col in cols:
                self.listbox.heading(col, text=col)
            
            for order in orders:
                self.id = order[0]
                self.cration = order[1]
                self.paid = order[2]
                self.user = f"{self.user_name[0]} {self.user_name[1]}"
                values = (self.id, self.cration, self.paid, self.user)
                self.listbox.insert('',END, values=values)

            self.listbox.place(x=250, y=0, height=600, width=650)
        else:
            messagebox.showinfo("Warning", f"ID is empty")

    def discount_cards(self):
        self.id = self.id_ent.get()
        if self.id:
            self.listbox.destroy()
            query = f"SELECT * FROM Discount_cards WHERE [User_ID]={self.id}"
            cursor.execute(query)
            cards = cursor.fetchall()
            cols = ('ID', 'Number of orders', 'Creation', 'Is Active', 'Discount', 'User')
            self.listbox = ttk.Treeview(self.frame, columns=cols, show='headings')

            for col in cols:
                self.listbox.heading(col, text=col)

            for card in cards:
                self.id = card[0]
                self.noo = card[1]
                self.creation = card[2]
                self.is_active = card[3]
                self.discount = card[4]
                self.user = f"{self.user_name[0]} {self.user_name[1]}"
                values = (self.id, self.noo, self.creation, self.is_active, self.discount, self.user)
                self.listbox.insert('',END, values=values)

            self.listbox.place(x=250, y=0, height=600, width=650)
        else:
            messagebox.showinfo("Warning", f"ID is empty")

    def passengers(self):
        self.id = self.id_ent.get()
        if self.id:
            self.listbox.destroy()
            query = f"EXEC select_passengers {self.id}"
            cursor.execute(query)
            passengers = cursor.fetchall()

            cols = ('ID', 'Firstname', 'Lastname', 'Document', 'Phone', 'Birthday', 'Price', 'Seat', 'Coach', 'Departation', 'Arrival', 'From', 'To')
            self.listbox = ttk.Treeview(self.frame, columns=cols, show='headings')

            for col in cols:
                self.listbox.heading(col, text=col)

            for passenger in passengers:
                id = passenger[0]
                fn = passenger[1]
                ln = passenger[2]
                document = passenger[3]
                phone = passenger[4]
                dob = passenger[5]
                price = passenger[6]
                seat = passenger[9]
                coach = passenger[10]
                dt_dep = passenger[12]
                dt_arr = passenger[13]
                station_name_dep = passenger[14]
                station_name_arr = passenger[15] 
                values = (id, fn, ln, document, phone, dob, price, seat, coach, dt_dep, dt_arr, station_name_dep, station_name_arr)
                self.listbox.insert('',END, values=values)
            self.listbox.place(x=250, y=0, height=600, width=650)

        else:
            messagebox.showinfo("Warning", f"ID is empty")
        
    def losecards(self):
        query = "EXEC lose_cards"
        cursor.execute(query)

class Schedule():
    def __init__(self,admin):
        self.cursor = admin.cursor
        self.frame = admin.frame
        Label(self.frame, text='ID', font=admin.font).place(x=0, y=0, height=30, width=100)
        Label(self.frame, text='Dep date', font=admin.font).place(x=0, y=30, height=30, width=100)
        Label(self.frame, text='Dep time', font=admin.font).place(x=0, y=60, height=30, width=100)
        Label(self.frame, text='Arr date', font=admin.font).place(x=0, y=90, height=30, width=100)
        Label(self.frame, text='Arr time', font=admin.font).place(x=0, y=120, height=30, width=100)
        Label(self.frame, text='Price', font=admin.font).place(x=0, y=150, height=30, width=100)
        Label(self.frame, text='Track', font=admin.font).place(x=0, y=180, height=30, width=100)
        Label(self.frame, text='Train', font=admin.font).place(x=0, y=210, height=30, width=100)

        self.id_ent = Entry(self.frame, font=admin.font)
        self.id_ent.place(x=100, y=0, height=30, width=150)
        
        
        self.dep_date = DateEntry(self.frame, font=admin.font)
        self.dep_date.place(x=100, y=30, height=30, width=150)
        self.arr_date = DateEntry(self.frame, font=admin.font)
        self.arr_date.place(x=100, y=60, height=30, width=150)

        self.dep_hour_ent = Spinbox(self.frame, from_=0, to=23, font=admin.font)
        self.dep_hour_ent.place(x=100, y=90, height=30, width=75)
        self.dep_min_ent = Spinbox(self.frame, from_=0, to=59, font=admin.font)
        self.dep_min_ent.place(x=175, y=90, height=30, width=75)
        self.arr_hour_ent = Spinbox(self.frame, from_=0, to=23, font=admin.font)
        self.arr_hour_ent.place(x=100, y=120, height=30, width=75)
        self.arr_min_ent = Spinbox(self.frame, from_=0, to=59, font=admin.font)
        self.arr_min_ent.place(x=175, y=120, height=30, width=75)

        self.price_ent = Entry(self.frame, font=admin.font)
        self.price_ent.place(x=100, y=150, height=30, width=150)

        query = f"EXEC select_tracks"
        cursor.execute(query)
        tracks = cursor.fetchall()
        track_list = [[track[0], f'{track[1]}-{track[2]}'] for track in tracks]
        track_id = [item[0] for item in track_list]
        track_s = [item[1] for item in track_list]
        self.track_ent = ttk.Combobox(self.frame, values=track_s, font=admin.font)
        self.track_ent.place(x=100, y=180, height=30, width=150)
        
        query = f"SELECT * FROM Trains"
        cursor.execute(query)
        trains = cursor.fetchall()
        train_id = [train[0] for train in trains]
        trains_list = [train[1] for train in trains]
        self.train = ttk.Combobox(self.frame, values=trains_list, font=admin.font)
        self.train.place(x=100, y=210, height=30, width=150)

        # query = "SELECT * FROM Schedule WHERE DT_dep > GETDATE()"
        cols = ('ID', 'Dep', 'Arr', 'Price', 'Track', 'Train', 'Is_delay')
        self.listbox = ttk.Treeview(admin.frame, columns=cols, show='headings')
        for col in cols:
            self.listbox.heading(col, text=col)
        self.listbox.place(x=250, y=0, height=600, width=650)

        query = "SELECT * FROM Schedule"
        cursor.execute(query)
        schedules = cursor.fetchall()
        for schedule in schedules:
            id_ = schedule[0]
            dep = schedule[1]
            arr = schedule[2]
            price = schedule[3]  
            track = track_s[track_id.index(schedule[4])]
            train = trains_list[train_id.index(schedule[5])]
            is_delay = schedule[6]
            values = (id_, dep, arr, price, track, train, is_delay)
            self.listbox.insert('', END, values = values)
            
    

Admin(cursor, 1)