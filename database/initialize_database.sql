PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Anime(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    type TEXT,
    aired_from DATE, 
    aired_to DATE,
    rating TEXT,
    premiered TEXT,
    studio TEXT
);

CREATE TABLE IF NOT EXISTS Genre(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    ui_theme TEXT
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
