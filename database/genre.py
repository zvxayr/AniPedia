from __future__ import annotations
from sqlite3 import Connection, connect
from dataclasses import dataclass, asdict
from typing import Optional, NoReturn


@dataclass
class Genre:
    name: str
    genre_id: int = None

    @staticmethod
    def create(conn: Connection, genre: Genre) -> NoReturn:
        query = 'INSERT INTO Genre(name) VALUES(?)'
        with conn:
            conn.execute(query, (genre.name,))

    @staticmethod
    def from_id(conn: Connection, genre_id: int) -> Optional[Genre]:
        query = f'SELECT * FROM Genre WHERE genre_id=?'
        if data := conn.execute(query, (genre_id,)).fetchone():
            return Genre(*data)

    @staticmethod
    def all(conn: Connection) -> list[Genre]:
        query = 'SELECT * FROM Genre'
        return [Genre(*x) for x in conn.execute(query)]
