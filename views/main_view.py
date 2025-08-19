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
        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        # --- układ lewo-prawo ---
        top_frame = tk.Frame(self.frame)
        top_frame.pack(fill="both", expand=True, pady=10)

        # Lewa część (film 1)
        left_frame = tk.Frame(top_frame)
        left_frame.pack(side="left", padx=20, fill="y")

        tk.Label(left_frame, text="Film 1:").pack()
        self.search1 = tk.Entry(left_frame, width=40)
        self.search1.pack()
        self.search1.bind("<KeyRelease>", lambda e: self.update_listbox(self.search1, self.listbox1))

        self.listbox1 = tk.Listbox(left_frame, width=40, height=15,
                                   selectmode=tk.SINGLE, exportselection=False)
        self.listbox1.pack(pady=5)

        # Prawa część (film 2)
        right_frame = tk.Frame(top_frame)
        right_frame.pack(side="right", padx=20, fill="y")

        tk.Label(right_frame, text="Film 2:").pack()
        self.search2 = tk.Entry(right_frame, width=40)
        self.search2.pack()
        self.search2.bind("<KeyRelease>", lambda e: self.update_listbox(self.search2, self.listbox2))

        self.listbox2 = tk.Listbox(right_frame, width=40, height=15,
                                   selectmode=tk.SINGLE, exportselection=False)
        self.listbox2.pack(pady=5)

        # Guziki pod spodem
        tk.Button(self.frame, text="Pokaż rekomendacje", command=self.show_recommendations).pack(pady=5)
        tk.Button(self.frame, text="Wróć", command=self.back_callback).pack(pady=5)

        # Wyniki
        self.result = tk.Frame(self.frame)
        self.result.pack(fill="both", expand=True, pady=10)

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

        tk.Label(self.result, text=f"Wybrane filmy:\n - {film1}\n - {film2}", 
                    font=("Arial", 10)).pack(anchor="w", pady=5)

        tk.Label(self.result, text="Proponowane filmy:", 
                    font=("Arial", 12, "bold")).pack(anchor="w", pady=5)

        for score, f in top_recs:
            row = tk.Frame(self.result)
            row.pack(fill="x", pady=2)

            # opis filmu
            tk.Label(row, text=f"{f.name} ({f.year})", width=50, anchor="w").pack(side="left")

            # guziki akcji jako przełączniki
            def make_toggle(flag_name, film, btn):
                def toggle():
                    current = getattr(film, flag_name)
                    setattr(film, flag_name, 0 if current else 1)
                    btn.config(bg="lightpink" if getattr(film, flag_name) else "SystemButtonFace")
                    self.update_csv(film)
                return toggle

            btn_to_watch = tk.Button(row, text="Do obejrzenia",
                                    bg="lightpink" if f.to_watch else "SystemButtonFace")
            btn_to_watch.config(command=make_toggle("to_watch", f, btn_to_watch))
            btn_to_watch.pack(side="left", padx=5)

            btn_watched = tk.Button(row, text="Obejrzany",
                                    bg="lightpink" if f.watched else "SystemButtonFace")
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

