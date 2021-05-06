import unittest
from user import User
from helper import initialize_database
from sqlite3 import Connection, connect, IntegrityError, ProgrammingError
from typing import Optional
from os import path


class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.conn: Connection = connect(':memory:')
        initialize_database(cls.conn)

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def setUp(self):
        users = [(1, 'Andrew'), (2, 'Vince')]
        animes = [(1, "Wolf's Rain"), (2, 'Perfect Blue')]
        ratings = [(1, 1, 8), (1, 2, 9), (2, 1, 10)]

        em = TestUser.conn.executemany
        em('INSERT INTO User(id, username, password) VALUES(?, ?, "")', users)
        em('INSERT INTO Anime(id, title) VALUES(?, ?)', animes)
        em('INSERT INTO UserAnime VALUES(?, ?, ?)', ratings)

    def tearDown(self):
        TestUser.conn.executescript("""
            DELETE FROM UserAnime;
            DELETE FROM User;
            DELETE FROM Anime;
        """)

    def test_create(self):
        User.create(TestUser.conn, User('Miles', ''))
        Miles = User.from_username(TestUser.conn, 'Miles')
        self.assertEqual(Miles.username, 'Miles')

        # creating user with existing username
        with self.assertRaises(IntegrityError):
            User.create(TestUser.conn, User('Vince', ''))

    def test_from_id(self):
        NonExistentUser = User.from_id(TestUser.conn, 0)
        Andrew = User.from_id(TestUser.conn, 1)

        self.assertIsNone(NonExistentUser)
        self.assertEqual(Andrew.username, 'Andrew')

    def test_from_username(self):
        NonExistentUser = User.from_username(TestUser.conn, 'Samantha')
        Andrew = User.from_username(TestUser.conn, 'Andrew')

        self.assertIsNone(NonExistentUser)
        self.assertEqual(Andrew.user_id, 1)

    def test_rate_anime(self):
        Vince = User.from_username(TestUser.conn, 'Vince')

        # rating new anime
        Vince.rate_anime(TestUser.conn, 2, 9)
        self.assertEqual(get_rating(TestUser.conn, Vince.user_id, 2), 9)

        # updating old rating
        Vince.rate_anime(TestUser.conn, 1, 9)
        self.assertEqual(get_rating(TestUser.conn, Vince.user_id, 1), 9)

        # rating nonexistent anime
        with self.assertRaises(IntegrityError):
            Vince.rate_anime(TestUser.conn, 3, 10)

    def test_unrate_anime(self):
        Vince = User.from_username(TestUser.conn, 'Vince')
        Vince.unrate_anime(TestUser.conn, 1)

        self.assertIsNone(get_rating(TestUser.conn, Vince.user_id, 1))

    def test_change_username(self):
        Vince = User.from_username(TestUser.conn, 'Vince')

        Vince.change_username(TestUser.conn, 'Vincent')
        self.assertEqual(Vince.username, 'Vincent')

        with self.assertRaises(IntegrityError):
            Vince.change_username(TestUser.conn, 'Andrew')

    def test_change_password(self):
        Andrew = User.from_username(TestUser.conn, 'Andrew')
        Andrew.change_password(TestUser.conn, 'new_password')

        self.assertEqual(Andrew.password, 'new_password')


def get_rating(conn: Connection, user_id: int, anime_id: int) -> Optional[int]:
    query = 'SELECT score FROM UserAnime where user_id=? AND anime_id=?'
    if data := conn.execute(query, (user_id, anime_id)).fetchone():
        return data[0]


if __name__ == '__main__':
    unittest.main()
