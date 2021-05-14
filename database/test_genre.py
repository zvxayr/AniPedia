import unittest
from .genre import Genre
from .helper import initialize_database
from sqlite3 import Connection, connect, IntegrityError


class TestGenre(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.conn: Connection = connect(':memory:')
        initialize_database(cls.conn)

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def setUp(self):
        genres = [(1, 'Action'), (2, 'Adventure'),
                  (3, 'Comedy'), (4, 'Sci-Fi'), (5, 'Shounen')]

        em = TestGenre.conn.executemany
        em('INSERT INTO Genre(genre_id, name) VALUES(?, ?)', genres)

    def tearDown(self):
        TestGenre.conn.executescript("""
            DELETE FROM Genre;
        """)

    def test_create(self):
        conn = TestGenre.conn

        Genre.create(conn, Genre('Shoujo'))
        Shoujo = conn.execute(
            'SELECT * FROM Genre WHERE name="Shoujo"').fetchone()
        self.assertIsNotNone(Shoujo)

    def test_from_id(self):
        conn = TestGenre.conn
        NonExistentGenre = Genre.from_id(conn, 0)
        Action = Genre.from_id(conn, 1)

        self.assertIsNone(NonExistentGenre)
        self.assertEqual(Action.name, 'Action')

    def test_all(self):
        genres = Genre.all(TestGenre.conn)
        self.assertEqual(len(genres), 5)


if __name__ == '__main__':
    unittest.main()
