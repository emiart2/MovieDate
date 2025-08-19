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

        # --- główny frame z tłem ---
        self.frame = tk.Frame(root, bg="#fbffae")
        self.frame.pack(fill="both", expand=True)

        # Wyśrodkowanie w pionie
        self.inner_frame = tk.Frame(self.frame, bg="#fbffae")
        self.inner_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Tytuł
        tk.Label(
            self.inner_frame, 
            text="Dodaj nowy film", 
            font=("Arial", 14, "bold"), 
            fg="#545454", 
            bg="#fbffae"
        ).pack(pady=10)

        # Pola do wpisania danych z napisem nad Entry
        self.entry_name = self.make_labeled_entry("Tytuł:")
        self.entry_author = self.make_labeled_entry("Autor:")
        self.entry_year = self.make_labeled_entry("Rok:")
        self.entry_genre = self.make_labeled_entry("Gatunki (oddzielone ;):")
        self.entry_keywords = self.make_labeled_entry("Słowa kluczowe (oddzielone ;):")

        # Domyślne ustawienia
        self.var_to_watch = tk.IntVar()
        self.var_watched = tk.IntVar()

        tk.Checkbutton(
            self.inner_frame, 
            text="Do obejrzenia", 
            variable=self.var_to_watch,
            bg="#fbffae"
        ).pack(pady=2)

        tk.Checkbutton(
            self.inner_frame, 
            text="Obejrzany", 
            variable=self.var_watched,
            bg="#fbffae"
        ).pack(pady=2)

        # Guziki
        tk.Button(
            self.inner_frame, 
            text="Zapisz", 
            bg="#ffaade", fg="white", font=("Arial", 10), width=20,
            command=self.add_film
        ).pack(pady=5)

        tk.Button(
            self.inner_frame, 
            text="Wróć", 
            bg="#ffaade", fg="white", font=("Arial", 10), width=20,
            command=self.back_callback
        ).pack(pady=5)

    def make_labeled_entry(self, label_text):
        frame = tk.Frame(self.inner_frame, bg="#fbffae")
        frame.pack(pady=5, fill="x")
        tk.Label(frame, text=label_text, bg="#fbffae").pack(anchor="w")
        entry = tk.Entry(frame, width=40)
        entry.pack()
        return entry


    def add_film(self):
        try:
            name = self.entry_name.get().strip()
            author = self.entry_author.get().strip()
            year = int(self.entry_year.get().strip())
            genre = [g.strip() for g in self.entry_genre.get().split(";") if g.strip()]
            keywords = [k.strip() for k in self.entry_keywords.get().split(";") if k.strip()]

            #default settings
            film = Film(name, author, year, genre, keywords,
            self.var_to_watch.get(), self.var_watched.get())

            if not name or not author:
                raise ValueError("Brak wymaganych danych")

            film = Film(name, author, year, genre, keywords)
            self.films.append(film)
            save_film_to_csv(film, self.csv_file)

            messagebox.showinfo("Sukces", "Film dodany!")
            self.back_callback()  # wróć po zapisaniu
        except Exception as e:
            messagebox.showerror("Błąd", str(e))
