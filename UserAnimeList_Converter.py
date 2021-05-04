import sqlite3, csv

connection = sqlite3.connect("ANIME.db")
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS UserAnime")
cursor.execute("""CREATE TABLE UserAnime(
    user_id int,
    anime_id int,
    score int
);""")

cursor.execute("SELECT username, id FROM User");
name_id_map = dict(cursor.fetchall())

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
            "INSERT INTO UserAnime VALUES (?,?,?)",
            (name_id_map[username], anime_id, my_score)
        )
    
    # some anime ratings by users contains a score of zero
    # can happen if they added a status (like plan to watch)
    # while not adding a rating. 
    cursor.execute("DELETE FROM UserAnime WHERE score=0")

connection.commit()
connection.close()
