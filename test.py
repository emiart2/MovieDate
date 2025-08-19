import Film
import pandas as pd

data = pd.read_csv('data/data_international.csv', sep=',')
print(data.head())

def get_film_from_row(row):
    # Split genre and key_words by semicolon and strip whitespace
    genre = [g.strip() for g in str(row['genre']).split(';')]
    key_words = [k.strip() for k in str(row['key_words']).split(';')]
    return Film.Film(
        row['name'],
        row['author'],
        int(row['year']),
        genre,
        key_words
    )

film1 = get_film_from_row(data.iloc[3])
film2 = get_film_from_row(data.iloc[17])
print(film1.metric(film2))
print(film1.name, film2.name)
print(film1)
print(film2)






