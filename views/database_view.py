import tkinter as tk
from tkinter import ttk
import pandas as pd

class DatabaseView:
    def __init__(self, root, films, csv_file, back_callback):
        self.root = root
        self.films = films
        self.csv_file = csv_file
        self.back_callback = back_callback

        # --- główny frame z tłem ---
        self.frame = tk.Frame(root, bg="#fbffae")
        self.frame.pack(fill="both", expand=True)

        # Tytuł
        tk.Label(
            self.frame, 
            text="Baza filmów", 
            font=("Arial", 30, "bold"), 
            fg="#ffaade", 
            bg="#fbffae"
        ).pack(pady=10)

        # --- filtry ---
        filter_frame = tk.Frame(self.frame, bg="#fbffae")
        filter_frame.pack(pady=5)

        tk.Label(filter_frame, text="Szukaj:", bg="#fbffae").pack(side="left")
        self.search_var = tk.StringVar()
        tk.Entry(filter_frame, textvariable=self.search_var).pack(side="left", padx=5)
        self.search_var.trace_add("write", lambda *args: self.load_data())

        self.show_to_watch = tk.IntVar()
        tk.Checkbutton(
            filter_frame, 
            text="Do obejrzenia", 
            variable=self.show_to_watch,
            command=self.load_data,
            bg="#fbffae"
        ).pack(side="left", padx=5)

        self.show_watched = tk.IntVar()
        tk.Checkbutton(
            filter_frame, 
            text="Obejrzane", 
            variable=self.show_watched,
            command=self.load_data,
            bg="#fbffae"
        ).pack(side="left", padx=5)

        # --- tabela ---
        columns = ("Tytuł", "Autor", "Rok", "Do obejrzenia", "Obejrzany")
        self.tree = ttk.Treeview(
            self.frame, columns=columns, show="headings", selectmode="browse"
        )

        style = ttk.Style()
        style.configure("Treeview", background="#fbffae", foreground="#545454", rowheight=25, fieldbackground="#fbffae")
        style.map("Treeview", background=[("selected", "#ffaade")], foreground=[("selected", "white")])

        for col in columns:
            if col in ["Tytuł", "Autor"]:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=190, anchor="w")
            elif col == "Rok":
                self.tree.heading(col, text=col)
                self.tree.column(col, width=50, anchor="w")
            else:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=120, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # menu kontekstowe
        self.menu = tk.Menu(self.frame, tearoff=0)
        self.menu.add_command(label="Oznacz jako do obejrzenia", command=self.mark_to_watch)
        self.menu.add_command(label="Oznacz jako obejrzany", command=self.mark_watched)

        self.tree.bind("<Button-3>", self.show_context_menu)

        # wypełnienie danymi
        self.load_data()

        # przycisk Wróć
        tk.Button(
            self.frame, text="Wróć", 
            bg="#ffaade", fg="white", font=("Arial", 10), height=2, width=20,
            command=self.back_callback
        ).pack(pady=10)


    def load_data(self):
        # wyczyszczenie starej zawartości
        for row in self.tree.get_children():
            self.tree.delete(row)

        search_text = self.search_var.get().lower()

        for f in self.films:
            # filtr wyszukiwania
            if search_text and search_text not in f.name.lower() and search_text not in f.author.lower():
                continue
            # filtr checkboxów
            if self.show_to_watch.get() and not f.to_watch:
                continue
            if self.show_watched.get() and not f.watched:
                continue

            self.tree.insert("", "end", values=(
                f.name,
                f.author,
                f.year,
                "✓" if f.to_watch else "",
                "✓" if f.watched else "",
            ))

    def show_context_menu(self, event):
        selected = self.tree.identify_row(event.y)
        if selected:
            self.tree.selection_set(selected)
            self.menu.post(event.x_root, event.y_root)

    def mark_to_watch(self):
        selected = self.tree.selection()
        if not selected:
            return
        item = selected[0]
        title = self.tree.item(item, "values")[0]
        film = next(f for f in self.films if f.name == title)
        film.to_watch, film.watched = 1, 0
        self.save_all()
        self.load_data()

    def mark_watched(self):
        selected = self.tree.selection()
        if not selected:
            return
        item = selected[0]
        title = self.tree.item(item, "values")[0]
        film = next(f for f in self.films if f.name == title)
        film.to_watch, film.watched = 0, 1
        self.save_all()
        self.load_data()

    def save_all(self):
        rows = []
        for f in self.films:
            rows.append({
                "name": f.name,
                "author": f.author,
                "year": f.year,
                "genre": ";".join(f.genre),
                "key_words": ";".join(f.key_words),
                "to_watch": f.to_watch,
                "watched": f.watched,
            })
        df = pd.DataFrame(rows)
        df.to_csv(self.csv_file, index=False)

