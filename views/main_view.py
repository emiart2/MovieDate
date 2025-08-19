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
        self.result = tk.Text(self.frame, height=10, width=90)
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

        self.result.delete(1.0, tk.END)
        self.result.insert(tk.END, f"Wybrane filmy:\n - {film1}\n - {film2}\n\n")
        self.result.insert(tk.END, "Proponowane filmy:\n")
        for score, f in top_recs:
            self.result.insert(tk.END, f"{f.name} ({f.year}) — {score:.1f}% podobieństwa\n")
