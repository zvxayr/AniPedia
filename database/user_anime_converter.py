import csv
from sqlite3 import Connection
from helper import initialize_database, foreign_key_checks_off


def clean_tables(conn: Connection):
    conn.executescript("""
        DROP TABLE IF EXISTS UserAnime;
    """)

    initialize_database(conn)


def convert_user_anime_csv_to_db(conn: Connection, filename: str):
    clean_tables(conn)

    cursor = conn.execute('SELECT username, user_id FROM User')
    name_id_map = dict(cursor.fetchall())

    with foreign_key_checks_off(conn):
        with open('UserAnimeList.csv', 'r', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(csvreader)
            for row in csvreader:
                (username,
                 anime_id,
                 my_watch,
                 my_start_date,
                 my_finish_date,
                 my_score,
                 my_status,
                 my_rewatching,
                 my_rewatching_ep,
                 my_last_updated,
                 my_tags) = row

                try:
                    conn.execute(
                        'INSERT INTO UserAnime VALUES (?,?,?)',
                        (name_id_map[username], anime_id, my_score)
                    )
                except Exception:
                    pass

            # some anime ratings by users contains a score of zero
            # can happen if they added a status (like plan to watch)
            # while not adding a rating.
            conn.execute('DELETE FROM UserAnime WHERE score=0')


if __name__ == '__main__':
    from helper import get_connection
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

    import config
    conn = get_connection(config.dbpath)
    convert_user_anime_csv_to_db(conn, 'UserAnimeList.csv')
    conn.close()
