import sqlite3, csv

connection = sqlite3.connect("ANIME.db")
cursor = connection.cursor()

cursor.execute("""DROP TABLE IF EXISTS User;""")
cursor.execute("""CREATE TABLE IF NOT EXISTS User(
    username text
);""")

with open('UserList.csv', 'r', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar= '"')
    next(spamreader) # first row on the csv file contains the column names
    
    for row in spamreader:
        (username,
        user_id,
        user_watching,
        user_completed,
        user_onhold,
        user_dropped,
        user_plantowatch,
        user_days_spent_watching,
        gender,
        location,
        birth_date,
        access_rank,
        join_date,
        last_online,
        stats_mean_score,
        stats_rewatched,
        stats_episodes) = row
        cursor.execute("INSERT INTO User VALUES (?);", [username])

connection.commit()
connection.close()