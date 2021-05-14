from __future__ import annotations
from sqlite3 import Connection, connect
from datetime import date
from dataclasses import dataclass, asdict
from typing import Optional, NoReturn
from itertools import chain

@dataclass
class Anime:
    title: str
    anime_type: str = 'Unknown'
    aired_from: Optional[date] = None
    aired_to: Optional[date] = None
    rating: str = ''
    premiered: str = ''
    studio: str = ''
    anime_id: Optional[int] = None

    def get_genres(self, conn: Connection) -> list[int]:
        query = """
        SELECT Genre.* FROM AnimeGenre
            LEFT JOIN Genre ON Genre.genre_id=AnimeGenre.genre_id
            WHERE anime_id=?
        """
        return tuple(Genre(*x) for x in conn.execute(query, (self.anime_id,)))

    def update(self, conn: Connection, **kwargs) -> NoReturn:
        values = kwargs | {'id': self.anime_id}
        columns = ','.join(map(make_set_string, kwargs.keys()))
        query = f'UPDATE Anime SET {columns} WHERE anime_id=:id'
        with conn:
            conn.execute(query, values)
            for key, val in kwargs.items():
                setattr(self, key, val)

    def set_genres(self, conn: Connection, genres: list[int]) -> NoReturn:
        delete_query = 'DELETE FROM AnimeGenre WHERE anime_id=?'
        insert_query = 'INSERT INTO AnimeGenre(anime_id, genre_id) VALUES(?,?)'
        with conn:
            conn.execute(delete_query, (self.anime_id,))
            conn.executemany(insert_query, map(
                lambda genre: (self.anime_id, genre), genres))

    @staticmethod
    def create(conn: Connection, anime: Anime) -> NoReturn:
        values = {k: v for k, v in asdict(anime).items() if v is not None}
        columns = ','.join(values.keys())
        labels = ','.join([f':{name}' for name in values.keys()])
        query = f'INSERT INTO Anime({columns}) VALUES({labels})'
        with conn:
            conn.execute(query, values)

    @staticmethod
    def from_id(conn: Connection, anime_id: int) -> Optional[Anime]:
        query = 'SELECT * from Anime WHERE anime_id=?'
        if data := conn.execute(query, (anime_id,)).fetchone():
            return Anime(*data)

    @staticmethod
    def from_title_and_type(conn: Connection,
                            title: str,
                            anime_type: str = 'Unknown'
                            ) -> Optional[Anime]:
        query = 'SELECT * from Anime WHERE title=? AND anime_type=?'
        if data := conn.execute(query, (title, anime_type)).fetchone():
            return Anime(*data)

    @staticmethod
    def search(conn: Connection, *,
               title: str = '',
               include_genres: list[int] = None,
               exclude_genres: list[int] = None,
               limit: int = -1, page: int = 1
               ) -> list[Anime]:
        include_genres = include_genres or []
        exclude_genres = exclude_genres or []
        query = f"""
            SELECT Anime.* FROM Anime
            LEFT JOIN AnimeGenre ON Anime.anime_id = AnimeGenre.anime_id
            GROUP BY Anime.anime_id
            HAVING title LIKE ?
                AND sum(AnimeGenre.genre_id IN ({','.join(['?'] * len(include_genres))})) = {len(include_genres)}
                AND min(AnimeGenre.genre_id not in ({','.join(['?'] * len(exclude_genres))}))
            LIMIT ?
            OFFSET ?
        """
        offset = limit * (page - 1)
        values = tuple(chain([f'%{title}%'], include_genres,
                       exclude_genres, [limit, offset]))
        result = conn.execute(query, values)
        return list(map(lambda x: Anime(*x), result))


def make_set_string(string: str):
    return f'{string}=:{string}'
