PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Anime(
    title TEXT NOT NULL,
    type TEXT,
    aired_from DATE, 
    aired_to DATE,
    rating TEXT,
    premiered TEXT,
    studio TEXT,
    id INTEGER PRIMARY KEY AUTOINCREMENT
);

CREATE TABLE IF NOT EXISTS Genre(
    name TEXT UNIQUE,
    id INTEGER PRIMARY KEY AUTOINCREMENT
);

CREATE TABLE IF NOT EXISTS AnimeGenre(
    anime_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,

    CONSTRAINT fk_Anime
        FOREIGN KEY(anime_id)
        REFERENCES Anime(id)
        ON DELETE CASCADE
    
    CONSTRAINT fk_Genre
        FOREIGN KEY(genre_id)
        REFERENCES Genre(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS User(
    username TEXT UNIQUE,
    password TEXT,
    ui_theme TEXT,
    id INTEGER PRIMARY KEY AUTOINCREMENT
);

CREATE TABLE IF NOT EXISTS UserAnime(
    user_id INTEGER NOT NULL,
    anime_id INTEGER NOT NULL,
    score INTEGER,

    CONSTRAINT fk_User
        FOREIGN KEY(user_id)
        REFERENCES User(id)
        ON DELETE CASCADE

    CONSTRAINT fk_Anime
        FOREIGN KEY(anime_id)
        REFERENCES Anime(id)
        ON DELETE CASCADE

    UNIQUE(user_id, anime_id) ON CONFLICT REPLACE
);
