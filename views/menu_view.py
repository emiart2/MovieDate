import tkinter as tk
from views.main_view import MainView
from views.add_view import AddView
from views.database_view import DatabaseView

class MenuView:
    def __init__(self, root, films, csv_file):
        self.root = root
        self.films = films
        self.csv_file = csv_file

        frame = tk.Frame(root)
        frame.pack(expand=True)

        tk.Label(frame, text="MovieDate", font=("Arial", 20)).pack(pady=20)

        tk.Button(frame, text="Propozycje filmów", width=25,
                  command=lambda: self.show(MainView)).pack(pady=10)

        tk.Button(frame, text="Dodaj nowy film", width=25,
                  command=lambda: self.show(AddView)).pack(pady=10)

        tk.Button(frame, text="Przeglądaj bazę", width=25,
                  command=lambda: self.show(DatabaseView)).pack(pady=10)


    #shows any view (main, add, database)
    def show(self, ViewClass):
        for widget in self.root.winfo_children():
            widget.destroy()
        ViewClass(self.root, self.films, self.csv_file, self.back_to_menu)


    #shows menu view
    def back_to_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        MenuView(self.root, self.films, self.csv_file)
