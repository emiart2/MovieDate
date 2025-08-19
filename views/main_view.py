import tkinter as tk
from tkinter import messagebox

class MainView:
    def __init__(self, root, films, csv_file, back_callback):
        self.root = root
        self.films = films
        self.film_dict = {f.name: f for f in self.films}
        self.csv_file = csv_file
        self.back_callback = back_callback

        # --- główny frame ---
        self.frame = tk.Frame(root, bg="#fbffae")
        self.frame.pack(fill="both", expand=True)
        tk.Label(
            self.frame, 
            text="Wybierzcie swoje filmy!", 
            font=("Arial", 30, "bold"),
            bg="#fbffae",   # kolor tła
            fg="#ffaade"    # kolor czcionki
        ).pack(pady=10)

        # --- układ lewo-prawo (top_frame) ---
        top_frame = tk.Frame(self.frame, bg="#fbffae")
        top_frame.pack(pady=10)

        # Lewa część (film 1)
        left_frame = tk.Frame(top_frame, bg="#fbffae")
        left_frame.pack(side="left", padx=10)  # zmniejszone padx
        self.search1 = tk.Entry(left_frame, width=35)
        self.search1.pack(pady=2)
        self.search1.bind("<KeyRelease>", lambda e: self.update_listbox(self.search1, self.listbox1))
        self.listbox1 = tk.Listbox(left_frame, width=35, height=15, selectmode=tk.SINGLE, exportselection=False)
        self.listbox1.pack(pady=2)

        # Prawa część (film 2)
        right_frame = tk.Frame(top_frame, bg="#fbffae")
        right_frame.pack(side="left", padx=10)  # zmniejszone padx
        self.search2 = tk.Entry(right_frame, width=35)
        self.search2.pack(pady=2)
        self.search2.bind("<KeyRelease>", lambda e: self.update_listbox(self.search2, self.listbox2))
        self.listbox2 = tk.Listbox(right_frame, width=35, height=15, selectmode=tk.SINGLE, exportselection=False)
        self.listbox2.pack(pady=2)

        # Wypełnij listy
        for f in self.films:
            self.listbox1.insert(tk.END, f.name)
            self.listbox2.insert(tk.END, f.name)

        # Guziki pod spodem, wyśrodkowane
        btn_frame = tk.Frame(self.frame, bg="#fbffae")
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Pokaż rekomendacje", bg="#ffaade", fg="white", font=("Arial", 10), height=2, width=30,
                command=self.show_recommendations).pack(pady=2)
        tk.Button(btn_frame, text="Wróć", bg="#ffaade", fg="white", font=("Arial", 10), height=2, width=30,
                command=self.back_callback).pack(pady=2)

        # Wyniki – wyśrodkowane
        self.result = tk.Frame(self.frame, bg="#fbffae")
        self.result.pack(pady=10)

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

        # destroy old view
        for widget in self.result.winfo_children():
            widget.destroy()

        tk.Label(self.result, text="Proponowane filmy:", 
                    font=("Arial", 12, "bold"), bg="#fbffae", fg="#545454").pack(anchor="w", pady=5)

        for score, f in top_recs:
            row = tk.Frame(self.result, bg="#fbffae")
            row.pack(fill="x", pady=2)

            # opis filmu
            tk.Label(row, text=f"{f.name} ({f.year})", width=50, anchor="w", bg="#fbffae", fg="#545454").pack(side="left")

            # guziki akcji jako przełączniki
            def make_toggle(flag_name, film, btn):
                def toggle():
                    current = getattr(film, flag_name)
                    setattr(film, flag_name, 0 if current else 1)
                    btn.config(bg="#ffaade" if getattr(film, flag_name) else "white")
                    self.update_csv(film)
                return toggle

            btn_to_watch = tk.Button(row, text="Do obejrzenia",
                                    bg="#ffaade" if f.to_watch else "white")
            btn_to_watch.config(command=make_toggle("to_watch", f, btn_to_watch))
            btn_to_watch.pack(side="left", padx=5)

            btn_watched = tk.Button(row, text="Obejrzany",
                                    bg="#ffaade" if f.watched else "white")
            btn_watched.config(command=make_toggle("watched", f, btn_watched))
            btn_watched.pack(side="left", padx=5)

    def set_flag(self, film, to_watch=None, watched=None):
        if to_watch is not None:
            film.to_watch = to_watch
        if watched is not None:
            film.watched = watched

        # od razu zapisz do CSV
        self.update_csv(film)

    def update_csv(self, film):
        import pandas as pd
        df = pd.read_csv(self.csv_file)

        # znajdź po nazwie i roku (lub czymś unikalnym)
        mask = (df["name"] == film.name) & (df["year"] == film.year)
        if mask.any():
            if "to_watch" in df.columns:
                df.loc[mask, "to_watch"] = film.to_watch
            if "watched" in df.columns:
                df.loc[mask, "watched"] = film.watched
            df.to_csv(self.csv_file, index=False)

