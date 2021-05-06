from __future__ import annotations
from sqlite3 import Connection, connect, ProgrammingError
from dataclasses import dataclass
from typing import Optional, NoReturn


@dataclass
class User:
    user_id: int
    username: str
    password: str

    def rate_anime(self, conn: Connection, anime_id: int, score: int) -> NoReturn:
        query = 'INSERT INTO UserAnime(user_id, anime_id, score) VALUES (?,?,?)'
        with conn:
            conn.execute(query, (self.user_id, anime_id, score))

    def unrate_anime(self, conn: Connection, anime_id: int) -> NoReturn:
        query = 'DELETE FROM UserAnime WHERE user_id=? AND anime_id=?'
        with conn:
            conn.execute(query, (self.user_id, anime_id))

    def change_username(self, conn: Connection, new_username: str) -> NoReturn:
        query = 'UPDATE User SET username = ? WHERE id = ?'
        with conn:
            conn.execute(query, (new_username, self.user_id))
            self.username = new_username

    def change_password(self, conn: Connection, new_password: str) -> NoReturn:
        query = 'UPDATE User SET password = ? WHERE id = ?'
        with conn:
            conn.execute(query, (self.password, self.user_id))
            self.password = new_password

    @staticmethod
    def create(conn: Connection, username: str, password: str) -> NoReturn:
        query = 'INSERT INTO User(username, password) VALUES(?, ?)'
        with conn:
            conn.execute(query, (username, password))

    @staticmethod
    def from_id(conn: Connection, user_id: int) -> Optional[User]:
        query = 'SELECT * from User WHERE id=?'
        if data := conn.execute(query, (user_id,)).fetchone():
            return User(*data)

    @staticmethod
    def from_username(conn: Connection, username: str) -> Optional[User]:
        query = 'SELECT * from User WHERE username=?'
        if data := conn.execute(query, (username,)).fetchone():
            return User(*data)
