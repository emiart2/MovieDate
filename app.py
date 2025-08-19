import tkinter as tk
from views.menu_view import MenuView
from models.data_manager import load_films

CSV_FILE = "data/data_all_fixed_robust.csv"

if __name__ == "__main__":
    root = tk.Tk()
    root.title("MovieDate")
    root.geometry("700x700")

    films = load_films(CSV_FILE)

    app = MenuView(root, films, CSV_FILE)
    root.mainloop()


