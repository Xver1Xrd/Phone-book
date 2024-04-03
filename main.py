import tkinter as tk
from tkinter import ttk
import sqlite3
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()
    def init_main(self):
            
        toolbar = tk.Frame(bg='#d7d7d7', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X) 
        # ДОБАВЛЕНИЕ 
        self.img_add = tk.PhotoImage(file='./img/add.png')
        btn_add = tk.Button(toolbar, text='Добавить', bg='#d7d7d7', 
                            bd=0, image=self.img_add, command=self.open_child)
        btn_add.pack(side=tk.LEFT)
        # ИЗМЕНЕНИЕ
        self.update_img = tk.PhotoImage(file='./img/update.png')
        btn_edit = tk.Button(toolbar, text='Изменить', bg='#d7d7d7', 
                            bd=0, image=self.update_img, command=self.open_update_dialog)
        btn_edit.pack(side=tk.LEFT) 
        # ИЗМЕНЕНИЕ      
        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        btn_delete = tk.Button(toolbar, text='Удалить', bg='#d7d7d7',
                               bd=0, image=self.delete_img, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)
        # ПОИСК
        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, text='Поиск', bg='#d7d7d7',
                               bd=0, image=self.search_img, command=self.open_search)
        btn_search.pack(side=tk.LEFT)
        # ОБНОВЛЕНИЕ
        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh = tk.Button(toolbar, text='Обновить', bg='#d7d7d7',
                               bd=0, image=self.refresh_img, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)
        # создания таблички
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'phone', 'email', 'salary'),
                                 height=45, show='headings')
        
        # колонки
        self.tree.column('ID', width=45, anchor=tk.CENTER)
        self.tree.column('name', width=220, anchor=tk.CENTER)
        self.tree.column('phone', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('salary', width=80, anchor=tk.CENTER)
        
        # названия
        self.tree.heading('ID', text='id')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('salary', text='Зарплата')
        self.tree.pack(side=tk.LEFT)
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)
    # функция для добавления данных
    def records(self, name, phone, email, salary):
        self.db.insert_data(name, phone, email, salary)
        self.view_records()
    def update_record(self, name, phone, email, salary):
        id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cur.execute('''UPDATE users SET name=?, phone=?, email=?, salary=? WHERE ID=?''',
                            (name, phone, email, salary, id))
        self.db.conn.commit()
        self.view_records()
    # вывод всех данных и бд в таблицу главного окна
    def view_records(self):
        self.db.cur.execute('''SELECT * FROM users ''')
        
        [self.tree.delete(i) for i in self.tree.get_children()]
        
        [self.tree.insert('', 'end', values=row)
         for row in self.db.cur.fetchall()]
    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.cur.execute('''DELETE FROM users WHERE ID=?''',
                                (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()
    def search_records(self, name):
        name = ('%' + name + '%')
        self.db.cur.execute('''SELECT * FROM users WHERE name LIKE ?''', (name, ))
        [self.tree.delete(i) for i in self.tree.get_children()]     
        [self.tree.insert('', 'end', values=row)
         for row in self.db.cur.fetchall()]
        
###################################################################################################        
    # функция для открытия дочернего окна
    def open_child(self):
        Child()
    # функция для окрытия окна обновления
    def open_update_dialog(self):
        Update()
    # функция для открытия поиска
    def open_search(self):
        Search()
###################################################################################################        
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app
    def init_child(self):
        # параметры окошка
        self.title('Добавление сотрудника')
        self.geometry('400x220')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        # надписи для полей ввода
        label_name = tk.Label(self, text='ФИО: ')
        label_name.place(x=50, y=50)
        label_phone = tk.Label(self, text='Телефон: ')
        label_phone.place(x=50, y=80)
        label_email = tk.Label(self, text='E-mail: ')
        label_email.place(x=50, y=110)
        label_salary = tk.Label(self, text='Зарплата: ')
        label_salary.place(x=50, y=140)
        # поля ввода
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=200, y=80)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)   
        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=140)
        # кнопки добавить и закрыть
        self.btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=10, y=180)
        self.btn_add = tk.Button(self, text='Добавить')
        self.btn_add.place(x=320, y=180)
        self.btn_add.bind('<Button-1>', lambda event:
                     self.view.records(self.entry_name.get(),
                                       self.entry_phone.get(),
                                       self.entry_email.get(),
                                       self.entry_salary.get()))
        
###################################################################################################
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()
    def init_edit(self):
        self.title('Редактировать позицию') 
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=300, y=180)
        self.btn_add.destroy()
        btn_edit.bind('<Button-1>', lambda event:
            self.view.update_record(self.entry_name.get(),
                            self.entry_phone.get(),
                            self.entry_email.get(),
                            self.entry_salary.get()))
        
    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        self.db.cur.execute('''SELECT * FROM users WHERE ID=?''', (id, ))
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])
###################################################################################################
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app
    def init_child(self):
        self.title('Поиск')
        self.geometry('300x200')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
###################################################################################################
        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=20, y=20)
        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=70, y=20)
###################################################################################################
        self.btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=10, y=160)
        self.btn_search = tk.Button(self, text='Найти')
        self.btn_search.place(x=240, y=160)
        self.btn_search.bind('<Button-1>', lambda event: 
                             self.view.search_records(self.entry_name.get()))
###################################################################################################        
class DB:
# создание базы данных ну и таблицы
    def __init__(self):
        self.conn = sqlite3.connect('employees.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS users(
                         id INTEGER PRIMARY KEY,
                         name TEXT,
                         phone TEXT,
                         email TEXT,
                         salary TEXT
                                            )
                        ''')
        self.conn.commit()
# добавление контакта    
    def insert_data(self, name, phone, email, salary):
        self.cur.execute('''
        INSERT INTO users (name, phone, email, salary)
        VALUES(?, ?, ?, ?) ''', (name, phone, email, salary))
        self.conn.commit()
# on startup
if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Список сотрудников компании')
    root.geometry('660x450')
    root.configure(bg='white')
    root.resizable(False, False)
    root.mainloop()