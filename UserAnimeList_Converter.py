import sqlite3, csv

connection = sqlite3.connect("ANIME.db")
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS UserAnime")
cursor.execute("""CREATE TABLE UserAnime(
    user_id int,
    anime_id int,
    score int
);""")

with open('UserAnimeList.csv', 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar= '"')
    next(csvreader)
    for row in csvreader:
        (username,
        anime_id,
        my_watch,
        my_start_date,
        my_finish_date,
        my_score,
        my_status,
        my_rewatching,
        my_rewatching_ep,
        my_last_updated,
        my_tags) = row
        cursor.execute(
            """INSERT INTO UserAnime (user_id, anime_id, score)
               SELECT id, ?, ? FROM User
               WHERE username = ?;""",
            (anime_id, my_score, username)
        )

connection.commit()
connection.close()
