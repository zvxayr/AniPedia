from sqlite3 import Connection
import pyglet
import json
import urllib.request
from urllib.request import urlopen, Request
from PIL import Image
from database import Genre, get_connection
from config import dbpath
import wx
import wx.lib.scrolledpanel
from pubsub import *
from database.helper import get_connection
from config import dbpath
from database import Anime
from database import User


class GatherInfo:
    def getposter(self, title):
        self.title = title.replace(' ', '%20')
        url = f"""https://kitsu.io/api/edge/anime?filter[text]={self.title}=(Title)&fields[anime]=canonicalTitle,posterImage&page[limit]=1&page[offset]=0
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        reg_url = url
        req = Request(url=reg_url, headers=headers)
        link = urlopen(req).read()

        json_string = link
        my_dict = json.loads(json_string)

        reg_url = my_dict['data'][0]['attributes']['posterImage']['small']
        req = Request(url=reg_url, headers=headers)
        image = Image.open(urllib.request.urlopen(req))

        image.save("poster.png", format='PNG', quality=75)

    def getsynopsis(self, title):
        title_parts = title.split(' ')
        self.title = ''
        for word in title_parts:
            self.title = self.title + word + '%20'
        self.title = self.title[:-3]
        main_url = f"""https://kitsu.io/api/edge/anime?filter[text]={self.title}=(Title)&fields[anime]=canonicalTitle,posterImage&page[limit]=1&page[offset]=0
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        reg_url = main_url
        req = Request(url=reg_url, headers=headers)
        main_link = urlopen(req).read()

        json_string = main_link
        main_dict = json.loads(json_string)
        details_url = (main_dict['data'][0]['links']['self'])

        reg_url = details_url
        req = Request(url=reg_url, headers=headers)
        details_link = urlopen(req).read()

        json_string1 = details_link
        details_dict = json.loads(json_string1)

        return "Synopsis: \n \n" + details_dict['data']['attributes']['synopsis']


class AnimePreview(wx.Panel):
    def __init__(self, parent, anime, previous):
        super().__init__(parent)
        self.Anime = anime
        self.title = anime.title
        self.previous = previous
        self.build_ui()

    def build_ui(self):
        self.username = 'Xinil'
        self.password = ''
        self.gatherinfo = GatherInfo()
        self.SetBackgroundColour('#1D1F21')
        self.SetSizer(top_vbox := wx.BoxSizer(wx.VERTICAL))
        self.user = User(self.username, self.password)

        top_vbox.Add(header := wx.Panel(self, size=(-1, 60)), 0, wx.EXPAND)
        header.SetSizer(header_hbox := wx.BoxSizer(wx.HORIZONTAL))
        header.SetBackgroundColour('#A286B8')

        header_hbox.Add(AnipediaLabelContainer := wx.Panel(
            header, size=(50, -1)), wx.ALIGN_LEFT | wx.EXPAND | wx.LEFT, border=20)
        AnipediaLabelContainer.SetSizer(
            AnipediaLabelContainer_hbox := wx.BoxSizer(wx.VERTICAL))
        AnipediaLabelContainer_hbox.Add(AnipediaLabel := wx.StaticText(
            AnipediaLabelContainer), flag=wx.LEFT | wx.TOP, border=10)
        AnipediaLabel.SetLabel('Anipedia')

        Titlefont = wx.Font(pointSize=22, family=wx.DEFAULT,
                            style=wx.NORMAL, weight=wx.NORMAL,
                            faceName='Arial Bold')

        AnipediaLabel.SetFont(Titlefont)

        header_hbox.Add(ratingpanel := wx.Panel(
            header, size=(120, -1)), wx.ALIGN_RIGHT)
        ratingpanel.SetSizer(ratingpanel_vbox := wx.BoxSizer(wx.VERTICAL))
        ratingpanel_vbox.Add(rate_btn := wx.Button(
            ratingpanel, label='Rate this anime?', size=(120, 80)), flag=wx.ALIGN_RIGHT)
        rate_btn.SetBackgroundColour('#7B5B94')

        header_hbox.Add(rate_box := wx.TextCtrl(
            header, size=(120, 40)), flag=wx.TOP | wx.RIGHT, border=10)
        rate_box.SetHint('Rate Anime...')

        header_hbox.Add(innerpanel := wx.Panel(
            header, size=(120, 80)), wx.ALIGN_RIGHT)
        innerpanel.SetSizer(innerpanel_vbox := wx.BoxSizer(wx.VERTICAL))
        innerpanel_vbox.Add(back_btn := wx.Button(
            innerpanel, label='Back', size=(120, 80)), flag=wx.ALIGN_RIGHT)
        back_btn.Bind(wx.EVT_BUTTON, self.previous)
        back_btn.SetBackgroundColour('#7B5B94')

        # image
        self.gatherinfo.getposter(self.title)
        top_vbox.Add(body := wx.lib.scrolledpanel.ScrolledPanel(
            self, size=(1280, 1600), style=wx.SIMPLE_BORDER), flag=wx.CENTER)
        body.SetupScrolling()
        body.SetSizer(body_vbox := wx.BoxSizer(wx.VERTICAL))
        body.SetBackgroundColour('#1A1110')
        body_vbox.Add(poster := wx.StaticBitmap(body, wx.ID_ANY, wx.Bitmap(
            'poster.png', type=wx.BITMAP_TYPE_PNG)), flag=wx.CENTER | wx.TOP, border=50)

        # info
        body_vbox.Add(AnimeTitle := wx.StaticText(body),
                      flag=wx.CENTER | wx.TOP, border=20)
        AnimeTitle.SetLabel(self.title)
        AnimeTitleFont = wx.Font(pointSize=22, family=wx.DEFAULT,
                                 style=wx.NORMAL, weight=wx.NORMAL, underline=True,
                                 faceName='Arial Bold')

        AnimeTitle.SetForegroundColour("#7B5B94")
        AnimeTitle.SetFont(AnimeTitleFont)

        conn = get_connection(dbpath)
        self.Genre = self.Anime.get_genres(conn)
        genre_names = list(map(lambda g: g.name, self.Genre))

        Animegenres = 'Genres: '
        for genres in genre_names:
            Animegenres = Animegenres + genres + ', '

        Animegenres = Animegenres[:-2]

        Type = self.Anime.anime_type
        Premiere = self.Anime.premiered
        Studio = self.Anime.studio
        self.ID = self.Anime.anime_id

        rate_btn.Bind(wx.EVT_BUTTON, self.rateanime)

        # Genres
        body_vbox.Add(Animegenres := wx.StaticText(
            body, label=Animegenres), flag=wx.LEFT | wx.TOP, border=20)
        AnimegenresFont = wx.Font(pointSize=16, family=wx.DEFAULT,
                                  style=wx.NORMAL, weight=wx.NORMAL,
                                  faceName='Arial')

        Animegenres.Wrap(690)
        Animegenres.SetForegroundColour("white")
        Animegenres.SetFont(AnimegenresFont)

        # Type
        Type = 'Type: ' + Type
        body_vbox.Add(Type := wx.StaticText(body, label=Type),
                      flag=wx.LEFT | wx.TOP, border=20)
        TypeFont = wx.Font(pointSize=16, family=wx.DEFAULT,
                           style=wx.NORMAL, weight=wx.NORMAL,
                           faceName='Arial')

        Type.Wrap(690)
        Type.SetForegroundColour("white")
        Type.SetFont(TypeFont)

        # Premiere
        Premiere = 'Premiere: ' + Premiere
        body_vbox.Add(Premiere := wx.StaticText(
            body, label=Premiere), flag=wx.LEFT | wx.TOP, border=20)
        PremiereFont = wx.Font(pointSize=16, family=wx.DEFAULT,
                               style=wx.NORMAL, weight=wx.NORMAL,
                               faceName='Arial')

        Premiere.Wrap(690)
        Premiere.SetForegroundColour("white")
        Premiere.SetFont(PremiereFont)

        # Synopsis
        AnimeSynopsis = self.gatherinfo.getsynopsis(self.title)
        body_vbox.Add(AnimeSynopsis := wx.StaticText(
            body, label=AnimeSynopsis), flag=wx.LEFT | wx.TOP, border=20)
        AnimeSynopsisFont = wx.Font(pointSize=16, family=wx.DEFAULT,
                                    style=wx.NORMAL, weight=wx.NORMAL,
                                    faceName='Arial')

        AnimeSynopsis.Wrap(690)
        AnimeSynopsis.SetForegroundColour("white")
        AnimeSynopsis.SetFont(AnimeSynopsisFont)

        # studio
        Studio = 'Studio: ' + Studio
        body_vbox.Add(Studio := wx.StaticText(body, label=Studio),
                      flag=wx.LEFT | wx.TOP, border=20)
        StudioFont = wx.Font(pointSize=16, family=wx.DEFAULT,
                             style=wx.NORMAL, weight=wx.NORMAL,
                             faceName='Arial')

        Studio.Wrap(690)
        Studio.SetForegroundColour("white")
        Studio.SetFont(StudioFont)

    def rateanime(self, event):
        rating = self.rate_box.GetValue()
        if rating != 0-10:
            self.rate_box.SetHint('Invalid Input')
        else:
            with get_connection(dbpath) as conn:
                user_rating = int(rating)
                self.user.rate_anime(conn, ID, user_rating)


if __name__ == '__main__':
    title = 'Anime Preview'
    size = (1280, 720)
    style = wx.CAPTION | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.CLOSE_BOX

    app = wx.App()
    frame = wx.Frame(None, title=title, size=size, style=style)
    title = 'Fullmetal Alchemist: Brotherhood'
    AnimePreview(frame, title)
    frame.Center()
    frame.Show()
    app.MainLoop()
