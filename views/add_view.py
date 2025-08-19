import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os
from models.Film import Film

def save_film_to_csv(film: Film, csv_file: str):
    row = {
        "name": film.name,
        "author": film.author,
        "year": film.year,
        "genre": ";".join(film.genre),
        "key_words": ";".join(film.key_words),
    }
    df = pd.DataFrame([row])
    df.to_csv(csv_file, mode="a", index=False, header=not os.path.exists(csv_file))

class AddView:
    def __init__(self, root, films, csv_file, back_callback):
        self.root = root
        self.films = films
        self.csv_file = csv_file
        self.back_callback = back_callback

        # główny frame
        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Dodaj nowy film").pack(pady=10)

        self.entry_name = self.make_labeled_entry("Tytuł:")
        self.entry_author = self.make_labeled_entry("Autor:")
        self.entry_year = self.make_labeled_entry("Rok:")
        self.entry_genre = self.make_labeled_entry("Gatunki (oddzielone ;):")
        self.entry_keywords = self.make_labeled_entry("Słowa kluczowe (oddzielone ;):")

        tk.Button(self.frame, text="Zapisz", command=self.add_film).pack(pady=10)
        tk.Button(self.frame, text="Wróć", command=self.back_callback).pack()

    def make_labeled_entry(self, label):
        tk.Label(self.frame, text=label).pack()
        entry = tk.Entry(self.frame, width=50)
        entry.pack()
        return entry

    def add_film(self):
        try:
            name = self.entry_name.get().strip()
            author = self.entry_author.get().strip()
            year = int(self.entry_year.get().strip())
            genre = [g.strip() for g in self.entry_genre.get().split(";") if g.strip()]
            keywords = [k.strip() for k in self.entry_keywords.get().split(";") if k.strip()]

            if not name or not author:
                raise ValueError("Brak wymaganych danych")

            film = Film(name, author, year, genre, keywords)
            self.films.append(film)
            save_film_to_csv(film, self.csv_file)

            messagebox.showinfo("Sukces", "Film dodany!")
            self.back_callback()  # wróć po zapisaniu
        except Exception as e:
            messagebox.showerror("Błąd", str(e))
