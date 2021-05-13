from sqlite3 import Connection
from glooey.misc import Placeholder
import pyglet
import glooey
import json
import urllib.request
from urllib.request import urlopen, Request
from PIL import Image

class GatherInfo:
    def getposter(self, title):
        title_parts = title.split(' ')
        self.title = ''
        for word in title_parts:
            self.title = self.title + word + '%20'
        self.title = self.title[:-3]
        url = 'https://kitsu.io/api/edge/anime?filter[text]=' + self.title + '''=(Title)&fields[anime]=canonicalTitle,posterImage&page[limit]=1&page[offset]=0
        '''
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        reg_url = url
        req = Request(url=reg_url, headers=headers) 
        link = urlopen(req).read() 

        json_string=link
        my_dict=json.loads(json_string)

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
        main_url = 'https://kitsu.io/api/edge/anime?filter[text]=' + self.title + '''=(Title)&fields[anime]=canonicalTitle,posterImage&page[limit]=1&page[offset]=0
        '''
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        reg_url = main_url
        req = Request(url=reg_url, headers=headers) 
        main_link = urlopen(req).read() 

        json_string=main_link
        main_dict=json.loads(json_string)
        details_url=(main_dict['data'][0]['links']['self'])

        reg_url = details_url
        req = Request(url=reg_url, headers=headers) 
        details_link = urlopen(req).read() 

        json_string1=details_link
        details_dict=json.loads(json_string1)

        return "Synopsis: " + details_dict['data']['attributes']['synopsis']



class BackButton(glooey.Button):
    custom_height_hint = 50
    custom_width_hint = 80
    custom_alignment = 'right'

    class Foreground(glooey.Label):
        custom_color = '#babdb6'
        custom_font_size = 10
        custom_alignment = 'center'

    class Base(glooey.Background):
        custom_color = '#204a87'
        custom_outline = 'yellow'

    class Over(glooey.Background):
        custom_color = '#3465a4'
        custom_outline = 'yellow'

    class Down(glooey.Background):
        custom_color = '#729fcfff'
        custom_outline = 'yellow'

    def __init__(self):
        super().__init__(text='Back')

    def on_click(self, _):
        pass

class AnipediaLabel(glooey.Label):
        custom_color = 'white'
        custom_vert_padding = 0
        custom_horz_padding = 20
        custom_font_size = 20
        custom_width_hint = 48
        custom_height_hint = 24
        custom_text = 'Anipedia'
        custom_background_color = '#204a87'
        custom_alignment = 'center'

        class Base(glooey.Background):
            custom_color = '#204a87'
            custom_outline = 'yellow'

class AnimeTitle(glooey.text.Label):
    custom_color = '#7A5299'
    custom_vert_padding = 2
    custom_horz_padding = 20
    custom_font_size = 16
    custom_alignment = 'center'

class AnimeInfo(glooey.text.Label):
    custom_color = 'white'
    custom_vert_padding = 10
    custom_horz_padding = 20
    custom_font_size = 10
    custom_alignment = 'fill'

class AnimePoster(glooey.Image):
    custom_alignment = 'center'
    custom_padding = 5
    # def GetPoster(self, image_url):
    #     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    #     url = image_url
    #     reg_url = url
    #     req = Request(url=reg_url, headers=headers) 
    #     self.image = Image.open(urllib.request.urlopen(req))
        

class topcontainer(glooey.HBox):
    class Base(glooey.Background):
        custom_color = '#204a87'
        custom_outline = 'yellow'

class ImageContainer(glooey.VBox):
    class Base(glooey.Background):
        custom_color = '#204a87'
        custom_outline = 'yellow'

class InfoContainer(glooey.VBox):
    class Base(glooey.Background):
        custom_color = '#204a87'
        custom_outline = 'yellow'

class Base(glooey.Background):
    custom_color = '#204a87'
    custom_outline = None

class Scroll(glooey.VScrollBar):
    custom_button_speed = 100

class AnimePreview(glooey.Widget):
    def __init__(self, connection: Connection, **kwargs):
        super().__init__(**kwargs)

        self.connection = connection
        self.maininfo = GatherInfo()
        self.anipedia_label = AnipediaLabel()
        self.back_btn = BackButton()
        self.animeinfo = AnimeInfo()
        self.animeposter = AnimePoster()
        self.background = Base()
        title = 'Dragon Ball Z'
        self.title = AnimeTitle(title)
        self.synopsis = AnimeInfo(self.maininfo.getsynopsis(title), line_wrap = 1243)
        self.scroll = Scroll('right')
        
        self.top_container = topcontainer()
        self.image_container = ImageContainer()
        self.info_container = InfoContainer()
        self.back_btn.on_click = self.back_btn_click
        # self.image_container.add_back(self.background)
        image = self.maininfo.getposter(title)
        self.image_container.add(AnimePoster(pyglet.image.load('poster.png')))

        self.top_container.add(self.anipedia_label, size=0)
        self.top_container.add(Placeholder())
        self.top_container.add(self.back_btn, size=0)
        # self.top_container.add_back(self.background, size=None)

        self.image_container.custom_size_hint = 720, 500
        # info = self.maininfo.getposter(title)
        # print(info)
        # final = self.animeposter.GetPoster(info)
        # self.image_container.add(pyglet.image.load(final))
        
        self.info_container.add(self.title, size = 0)
        self.info_container.add(self.synopsis, size = 0)
        self.info_container.add(self.animeinfo, size = 0)
        self.info_container.add(self.animeinfo, size = 0)
        self.info_container.add(self.animeinfo, size = 0)
        self.info_container.add(self.animeinfo, size = 0)

        self.info_container._attach_child(self.scroll)

        self.container = glooey.VBox()
        self.container.custom_size_hint = 1280, 720
        self.container.custom_alignment = 'top'
        self.container.add(self.top_container, size=0)
        self.container.add(self.image_container, size=0)
        self.container.add(self.info_container, size=0)
        

        self._attach_child(self.container)
        

    def back_btn_click(self, _):
        print("previous page")


if __name__ == '__main__':
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    import config
    from database.helper import get_connection
    conn = get_connection(config.dbpath)

    window = pyglet.window.Window(1280, 720)
    gui = glooey.Gui(window)
    gui.add(AnimePreview(conn))
    
    MainPoster = AnimePoster()
    
    # AnimePoster.GetPoster('LOGIN_BG.png')
    # AnimeInfo.GetInfo('Test','test')
    pyglet.app.run()

    conn.close()