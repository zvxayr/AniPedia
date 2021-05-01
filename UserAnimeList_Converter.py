import sqlite3, csv

connection = sqlite3.connect("ANIME.db")
cursor = connection.cursor()

cursor.execute("""DROP TABLE UserAnime""")
cursor.execute("""CREATE TABLE IF NOT EXISTS UserAnime(
    Username text,
    anime_id int,
    my_score int
);""")

with open('UserAnimeList.csv', 'r', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar= '"')
    next(spamreader)
    for row in spamreader:
        (Username,
        anime_id,
        my_watch,
        my_start_date,
        my_finish_date
        ,my_score,
        my_status,
        my_rewatching,
        my_rewatching_ep,
        my_last_updated,
        my_tags) = row
        cursor.execute("""INSERT INTO UserAnime 
        VALUES (?,?,?)""", [Username, anime_id, my_score])

connection.commit()
connection.close()