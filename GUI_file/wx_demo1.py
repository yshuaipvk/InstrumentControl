import wx
class ExampleFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        panel = wx.Panel(self)
        self.quote = wx.StaticText(panel, label="Your quote:", pos=(20, 30))
        self.button = wx.Button(self,label ='Save',pos=(200,325))
        self.Bind(wx.EVT_BUTTON,self.OnClick,self.button)

        self.Show()

app = wx.App(False)
ExampleFrame(None)
app.MainLoop()