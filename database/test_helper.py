import unittest
from user import User
from helper import *
from sqlite3 import connect
from os import path


class TestHelper(unittest.TestCase):

    def test_is_connection_closed(self):
        conn = connect(':memory:')
        self.assertFalse(is_connection_closed(conn))
        conn.close()
        self.assertTrue(is_connection_closed(conn))

    def test_get_connection(self):
        conn = get_connection()
        self.assertIs(conn, get_connection())
        conn.close()
        self.assertIsNot(conn, get_connection())
        conn.close()

    def test_initialize_database(self):
        conn = connect(':memory:')
        initialize_database(conn)
        cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        self.assertGreater(len(cur.fetchall()), 0)
        conn.close()


if __name__ == '__main__':
    unittest.main()
