import pandas as pd
from models.Film import Film
import re
import os

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

        #default settings
        to_watch = int(row.get("to_watch", 0))
        watched = int(row.get("watched", 0))

        films.append(Film(str(row["name"]).strip(), str(row["author"]).strip(), year_int, genre, key_words, to_watch, watched))
    return films

def save_film_to_csv(film: Film, csv_file: str):
    row = {
        "name": film.name,
        "author": film.author,
        "year": film.year,
        "genre": ";".join(film.genre),
        "key_words": ";".join(film.key_words),
        "to_watch": film.to_watch,
        "watched": film.watched,
    }
    df = pd.DataFrame([row])
    df.to_csv(csv_file, mode="a", index=False, header=not os.path.exists(csv_file))

