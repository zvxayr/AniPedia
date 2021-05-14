import csv
from sqlite3 import Connection
from .helper import initialize_database, foreign_key_checks_off


def clean_tables(conn: Connection):
    conn.executescript("""
        DROP TABLE IF EXISTS User;
    """)

    initialize_database(conn)


def convert_user_csv_to_db(conn: Connection, filename: str):
    clean_tables(conn)
    with open(filename, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(csvreader)  # first row on the csv file contains the column names

        with foreign_key_checks_off(conn):
            for row in csvreader:
                (username,
                 user_id,
                 user_watching,
                 user_completed,
                 user_onhold,
                 user_dropped,
                 user_plantowatch,
                 user_days_spent_watching,
                 gender,
                 location,
                 birth_date,
                 access_rank,
                 join_date,
                 last_online,
                 stats_mean_score,
                 stats_rewatched,
                 stats_episodes) = row

                try:
                    conn.execute(
                        'INSERT INTO User VALUES (?,"",NULL,?);', (username, user_id))
                except Exception:
                    pass


if __name__ == '__main__':
    from .helper import get_connection
    from config import dbpath

    with get_connection(dbpath) as conn:
        convert_user_csv_to_db(conn, 'UserList.csv')
