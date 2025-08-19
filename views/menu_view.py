import tkinter as tk
from views.main_view import MainView
from views.add_view import AddView
from views.database_view import DatabaseView
from PIL import Image, ImageTk

class MenuView:
    def __init__(self, root, films, csv_file):
        self.root = root
        self.root.geometry("700x700")
        self.films = films
        self.csv_file = csv_file

        # --- przechowujemy referencję do obrazu ---
        self.bg_image = Image.open("graphic/menu.png")
        self.bg_image = self.bg_image.resize((700, 700))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # --- Label z tłem ---
        self.bg_label = tk.Label(root, image=self.bg_photo, bg="#fbffae")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # --- Frame na przyciski ---
        self.frame = tk.Frame(root, bg="#fbffae", bd=0)
        self.frame.pack(side="bottom", pady=40)

        # szeroki przycisk – dwa razy szerszy niż dolne razem
        btn_choose = tk.Button(self.frame, text="Wybierz film!",
                            bg="#ffaade", fg="white", font=("Arial", 14),
                            height=2,
                            width=30,  # <-- szerokość w "znakach"
                            command=lambda: self.show(MainView))
        btn_choose.pack(pady=(0, 15))  # odstęp w dół

        # drugi wiersz – ramka wyśrodkowana
        bottom_frame = tk.Frame(self.frame, bg="#fbffae")
        bottom_frame.pack()

        btn_add = tk.Button(bottom_frame, text="Dodaj nowy film",
                            bg="#ffaade", fg="white", font=("Arial", 14),
                            width=14, height=2,
                            command=lambda: self.show(AddView))
        btn_add.pack(side="left", padx=10)

        btn_db = tk.Button(bottom_frame, text="Przeglądaj bazę",
                        bg="#ffaade", fg="white", font=("Arial", 14),
                        width=14, height=2,
                        command=lambda: self.show(DatabaseView))
        btn_db.pack(side="left", padx=10)



    def show(self, ViewClass):
        for widget in self.root.winfo_children():
            widget.destroy()
        ViewClass(self.root, self.films, self.csv_file, self.back_to_menu)


    def back_to_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        MenuView(self.root, self.films, self.csv_file)
