from sqlite3 import Connection, ProgrammingError, connect
from contextlib import contextmanager
from typing import NoReturn
from os import path


def is_connection_closed(connection: Connection) -> bool:
    try:
        connection.execute('select 1')
    except ProgrammingError:
        return True
    else:
        return False


def get_connection(database: str = ':memory:', absolute=False, connections={}) -> Connection:
    if database not in connections or is_connection_closed(connections[database]):
        connections[database] = connect(database)

    return connections[database]


def initialize_database(conn: Connection) -> NoReturn:
    filepath = f'{path.dirname(__file__)}\initialize_database.sql'
    with open(filepath) as sqlfile:
        sqlscript = sqlfile.read()
        conn.executescript(sqlscript)


@contextmanager
def foreign_key_checks_off(conn: Connection):
    conn.execute('PRAGMA foreign_keys = OFF;')
    try:
        yield
    finally:
        conn.execute('PRAGMA foreign_keys = ON;')
        conn.commit()
