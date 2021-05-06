import csv
import json
from sqlite3 import Connection
from helper import initialize_database, foreign_key_checks_off
from datetime import datetime


def convert_date_string(datestring: str):
    return datetime.strptime(datestring, '%Y-%m-%d').date() if datestring else None


def clean_tables(conn: Connection):
    conn.executescript("""
        DROP TABLE IF EXISTS AnimeGenre;
        DROP TABLE IF EXISTS Anime;
        DROP TABLE IF EXISTS Genre;
    """)

    initialize_database(conn)


def convert_anime_csv_to_db(conn: Connection, filename: str):
    clean_tables(conn)
    with open(filename, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(csvreader)
        genre_map = {}

        with foreign_key_checks_off(conn):
            for row in csvreader:
                (anime_id,
                 title,
                 title_english,
                 title_japan,
                 title_synonyms,
                 image_url,
                 anime_type,
                 source,
                 episodes,
                 status,
                 airing,
                 aired_string,
                 aired,
                 duration,
                 rating,
                 score,
                 scored_by,
                 rank,
                 popularity,
                 members,
                 favorites,
                 background,
                 premiered,
                 broadcast,
                 related,
                 producer,
                 licensor,
                 studio,
                 genre,
                 opening_theme,
                 ending_theme) = row

                try:
                    aired = json.loads(aired.replace(
                        "'", '"').replace('None', '""'))
                    aired_from = convert_date_string(aired['from'])
                    aired_to = convert_date_string(aired['to'])
                except Exception:
                    print(title)
                    exit()

                conn.execute(
                    'INSERT INTO Anime VALUES (?,?,?,?,?,?,?,?)',
                    (anime_id, title, anime_type, aired_from,
                        aired_to, rating, premiered, studio)
                )

                genres = genre.split(", ")
                for g in genres:
                    if not g:
                        continue
                    if g not in genre_map:
                        genre_map[g] = len(genre_map)
                        conn.execute(
                            'INSERT INTO Genre VALUES (?,?)', (genre_map[g], g))
                    conn.execute(
                        'INSERT INTO AnimeGenre VALUES (?,?)', (anime_id, genre_map[g]))


if __name__ == '__main__':
    from helper import get_connection
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

    import config
    conn = get_connection(config.dbpath)
    convert_anime_csv_to_db(conn, 'AnimeList.csv')
    conn.close()
