import wx
from wx.lib.pubsub import pub
from views import *

def make_frame(panelFactory, *args, **kwargs):
    title = 'AniPedia'
    size = (1280, 720)
    style = wx.CAPTION | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.CLOSE_BOX
    frame = wx.Frame(None, title=title, size=size, style=style)
    panel = panelFactory(frame, *args, **kwargs)
    frame.Center()
    return frame, panel


class AniPedia:
    def __init__(self, **kwargs):
        self.frame_panel = []
        
        self.push_frame_panel(*make_frame(LoginDialog, self.on_login))

    def push_frame_panel(self, frame, panel):
        if self.frame_panel:
            self.frame_panel[-1][0].Hide()

        self.frame_panel.append((frame, panel))
        frame.Show()

    def on_login(self):
        self.push_frame_panel(*make_frame(AdvancedSearch, self.on_search_result))
    
    def on_search_result(self, animes):
        self.push_frame_panel(*make_frame(SearchResults, animes, self.on_anime_selected))
    
    def on_anime_selected(self, anime):
        self.push_frame_panel(*make_frame(AnimePreview, anime, previous=self.previous))
    
    def previous(self, _):
        if not self.frame_panel:
            return
        
        self.frame_panel[-1][0].Hide()
        self.frame_panel[-1][0].Destroy()
        self.frame_panel[-1][1].Destroy()

        if not self.frame_panel:
            return

        self.frame_panel.pop()
        self.frame_panel[-1][0].Show()



if __name__ == '__main__':
    app = wx.App()
    AniPedia()
    app.MainLoop()
