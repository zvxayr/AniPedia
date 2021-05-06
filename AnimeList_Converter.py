import sqlite3, csv, json

connection = sqlite3.connect("ANIME.db")
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS Anime")
cursor.execute("DROP TABLE IF EXISTS Genre")
cursor.execute("DROP TABLE IF EXISTS AnimeGenre")

cursor.execute("""CREATE TABLE Anime(
    id int,
    title text,
    typeOfAnime text,
    aired_from date, 
    aired_to date,
    rating text,  
    premiered text,
    studio text
);""")

cursor.execute("""CREATE TABLE Genre(
    genre_id int,
    name text
);""")

cursor.execute("""CREATE TABLE AnimeGenre(
    anime_id int,
    genre_id int
);""")

with open('AnimeList.csv', 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar= '"')
    next(csvreader)
    genre_map = {}
    for row in csvreader:
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
                cursor.execute("INSERT INTO Genre VALUES (?,?)", (genre_map[g], g))
            cursor.execute("INSERT INTO AnimeGenre VALUES (?,?)", (anime_id, genre_map[g]))

        cursor.execute(
            "INSERT INTO Anime VALUES (?,?,?,?,?,?,?,?)",
            (anime_id, title, typeOfAnime, aired_from, aired_to, rating, premiered, studio)
        )
        

connection.commit()
connection.close()