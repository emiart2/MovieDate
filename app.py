import tkinter as tk
from tkinter import messagebox
import pandas as pd
from Film import Film
import re
import os

CSV_FILE = "data/data_all_fixed_robust.csv"

def load_films(csv_file):
    if not os.path.exists(csv_file):
        return []
    df = pd.read_csv(csv_file)
    films = []
    for _, row in df.iterrows():
        genre_val = row.at["genre"]
        key_words_val = row.at["key_words"]
        genre = str(genre_val).split(";") if isinstance(genre_val, str) and genre_val else []
        key_words = str(key_words_val).split(";") if isinstance(key_words_val, str) and key_words_val else []

        year_str = str(row.at["year"]) if "year" in row else ""
        m = re.search(r"\b(19|20)\d{2}\b", year_str)
        if not m:
            continue
        year_int = int(m.group(0))

        films.append(Film(str(row["name"]).strip(), str(row["author"]).strip(), year_int, genre, key_words))
    return films

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


class FilmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MovieDate")
        self.root.geometry("800x500")

        self.films = load_films(CSV_FILE)
        self.film_dict = {f.name: f for f in self.films}

        # --- ekrany ---
        self.main_frame = tk.Frame(root)
        self.add_frame = tk.Frame(root)

        self.build_main_frame()
        self.build_add_frame()

        tk.Button(self.root, text="≡", command=self.toggle_side_menu).place(x=5, y=5)
        self.build_side_menu()


        self.show_main()

    def build_main_frame(self):
        frame = self.main_frame

        # --- układ lewo-prawo ---
        top_frame = tk.Frame(frame)
        top_frame.pack(fill="both", expand=True, pady=10)

        # Lewa część (film 1)
        left_frame = tk.Frame(top_frame)
        left_frame.pack(side="left", padx=20, fill="y")

        tk.Label(left_frame, text="Film 1:").pack()
        self.search1 = tk.Entry(left_frame, width=40)
        self.search1.pack()
        self.search1.bind("<KeyRelease>", lambda e: self.update_listbox(self.search1, self.listbox1))

        self.listbox1 = tk.Listbox(left_frame, width=40, height=15, selectmode=tk.SINGLE, exportselection=False)


        self.listbox1.pack(pady=5)

        # Prawa część (film 2)
        right_frame = tk.Frame(top_frame)
        right_frame.pack(side="right", padx=20, fill="y")

        tk.Label(right_frame, text="Film 2:").pack()
        self.search2 = tk.Entry(right_frame, width=40)
        self.search2.pack()
        self.search2.bind("<KeyRelease>", lambda e: self.update_listbox(self.search2, self.listbox2))

        self.listbox2 = tk.Listbox(right_frame, width=40, height=15, selectmode=tk.SINGLE, exportselection=False)
        self.listbox2.pack(pady=5)

        # Guzik pod spodem
        tk.Button(frame, text="Pokaż rekomendacje", command=self.show_recommendations).pack(pady=5)
 

        for f in self.films:
            self.listbox1.insert(tk.END, f.name)
            self.listbox2.insert(tk.END, f.name)


        # Wyniki (tylko to zostaje na dole)
        self.result = tk.Text(frame, height=10, width=90)
        self.result.pack(pady=10)

    def build_add_frame(self):
        frame = self.add_frame

        tk.Label(frame, text="Dodaj nowy film").pack(pady=10)

        self.entry_name = self.make_labeled_entry(frame, "Tytuł:")
        self.entry_author = self.make_labeled_entry(frame, "Autor:")
        self.entry_year = self.make_labeled_entry(frame, "Rok:")
        self.entry_genre = self.make_labeled_entry(frame, "Gatunki (oddzielone ;):")
        self.entry_keywords = self.make_labeled_entry(frame, "Słowa kluczowe (oddzielone ;):")

        tk.Button(frame, text="Zapisz", command=self.add_film).pack(pady=10)
        tk.Button(frame, text="Wróć", command=self.show_main).pack()

    def make_labeled_entry(self, parent, label):
        tk.Label(parent, text=label).pack()
        entry = tk.Entry(parent, width=50)
        entry.pack()
        return entry

    def update_listbox(self, entry, listbox):
        query = entry.get().lower()
        listbox.delete(0, tk.END)
        for f in self.films:
            if query in f.name.lower() or query in f.author.lower():
                listbox.insert(tk.END, f.name)

    def show_recommendations(self):
        if not self.listbox1.curselection() or not self.listbox2.curselection():
            messagebox.showwarning("Błąd", "Wybierz po jednym filmie z każdej listy!")
            return

        film1_name = self.listbox1.get(self.listbox1.curselection()[0])
        film2_name = self.listbox2.get(self.listbox2.curselection()[0])
        film1, film2 = self.film_dict[film1_name], self.film_dict[film2_name]

        scores = []
        for f in self.films:
            if f not in (film1, film2):
                score = (f.metric(film1) + f.metric(film2)) / 2
                scores.append((score, f))
        scores.sort(reverse=True, key=lambda x: x[0])
        top_recs = scores[:5]

        self.result.delete(1.0, tk.END)
        self.result.insert(tk.END, f"Wybrane filmy:\n - {film1}\n - {film2}\n\n")
        self.result.insert(tk.END, "Proponowane filmy:\n")
        for score, f in top_recs:
            self.result.insert(tk.END, f"{f.name} ({f.year}) — {score:.1f}% podobieństwa\n")

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
            self.film_dict[film.name] = film
            save_film_to_csv(film, CSV_FILE)

            messagebox.showinfo("Sukces", "Film dodany!")
            self.show_main()
        except Exception as e:
            messagebox.showerror("Błąd", str(e))

    def show_main(self):
        self.add_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)

    def show_add(self):
        self.main_frame.pack_forget()
        self.add_frame.pack(fill="both", expand=True)
    
    def show_database(self):
        win = tk.Toplevel(self.root)
        win.title("Baza filmów")
        text = tk.Text(win, width=80, height=30)
        text.pack()
        for f in self.films:
            text.insert(tk.END, f"{f.name} ({f.year}) - {f.author}\n")

    def toggle_side_menu(self):
        if self.side_menu.winfo_ismapped():
            self.side_menu.place_forget()
        else:
            self.side_menu.place(x=0, y=30, width=200, height=200)


    def build_side_menu(self):
        self.side_menu = tk.Frame(self.root, bg="lightgray", width=200)
        tk.Button(self.side_menu, text="Dodaj film", command=self.show_add).pack(pady=5)
        tk.Button(self.side_menu, text="Pokaż bazę", command=self.show_database).pack(pady=5)
        tk.Button(self.side_menu, text="Zamknij", command=self.toggle_side_menu).pack(pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = FilmApp(root)
    root.mainloop()


