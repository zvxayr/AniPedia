import sqlite3, csv, json

connection = sqlite3.connect("ANIME.db")
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS AnimeList")
cursor.execute("DROP TABLE IF EXISTS Genre")
cursor.execute("DROP TABLE IF EXISTS AnimeGenre")

cursor.execute("""CREATE TABLE AnimeList(
    anime_id int,
    title text,
    typeOfAnime text,
    aired_from text, 
    aired_to text,
    rating text, 
    score double, 
    premiered text);""")

cursor.execute("""CREATE TABLE Genre(
    genre_id int,
    name text);""")

cursor.execute("""CREATE TABLE AnimeGenre(
    anime_id int,
    genre_id int);""")

with open('AnimeList.csv', 'r', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar= '"')
    next(spamreader)
    genre_map = {}
    for row in spamreader:
        (anime_id,
        title,
        title_english,
        title_japan,
        title_synonyms,
        image_url, 
        typeOfAnime,
        source,
        episodes, 
        status, 
        airing, 
        aired_string,
        aired, 
        duration, 
        rating, 
        score, 
        scored_by,
        rank, 
        popularity, 
        members,
        favorites, 
        background,
        premiered, 
        broadcast, 
        related, 
        producer, 
        licensor,
        studio, 
        genre, 
        opening_theme,
        ending_theme) = row
        try:
            aired = json.loads(aired.replace("'", '"').replace("None", '""'))
            aired_from = aired["from"]
            aired_to = aired["to"]
        except:
            print(title)
            exit()

        genres = genre.split(", ")
        for g in genres:
            if not g: continue
            if g not in genre_map:
                genre_map[g] = len(genre_map)
                cursor.execute("""INSERT INTO Genre VALUES (?,?)""", [genre_map[g], g])
            cursor.execute("""INSERT INTO AnimeGenre VALUES (?,?)""", [anime_id, genre_map[g]])

        
        cursor.execute("""INSERT INTO AnimeList 
        VALUES (?,?,?,?,?,?,?,?)""", 
        [anime_id, title, typeOfAnime, aired_from, aired_to, rating, premiered, studio])
        

connection.commit()
connection.close()