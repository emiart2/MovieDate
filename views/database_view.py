import tkinter as tk
from tkinter import ttk

class DatabaseView:
    def __init__(self, root, films,csv_file, back_callback):
        self.root = root
        self.films = films
        self.back_callback = back_callback

        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Baza filmów", font=("Arial", 14)).pack(pady=10)

        # tabela
        columns = ("Tytuł", "Autor", "Rok", "Gatunki", "Słowa kluczowe")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="w")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # wypełnienie danymi
        self.load_data()

        tk.Button(self.frame, text="Wróć", command=self.back_callback).pack(pady=10)

    def load_data(self):
        # wyczyszczenie starej zawartości
        for row in self.tree.get_children():
            self.tree.delete(row)

        # załadowanie filmów
        for f in self.films:
            self.tree.insert("", "end", values=(
                f.name,
                f.author,
                f.year,
                ", ".join(f.genre),
                ", ".join(f.key_words),
            ))
