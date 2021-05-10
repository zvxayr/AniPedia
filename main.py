from typing import Union
from database import User, Anime, get_connection
from config import dbpath
import tkinter.ttk as ttk
import tkinter as tk


class AniPedia(tk.Tk):
    def __init__(self):
        super().__init__()
        self.resizable(False, False)
        self.geometry("1280x720")


def center(win: Union[tk.Tk, tk.Toplevel]):
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry(f'{width}x{height}+{x}+{y}')
    win.deiconify()


if __name__ == "__main__":
    from database import initialize_database
    initialize_database(get_connection(dbpath))

    root = AniPedia()
    center(root)
    root.mainloop()
