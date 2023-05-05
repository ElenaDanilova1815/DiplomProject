# import cv2
import psycopg2
from config import host, user, password, db_name, port
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class MainApp(tk.Frame): # главное окно
    def __init__(self, root):
        super().__init__(root)
        self.db = db
        self.init_app()
        self.data_table_record()

    def init_app(self):
        self.table_frame = tk.Frame()
        self.table_frame.place(x=35, y=40)
        self.label_history = tk.Label(text="История")
        self.label_history.place(x=35, y=10)

        self.button_add = tk.Button(text="Добавить", command=self.open_dialog_add)
        self.button_add.place(x=35, y=380)

        self.button_update = tk.Button(text="Редактировать", command=self.open_dialog_update)
        self.button_update.place(x=110, y=380)

        self.button_delete = tk.Button(text="Удалить", command=self.data_table_delete)
        self.button_delete.place(x=215, y=380)

        self.exi_button = tk.Button(text='Выход', command=self.quit)
        self.exi_button.place(x=950, y=550)

        self.columns = ("ID", "Name", "State lic num", "Base")
        self.data_table = ttk.Treeview(self.table_frame, columns=self.columns, show="headings", height=15)
        self.data_table.pack(fill=tk.BOTH, expand=1)
        self.data_table.heading("ID", text="Номер", anchor=tk.W)
        self.data_table.column("#1", width=100, stretch=tk.FALSE)
        self.data_table.heading("Name", text="ФИО", anchor=tk.W)
        self.data_table.column("#2", width=250)
        self.data_table.heading("State lic num", text="Номер автотранспортного средства", anchor=tk.W)
        self.data_table.column("#3", width=300)
        self.data_table.heading("Base", text="Основание", anchor=tk.W)
        self.data_table.column("#4", width=300)

    def record(self, name, num, base):
        self.db.data_table_insert(name, num, base)
        self.data_table_record()

    def data_table_record(self):  # вставка данных из бд в таблицу
        self.db.cur.execute(
            "SELECT id_admission, name,state_license_num, base FROM admission ORDER BY id_admission ASC")
        [self.data_table.delete(i) for i in self.data_table.get_children()]
        [self.data_table.insert('', tk.END, values=row) for row in self.db.cur.fetchall()]

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

        if len(self.login) == 0 or len(self.password) == 0:
            messagebox.showinfo("d")

        self.db.cur.execute("SELECT login FROM guard_post WHERE login='%(login)s'" % {'login': self.login})
        self.check_login = self.db.cur.fetchone()

        self.db.cur.execute("SELECT password FROM guard_post WHERE password='%(password)s'" % {'password': self.password})
        self.check_password = self.db.cur.fetchone()

        if self.check_login[0][0] == self.login and self.check_password[0][0] == self.password:
            self.destroy()
            self.root.deiconify()
        elif self.check_login[0][0] != self.login and self.check_password[0][0] != self.password:
            messagebox.showinfo("s")

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

    def data_table_delete(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    db = DataBase()
    app = MainApp(root)
    autorization = WindowChildeAutorization()
    root.title('Test')
    root.geometry('1020x600')
    root.resizable(False, False)
    root.withdraw()
    app.mainloop()
