from __future__ import annotations
from sqlite3 import Connection, connect
from datetime import date
from dataclasses import dataclass, asdict
from typing import Optional, NoReturn


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

    def update(self, conn: Connection, **kwargs):
        values = kwargs | {'id': self.anime_id}
        columns = ','.join(map(make_set_string, kwargs.keys()))
        query = f'UPDATE Anime SET {columns} WHERE anime_id=:id'
        with conn:
            conn.execute(query, values)
            for key, val in kwargs.items():
                setattr(self, key, val)

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
    def search(conn: Connection, title: str, limit: int = -1, page: int = 1) -> list[Anime]:
        query = 'SELECT * from Anime WHERE title LIKE ? LIMIT ? OFFSET ?'
        offset = limit * (page - 1)
        return list(
            map(lambda x: Anime(*x), conn.execute(query, (f'%{title}%', limit, offset))))


def make_set_string(string: str):
    return f'{string}=:{string}'
