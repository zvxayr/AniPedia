import wx
from pubsub import pub

class LoginDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, title="Login", size=(1280,720))
        
        #title
        self.SetBackgroundColour('#1D1F21')
        self.SetSizer(top_vbox := wx.BoxSizer(wx.VERTICAL))

        top_vbox.Add(header := wx.Panel(self, size=(-1, 60)), 0, wx.EXPAND)
        header.SetSizer(header_hbox := wx.BoxSizer(wx.VERTICAL))
        header.SetBackgroundColour('#A286B8') 
        
        header_hbox.Add(AnipediaLabelContainer := wx.Panel(header, size = (-1, -1)), wx.ALIGN_LEFT | wx.EXPAND)
        AnipediaLabelContainer.SetSizer(AnipediaLabelContainer_hbox := wx.BoxSizer(wx.HORIZONTAL))
        AnipediaLabelContainer_hbox.Add(AnipediaLabel := wx.StaticText(AnipediaLabelContainer), flag = wx.ALIGN_CENTER | wx.LEFT, border = 20)
        AnipediaLabel.SetLabel('Anipedia')

        Titlefont = wx.Font(pointSize = 22, family = wx.DEFAULT,
               style = wx.NORMAL, weight = wx.NORMAL,
               faceName = 'Arial Bold')
        AnipediaLabel.SetFont(Titlefont)

        
        # user info
        Subfont = wx.Font(pointSize = 15, family = wx.DEFAULT,
               style = wx.NORMAL, weight = wx.NORMAL,
               faceName = 'Calibri')

        
        top_vbox.Add(body := wx.Panel(self), 1, wx.EXPAND | wx.LEFT | wx.RIGHT, border=350)
        body.SetSizer(body_vbox := wx.BoxSizer(wx.HORIZONTAL))
        body.SetBackgroundColour('#1D1F21')

        username_lbl = wx.StaticText(body, label="Username: ")
        username_lbl.SetFont(Subfont)
        username_lbl.SetForegroundColour('white')
        body_vbox.Add(username_lbl, 1, wx.EXPAND|wx.ALL|wx.RIGHT, 30)
        self.username = wx.TextCtrl(body, size=wx.Size(363, 20))
        body_vbox.Add(self.username, 7, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 30)

        # pass info
        top_vbox.Add(pass_panel := wx.Panel(self), 1, wx.EXPAND | wx.LEFT | wx.RIGHT, border=350)
        pass_panel.SetSizer(body_vbox := wx.BoxSizer(wx.HORIZONTAL))
        pass_panel.SetBackgroundColour('#1D1F21')

        password_lbl = wx.StaticText(pass_panel, label="Password:")
        password_lbl.SetFont(Subfont)
        password_lbl.SetForegroundColour('white')

        body_vbox.Add(password_lbl, 1, wx.EXPAND|wx.ALL, 30)
        self.password = wx.TextCtrl(pass_panel, style=wx.TE_PASSWORD|wx.TE_PROCESS_ENTER, size=wx.Size(363, 20))
        body_vbox.Add(self.password, 7, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 30)
    
        
        # buttin panel
        top_vbox.Add(button_panel := wx.Panel(self), 25, wx.EXPAND | wx.LEFT | wx.RIGHT, border=350)
        button_panel.SetSizer(body_vbox := wx.BoxSizer(wx.VERTICAL))
        button_panel.SetBackgroundColour('#1D1F21')

        btn = wx.Button(button_panel, label="Login")
        btn.Bind(wx.EVT_BUTTON, self.onLogin)
        body_vbox.Add(btn, 0, wx.ALL | wx.CENTER, 5)
        
               
    def onLogin(self, event):
        sample_username = "sample"
        sample_password = "sample"
        user_username = self.username.GetValue()
        user_password = self.password.GetValue()
        
        if user_password == sample_password and user_username == sample_username:
            print("You are now logged in!")
            pub.sendMessage("frameListener", message="show")
            self.Destroy()
        else:
            print("Username or password is incorrect!")
            
class MyPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
    
class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Main App")
        panel = MyPanel(self)
        pub.subscribe(self.myListener, "frameListener")
        
        # Ask user to login
        dlg = LoginDialog()
        dlg.ShowModal()
        
    def myListener(self, message, arg2=None):
        self.Show()
        
if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()
  