import cv2
import darknet
import psycopg2
from config import host, user, password, db_name, port
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

#интерфейс
class Main_App(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_app()
        self.data_table_record()
    def init_app(self):

        self.conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            port=port
        )
        self.cur = self.conn.cursor()

        self.table_frame = tk.Frame()
        self.table_frame.place(x=35, y=40)
        self.label_history = tk.Label(text="История")
        self.label_history.place(x=35, y=10)
        self.button_add = tk.Button(text="Добавить", command=self.open_dialog)
        self.button_add.place(x=35, y=380)
        self.button_update = tk.Button(text="Редактировать")
        self.button_update.place(x=110, y=380)
        self.button_delete = tk.Button(text="Удалить")
        self.button_delete.place(x=215, y=380)

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

    def data_table_record(self): #вставка данных из бд в таблицу
        query = "SELECT id_admission, name, state_license_num, base FROM admission ORDER BY id_admission ASC"
        self.cur.execute(query)
        rows = self.cur.fetchall()
        for i in rows:
            self.data_table.insert('', tk.END, values=i)
    def data_table_insert(self, id, name, num, base): #добавление данных в таблтцу
            query = "INSERT INTO admission(id_admission, name, state_license_num, base) VALUES (?, ?, ?, ?)"
            self.cur.execute(query, (id, name, num, base))
            self.conn.commit()
            self.data_table_record()

    def open_dialog(self):
        Window_Childe()


class Window_Childe(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app
    def init_child(self):
        self.title('Добавление нового пользователя')
        self.geometry('450x300')
        self.resizable(False, False)

        self.label_id = ttk.Label(self, text="Номер")
        self.label_id.place(x=40, y=5)
        self.entry_id =ttk.Entry(self)
        self.entry_id.place(x=180, y=5)

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

        self.button_ok = ttk.Button(self, text="ОК")
        self.button_ok.place(x=40, y=150)
        self.button_ok.bind('<button-1>', lambda event: self.view.data_table_insert(
            self.entry_id.get(),
            self.entry_name.get(),
            self.entry_num.get(),
            self.entry_base.get()
        ))
        self.button_otmena = ttk.Button(self, text="Отмена")
        self.button_otmena.place(x=40, y=200)

        self.grab_set()
        self.focus_set()

class DataBase():
    def __init__(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = Main_App(root)
    root.title('Test')
    root.geometry('1020x600')
    root.resizable(False, False)
    app.mainloop()