from database import Anime, get_connection
from config import dbpath
import wx
import wx.lib.scrolledpanel
from math import ceil


class SearchResult(wx.Panel):
    def __init__(self, parent, anime: Anime = Anime('', '')):
        super().__init__(parent, size=(180, 240))

        self.anime = anime

        self.build_ui()

    def build_ui(self):
        self.SetBackgroundColour('#2D2F31')
        self.SetSizer(vbox := wx.BoxSizer(wx.VERTICAL))

        vbox.Add(inner := wx.Panel(self), 1, wx.ALIGN_CENTER)
        inner.SetSizer(hbox := wx.BoxSizer(wx.HORIZONTAL))
        
        hbox.Add(txt := wx.StaticText(inner, label=self.anime.title), 1, wx.ALIGN_CENTER)
        txt.SetForegroundColour('white')

        self.Bind(wx.EVT_LEFT_DOWN, self.select)
    
    def select(self, event):
        print(self.anime)


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
    def __init__(self, parent, animes: list[Anime] = None, page = 1):
        super().__init__(parent)

        self.animes = animes or []
        self.page = page

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
        
        left_btn.Bind(wx.EVT_LEFT_DOWN, self.previous_page)
        right_btn.Bind(wx.EVT_LEFT_DOWN, self.next_page)

        self.sizer = vbox
        self.SetupScrolling()
        self.search_box = search_box
        self.search_btn = search_btn
        self.results_box = results_box
        self.results_gs = results_gs
        self._anime_links = []
        self.load_animes(self.page)

    def load_animes(self, page):
        self._anime_links = self._anime_links or []

        for link in self._anime_links:
            self.results_gs.Hide(link[0])
            link[0].Destroy()

        self._anime_links = [(SearchResult(self.results_box, a), 0, wx.ALIGN_CENTER)
                       for a in self.animes[8 * (page - 1): 8 * page]]

        self.results_gs.AddMany(self._anime_links)

        self.sizer.Layout()
        # self.Fit()

    def previous_page(self, event):
        if self.page == 1:
            return
        
        self.page -= 1
        self.load_animes(self.page)

    def next_page(self, event):
        if self.page == 1 + ((len(self.animes) - 1) // 8):
            return
        
        self.page += 1
        self.load_animes(self.page)



if __name__ == '__main__':
    title = 'Search Results'
    size = (1280, 720)
    style = wx.CAPTION | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.CLOSE_BOX

    animes = [Anime(chr(i)) for i in range(ord('A'), ord('Z') + 1)]

    app = wx.App()
    frame = wx.Frame(None, title=title, size=size, style=style)
    SearchResults(frame, animes)
    frame.Center()
    frame.Show()
    app.MainLoop()
