from user_converter import convert_user_csv_to_db
from anime_converter import convert_anime_csv_to_db
from user_anime_converter import convert_user_anime_csv_to_db


if __name__ == '__main__':
    from helper import get_connection
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

    import config
    conn = get_connection(config.dbpath)

    convert_user_csv_to_db(conn, 'UserList.csv')
    print('Processed UserList.csv')
    convert_anime_csv_to_db(conn, 'AnimeList.csv')
    print('Processed AnimeList.csv')
    convert_user_anime_csv_to_db(conn, 'UserAnimeList.csv')
    print('Processed UserAnimeList.csv')
    conn.close()
