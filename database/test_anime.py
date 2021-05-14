import unittest
from .anime import Anime
from .helper import initialize_database
from sqlite3 import Connection, connect, IntegrityError


class TestAnime(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.conn: Connection = connect(':memory:')
        initialize_database(cls.conn)

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def setUp(self):
        animes = [(1, 'Cowboy Bebop'),
                  (2, 'Cowboy Bebop: Tengoku no Tobira'), (3, 'Trigun')]
        genres = [(1, 'Action'), (2, 'Adventure'),
                  (3, 'Comedy'), (4, 'Sci-Fi'), (5, 'Shounen')]
        anime_genres = [(1, 1), (1, 2), (1, 3), (2, 1),
                        (2, 2), (2, 4), (3, 1), (3, 2), (3, 5)]

        em = TestAnime.conn.executemany
        em('INSERT INTO Anime(anime_id, title) VALUES(?, ?)', animes)
        em('INSERT INTO Genre(genre_id, name) VALUES(?, ?)', genres)
        em('INSERT INTO AnimeGenre(anime_id, genre_id) VALUES(?, ?)', anime_genres)

    def tearDown(self):
        TestAnime.conn.executescript("""
            DELETE FROM AnimeGenre;
            DELETE FROM Genre;
            DELETE FROM Anime;
        """)

    def test_search(self):
        # test pagination
        conn = TestAnime.conn
        self.assertEqual(len(Anime.search(conn, limit=1, page=2)), 1)
        self.assertEqual(len(Anime.search(conn, limit=1, page=1)), 1)
        self.assertEqual(len(Anime.search(conn, limit=2, page=1)), 2)
        self.assertEqual(len(Anime.search(conn, limit=2, page=2)), 1)

        # test title searching
        self.assertEqual(len(Anime.search(conn, title='cowboy')), 2)

        # test genre inclusion and exclusion
        self.assertEqual(len(Anime.search(conn, include_genres=[1])), 3)
        ActionAdventureComedy = Anime.search(conn, include_genres=[1, 2, 3])
        self.assertEqual(len(ActionAdventureComedy), 1)
        self.assertEqual(ActionAdventureComedy[0].title, 'Cowboy Bebop')
        self.assertEqual(len(Anime.search(conn, exclude_genres=[1])), 0)
        self.assertEqual(len(Anime.search(conn, exclude_genres=[5])), 2)
        self.assertEqual(
            len(Anime.search(conn, include_genres=[4], exclude_genres=[5])), 1)

    def test_create(self):
        conn = TestAnime.conn
        TVversion = Anime('Run Ronald', 'TV')
        Movieversion = Anime('Run Ronald', 'Movie')

        Anime.create(conn, TVversion)
        self.assertEqual(len(Anime.search(conn, title='Run Ronald')), 1)

        Anime.create(conn, Movieversion)
        self.assertEqual(len(Anime.search(conn, title='Run Ronald')), 2)

        with self.assertRaises(IntegrityError):
            Anime.create(conn, TVversion)

    def test_from_id(self):
        conn = TestAnime.conn
        NonExistentAnime = Anime.from_id(conn, 0)
        Bebop1 = Anime.from_id(conn, 1)

        self.assertIsNone(NonExistentAnime)
        self.assertEqual(Bebop1.title, 'Cowboy Bebop')

    def test_update(self):
        conn = TestAnime.conn
        Trigun = Anime.from_id(conn, 3)
        Trigun.update(conn, anime_type='Heave Ho')
        self.assertEqual(Trigun.anime_type, 'Heave Ho')

        with self.assertRaises(IntegrityError):
            Trigun.update(conn, anime_id=10)

    def test_get_genres(self):
        conn = TestAnime.conn
        Trigun = Anime.from_id(conn, 3)
        self.assertCountEqual(Trigun.get_genres(conn), (1, 2, 5))

    def test_set_genres(self):
        conn = TestAnime.conn
        Trigun = Anime.from_id(conn, 3)
        Trigun.set_genres(conn, [1, 3, 5])
        self.assertCountEqual(Trigun.get_genres(conn), (1, 3, 5))


if __name__ == '__main__':
    unittest.main()
