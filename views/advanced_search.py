import tkinter as tk
from sqlite3 import Connection
from typing import Union


class AdvancedSearch(tk.Frame):
    def __init__(self, master: Union[tk.Tk, tk.Toplevel()], connection: Connection, **kwargs):
        super().__init__(master, **kwargs)

        self.connection = connection


if __name__ == '__main__':
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

    import config
    from database.helper import get_connection
    conn = get_connection(config.dbpath)

    root = tk.Tk()
    AdvancedSearch(root, conn, width=1280, height=720).pack()
    root.mainloop()

    conn.close()
