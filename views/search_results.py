from database import Anime, get_connection
from config import dbpath
import wx
import wx.lib.scrolledpanel
from math import ceil


class SearchResult(wx.Panel):
    def __init__(self, parent, anime: Anime = None):
        super().__init__(parent, size=(180, 240))

        self.anime = anime

        self.build_ui()

    def build_ui(self):
        self.SetBackgroundColour('#2D2F31')
        self.SetSizer(vbox := wx.BoxSizer(wx.VERTICAL))


def make_arrow_btn(parent, label):
    btn = wx.Button(parent, label=label, size=(40, 40))
    btn.SetWindowStyleFlag(wx.NO_BORDER)

    btn.SetBackgroundColour('#2D2F31')
    btn.SetForegroundColour('#FFFFFF')

    def onMouseDown(event):
        btn.SetBackgroundColour('Yellow')
        btn.Refresh()

    def onMouseUp(event):
        btn.SetBackgroundColour('Green')
        btn.Refresh()

    def onMouseOver(event):
        btn.SetBackgroundColour('Green')
        btn.Refresh()

    def onMouseLeave(event):
        btn.SetBackgroundColour('#2D2F31')
        btn.Refresh()

    btn.Bind(wx.EVT_LEFT_DOWN, onMouseDown)
    btn.Bind(wx.EVT_LEFT_UP, onMouseUp)
    btn.Bind(wx.EVT_ENTER_WINDOW, onMouseOver)
    btn.Bind(wx.EVT_LEAVE_WINDOW, onMouseLeave)

    return btn


class SearchResults(wx.lib.scrolledpanel.ScrolledPanel):
    def __init__(self, parent, animes: list[Anime] = None):
        super().__init__(parent)

        self.animes = animes or []

        self.build_ui()

    def build_ui(self):
        self.SetBackgroundColour('#1D1F21')
        self.SetSizer(vbox := wx.BoxSizer(wx.VERTICAL))

        vbox.Add(header := wx.Panel(self, size=(-1, 80)), 0, wx.EXPAND)
        header.SetSizer(header_hbox := wx.BoxSizer(wx.HORIZONTAL))
        header.SetBackgroundColour('#ededed')

        header_hbox.Add(search_box := wx.TextCtrl(header))
        search_box.SetHint('Enter Anime Name')

        header_hbox.Add(search_btn := wx.Button(header, label='Search'))

        vbox.Add(body := wx.Panel(self, size=(-1, -1)), 1,
                 wx.EXPAND | wx.LEFT | wx.RIGHT, border=200)
        body.SetSizer(body_hbox := wx.BoxSizer(wx.HORIZONTAL))

        body_hbox.Add(left_btn := make_arrow_btn(
            body, label='<'), 0, wx.ALIGN_CENTER)
        body_hbox.Add(results_box := wx.Panel(body), 1, wx.EXPAND, border=5)
        body_hbox.Add(right_btn := make_arrow_btn(
            body, label='>'), 0, wx.ALIGN_CENTER)

        results_box.SetSizer(
            results_gs := wx.GridSizer(rows=2, cols=4, vgap=5, hgap=5))

        self.SetupScrolling()
        self.search_box = search_box
        self.search_btn = search_btn
        self.results_box = results_box
        self.results_gs = results_gs
        self.load_animes()

    def load_animes(self):
        anime_links = [(SearchResult(self.results_box, a), 0, wx.ALIGN_CENTER)
                       for a in self.animes]

        self.results_gs.AddMany(anime_links)


if __name__ == '__main__':
    title = 'Search Results'
    size = (1280, 720)
    style = wx.CAPTION | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.CLOSE_BOX

    animes = [Anime(chr(i)) for i in range(ord('A'), ord('Z') + 1)]

    app = wx.App()
    frame = wx.Frame(None, title=title, size=size, style=style)
    SearchResults(frame, [Anime('A'), Anime('B'), Anime('C'), Anime(
        'D'), Anime('E'), Anime('F'), Anime('G')])
    frame.Center()
    frame.Show()
    app.MainLoop()
