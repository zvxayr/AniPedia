import wx
from wx.lib.pubsub import pub
from database import User
from database.helper import get_connection
from config import dbpath
from views.advanced_search import AdvancedSearch
from views.advanced_search import AdvancedSFrame


class LoginDialog(wx.Panel):
    def __init__(self, parent, login=lambda: None):
        wx.Frame.__init__(self, parent)

        self.login = login
        # title
        self.SetBackgroundColour('#1D1F21')
        self.SetSizer(top_vbox := wx.BoxSizer(wx.VERTICAL))

        top_vbox.Add(header := wx.Panel(self, size=(-1, 60)), 0, wx.EXPAND)
        header.SetSizer(header_hbox := wx.BoxSizer(wx.VERTICAL))
        header.SetBackgroundColour('#A286B8')

        header_hbox.Add(AnipediaLabelContainer := wx.Panel(
            header, size=(-1, -1)), wx.ALIGN_LEFT | wx.EXPAND)
        AnipediaLabelContainer.SetSizer(
            AnipediaLabelContainer_hbox := wx.BoxSizer(wx.HORIZONTAL))
        AnipediaLabelContainer_hbox.Add(AnipediaLabel := wx.StaticText(
            AnipediaLabelContainer), flag=wx.ALIGN_CENTER | wx.LEFT, border=20)
        AnipediaLabel.SetLabel('Anipedia')

        Titlefont = wx.Font(pointSize=22, family=wx.DEFAULT,
                            style=wx.NORMAL, weight=wx.NORMAL,
                            faceName='Arial Bold')
        AnipediaLabel.SetFont(Titlefont)

        # user info
        Subfont = wx.Font(pointSize=15, family=wx.DEFAULT,
                          style=wx.NORMAL, weight=wx.NORMAL,
                          faceName='Calibri')

        top_vbox.Add(body := wx.Panel(self), 1, wx.EXPAND |
                     wx.LEFT | wx.RIGHT, border=350)
        body.SetSizer(body_vbox := wx.BoxSizer(wx.HORIZONTAL))
        body.SetBackgroundColour('#1D1F21')

        username_lbl = wx.StaticText(body, label="Username: ")
        username_lbl.SetFont(Subfont)
        username_lbl.SetForegroundColour('white')
        body_vbox.Add(username_lbl, 1, wx.EXPAND | wx.ALL | wx.RIGHT, 30)
        self.username = wx.TextCtrl(body, size=wx.Size(363, 20))
        body_vbox.Add(self.username, 7, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 30)

        # pass info
        top_vbox.Add(pass_panel := wx.Panel(self), 1,
                     wx.EXPAND | wx.LEFT | wx.RIGHT, border=350)
        pass_panel.SetSizer(body_vbox := wx.BoxSizer(wx.HORIZONTAL))
        pass_panel.SetBackgroundColour('#1D1F21')

        password_lbl = wx.StaticText(pass_panel, label="Password:")
        password_lbl.SetFont(Subfont)
        password_lbl.SetForegroundColour('white')

        body_vbox.Add(password_lbl, 1, wx.EXPAND | wx.ALL, 30)
        self.password = wx.TextCtrl(
            pass_panel, style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER, size=wx.Size(363, 20))
        body_vbox.Add(self.password, 7, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 30)

        # buttin panel
        top_vbox.Add(button_panel := wx.Panel(self), 25,
                     wx.EXPAND | wx.LEFT | wx.RIGHT, border=350)
        button_panel.SetSizer(body_vbox := wx.BoxSizer(wx.VERTICAL))
        button_panel.SetBackgroundColour('#1D1F21')

        btn = wx.Button(button_panel, label="Login")
        btn.Bind(wx.EVT_BUTTON, self.onLogin)
        body_vbox.Add(btn, 0, wx.ALL | wx.CENTER, 5)

    def onLogin(self, event):
        with get_connection(dbpath) as conn:
            user_username = self.username.GetValue()
            user_password = self.password.GetValue()
            self.user = User.from_username(conn, user_username)

        if self.user.password == user_password and self.user.username == user_username:
            self.login()


if __name__ == "__main__":
    title = 'Login'
    size = (1280, 720)
    style = wx.CAPTION | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.CLOSE_BOX

    app = wx.App()
    frame = wx.Frame(None, title=title, size=size, style=style)
    LoginDialog(frame)
    frame.Center()
    frame.Show()
    app.MainLoop()
