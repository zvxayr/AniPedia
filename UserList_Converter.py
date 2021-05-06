import sqlite3, csv

connection = sqlite3.connect("ANIME.db")
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS User;")
cursor.execute("""CREATE TABLE User(
    id int,
    username text
);""")

with open('UserList.csv', 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar= '"')
    next(csvreader) # first row on the csv file contains the column names
    
    for row in csvreader:
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
        cursor.execute("INSERT INTO User VALUES (?,?);", (user_id, username))

cursor.execute("""ALTER TABLE User
        ADD pass_word VARCHAR(25)""")

connection.commit()
connection.close()