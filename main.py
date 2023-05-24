#import cv2
import psycopg2
from config import host, user, password, db_name, port
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import num_detection
from num_detection import num_plate


class MainApp(tk.Frame): # главное окно
    def __init__(self, root):
        super().__init__(root)
        self.db = db
#        self.autorization = autorization
        self.init_exit()
        self.init_app()
        self.data_table_record()
        self.data_table_history_record()
        self.history_admission()


    def init_app(self):
        self.notebook = ttk.Notebook()
        self.notebook.place(height=500, width=1020)
        self.table_user_frame = tk.Frame(self.notebook)
        self.table_user_frame.place(x=35, y=40)
        self.table_history_frame = tk.Frame(self.notebook)
        self.table_history_frame.place(x=35, y=40)
        self.table_history_addmission_frame = tk.Frame(self.notebook)
        self.table_history_addmission_frame.place(x=35, y=40)
        self.notebook.add(self.table_history_addmission_frame, text='История допуска')
        self.notebook.add(self.table_history_frame, text='История авторизации')
        self.notebook.add(self.table_user_frame, text='Пользователи')

        self.button_add = tk.Button(self.table_user_frame, text="Добавить", command=self.open_dialog_add)
        self.button_add.place(x=35, y=420)

        self.button_update = tk.Button(self.table_user_frame, text="Редактировать", command=self.open_dialog_update)
        self.button_update.place(x=110, y=420)

        self.button_delete = tk.Button(self.table_user_frame, text="Удалить", command=self.data_table_delete)
        self.button_delete.place(x=215, y=420)

        self.columns1 = ("ID", "Name", "State lic num", "Base")
        self.data_table = ttk.Treeview(self.table_user_frame, columns=self.columns1, show="headings", height=15)
        self.data_table.place(width=1020, height=400)
        self.data_table.heading("ID", text="Номер", anchor=tk.W)
        self.data_table.column("#1", width=100, stretch=tk.FALSE)
        self.data_table.heading("Name", text="ФИО", anchor=tk.W)
        self.data_table.column("#2", width=250)
        self.data_table.heading("State lic num", text="Номер автотранспортного средства", anchor=tk.W)
        self.data_table.column("#3", width=300)
        self.data_table.heading("Base", text="Основание", anchor=tk.W)
        self.data_table.column("#4", width=300)

        self.columns2 = ("ID", "Name", "Action", "Time")
        self.data_table_history = ttk.Treeview(self.table_history_frame, columns=self.columns2, show="headings", height=15)
        self.data_table_history.place(width=1020, height=400)
        self.data_table_history.heading("ID", text="Номер", anchor=tk.W)
        self.data_table_history.column("#1", width=100, stretch=tk.FALSE)
        self.data_table_history.heading("Name", text="ФИО", anchor=tk.W)
        self.data_table_history.column("#2", width=300, stretch=tk.FALSE)
        self.data_table_history.heading("Action", text="Действие", anchor=tk.W)
        self.data_table_history.column("#3", width=400, stretch=tk.FALSE)
        self.data_table_history.heading("Time", text="Время", anchor=tk.W)
        self.data_table_history.column("#4", width=510, stretch=tk.FALSE)

        self.columns3 = ("ID", "Car", "Name", "Data")
        self.data_table_history_addmission = ttk.Treeview(self.table_history_addmission_frame, columns=self.columns3, show="headings", height=15)
        self.data_table_history_addmission.place(width=1020, height=400)
        self.data_table_history_addmission.heading("ID", text="Номер", anchor=tk.W)
        self.data_table_history_addmission.column("#1", width=100, stretch=tk.FALSE)
        self.data_table_history_addmission.heading("Car", text="Номер автомобиля", anchor=tk.W)
        self.data_table_history_addmission.column("#2", width=300, stretch=tk.FALSE)
        self.data_table_history_addmission.heading("Name", text="ФИО пользователя", anchor=tk.W)
        self.data_table_history_addmission.column("#3", width=400, stretch=tk.FALSE)
        self.data_table_history_addmission.heading("Data", text="Дата", anchor=tk.W)
        self.data_table_history_addmission.column("#4", width=500, stretch=tk.FALSE)


    def record(self, name, num, base):
        self.db.data_table_insert(name, num, base)
        self.data_table_record()
        self.data_table_history_record()

    def record2(self):
        self.data_table_history_record()
        self.data_table_history_entry_insert()


    def data_table_record(self):  # вставка данных из бд в таблицу
        self.db.cur.execute(
            "SELECT id_admission, name,state_license_num, base FROM admission ORDER BY id_admission ASC")
        [self.data_table.delete(i) for i in self.data_table.get_children()]
        [self.data_table.insert('', tk.END, values=row) for row in self.db.cur.fetchall()]

    def data_table_history_record(self):
        self.db.cur.execute(
            "SELECT id_act, name, action, time FROM history_test ORDER BY id_act ASC")
        [self.data_table_history.delete(i) for i in self.data_table_history.get_children()]
        [self.data_table_history.insert('', tk.END, values=row) for row in self.db.cur.fetchall()]

    def data_table_history_addmission_record(self):
        self.db.cur.execute(
            "SELECT id_admission, num_car_plate, name, data FROM history_addmission_test ORDER BY id_admission ASC")
        [self.data_table_history_addmission.delete(i) for i in self.data_table_history_addmission.get_children()]
        [self.data_table_history_addmission.insert('', tk.END, values=row) for row in self.db.cur.fetchall()]
        #self.history_admission()

    def history_admission(self):
        self.num_auto = num_plate
        print(self.num_auto)
        self.db.cur.execute("SELECT state_license_num FROM admission WHERE state_license_num='%(num)s'" % {'num': self.num_auto})
        self.check_num_plate = self.db.cur.fetchall()
        self.test = "test"
        self.time = datetime.now()

        self.query = ("INSERT INTO history_addmission_test " "(num_car_plate, name, data) " "VALUES ('%(num)s', '%(name)s', '%(data)s')" % {
                'num': num_plate,
                'name': self.test,
                'data': self.time
            })
        self.db.cur.execute(self.query)
        self.db.conn.commit()
        self.data_table_history_addmission_record()
        #print(self.num_auto)



    def data_table_history_entry_insert(self):
      #  self.au.init_button_autorization()
        self.data_table_history_record()

    #def data_table_history_exit_insert(self):
     #   self.action_exit = "Пользователь вышел из системы"
     #   self.time = datetime.now()

     #   self.query = (
        #        "INSERT INTO history_test " "(action, time) " "VALUES ('%(action)s', '%(time)s')" % {
#
       #     'action': self.action_exit,
      #      'time': self.time
      #  }
     #   )
    #    self.db.cur.execute(self.query)
     #   self.db.conn.commit()

    def data_table_update(self, name, num, base):
        self.db.cur.execute("UPDATE admission SET name='%(name)s', state_license_num='%(num)s', base='%(base)s' WHERE "
                            "id_admission='%(id_admission)s'" % {'name': name, 'num': num, 'base': base,
                                                                 'id_admission': self.data_table.set(
                                                                     self.data_table.selection()[0], "#1")})
        self.db.conn.commit()
        self.data_table_record()

    def data_table_delete(self):  # удаление данных из бд
        for select_item in self.data_table.selection():
            self.db.cur.execute("DELETE FROM admission WHERE id_admission='%(id_admission)s' " % {
                'id_admission': self.data_table.set(select_item, "#1")})
        self.db.conn.commit()
        self.data_table_record()

    def open_dialog_add(self):
        WindowChildeAdd()

    def open_dialog_update(self):
        Update()
    def init_exit(self): #обработка события нажатия на кнопку "Выход"
        self.exi_button = tk.Button(self.init_app(), text='Выход', command=self.quit)
        self.exi_button.place(x=950, y=550)
        self.exi_button.bind("<Button-1>")



class WindowChildeAutorization(tk.Toplevel): #окно авторизации
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.db = db
        self.root = root
        self.init_autorization()

    def init_autorization(self):
        self.title('Авторизация')
        self.geometry('450x300')
        self.resizable(False, False)

        self.label_log = ttk.Label(self, text='Логин')
        self.entry_log = ttk.Entry(self)
        self.label_log.place(x=200, y=50)
        self.entry_log.place(x=160, y=70)

        self.label_pass = ttk.Label(self, text='Пароль')
        self.entry_pass = ttk.Entry(self)
        self.label_pass.place(x=200, y=110)
        self.entry_pass.place(x=160, y=130)

        self.auto_button = ttk.Button(self, text="Авторизация", command=self.init_button_autorization)
        self.auto_button.place(x=180, y=200)

        self.exit_button = ttk.Button(self, text="Выход", command=self.quit)
        self.exit_button.place(x=183, y=230)

    def init_button_autorization(self):
        self.login = self.entry_log.get()

        self.password = self.entry_pass.get()
        self.action_entry = "Пользователь вошёл в систему"
        self.action_exit = "Пользователь вышел из системы"
        self.time = datetime.now()


        if len(self.login) == 0 or len(self.password) == 0:
            messagebox.showerror("Неправильный логин или пароль", "Введите правильный логин или пароль")

        self.db.cur.execute("SELECT login FROM guard_post WHERE login='%(login)s'" % {'login': self.login})
        self.check_login = self.db.cur.fetchall()

        self.db.cur.execute("SELECT password FROM guard_post WHERE password='%(password)s'" % {'password': self.password})
        self.check_password = self.db.cur.fetchall()

        if self.check_login[0][0] == self.login and self.check_password[0][0] == self.password:
            self.destroy()
            self.root.deiconify()
            self.query = (
                    "INSERT INTO history_test " "(name, action, time) " "VALUES ('%(name)s', '%(action)s', '%(time)s')" % {
                'name': self.login,
                'action': self.action_entry,
                'time': self.time
            }
            )
            self.db.cur.execute(self.query)
            self.db.conn.commit()
            self.view.data_table_history_record()

        elif self.check_login[0] != self.login and self.check_password[0] != self.password:
            messagebox.showerror("Неправильный логин или пароль", "Неправтльный логин или пароль, введите правильный логин или пароль")

    def dddd(self):
        while self.view.init_exit():
            self.query = (
                   "INSERT INTO history_test " "(name, action, time) " "VALUES ('%(name)s', '%(action)s', '%(time)s')" % {
                'name': self.login,
                'action': self.action_exit,
               'time': self.time
               }
            )
            self.db.cur.execute(self.query)
            self.db.conn.commit()

class WindowChildeAdd(tk.Toplevel): #окно добавления нового пользователя
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.init_child()

    def init_child(self):
        self.title('Добавление нового пользователя')
        self.geometry('450x300')
        self.resizable(False, False)

        self.label_name = ttk.Label(self, text="ФИО")
        self.label_name.place(x=40, y=40)
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=180, y=40)

        self.label_num = ttk.Label(self, text="Номер авто. средства")
        self.label_num.place(x=40, y=80)
        self.entry_num = ttk.Entry(self)
        self.entry_num.place(x=180, y=80)

        self.label_base = ttk.Label(self, text="Основание")
        self.label_base.place(x=40, y=120)
        self.entry_base = ttk.Entry(self)
        self.entry_base.place(x=180, y=120)

        self.button_ok = ttk.Button(self, text="Добавить")
        self.button_ok.place(x=40, y=150)
        self.button_ok.bind('<Button-1>', lambda event: self.view.record(
            self.entry_name.get(),
            self.entry_num.get(),
            self.entry_base.get()
        ))
        self.button_otmena = ttk.Button(self, text="Отмена", command=self.destroy)
        self.button_otmena.place(x=40, y=200)

        self.grab_set()
        self.focus_set()


class Update(WindowChildeAdd): #окно редактирования пользователя
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app

    def init_edit(self):
        self.title('Редактирование данных')
        button_edit = ttk.Button(self, text="Редактировать")
        button_edit.place(x=30, y=170)
        button_edit.bind('<Button-1>', lambda event: self.view.data_table_update(self.entry_name.get(),
                                                                                 self.entry_num.get(),
                                                                                 self.entry_base.get()))
        self.button_ok.destroy()


class DataBase:
    def __init__(self):
        super().__init__()
        self.conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            port=port
        )
        self.cur = self.conn.cursor()
        query = "SELECT id_admission, name,state_license_num, base FROM admission ORDER BY id_admission ASC"
        self.cur.execute(query)

    def data_table_insert(self, name, num, base):  # добавление данных в таблицу
        self.query = (
                "INSERT INTO admission " "(name, state_license_num, base) " "VALUES ('%(name)s', '%(num)s', "
                "'%(base)s')" % {
                    'name': name,
                    'num': num,
                    'base': base})
        self.cur.execute(self.query, (name, num, base))
        self.conn.commit()

if __name__ == "__main__":
    root = tk.Tk()
    db = DataBase()
    app = MainApp(root)
    autorization = WindowChildeAutorization()
    root.title('Информационная система "Шлагбаум"')
    root.geometry('1020x600')
    root.resizable(False, False)
    root.withdraw()
    app.mainloop()
