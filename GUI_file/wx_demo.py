import wx
from wx.core import Frame


class MainWdindows(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size= (500,400))
        self.control = wx.TextCtrl(self,style = wx.TE_MULTILINE)
        self.CreateStatusBar()
        filemenu = wx.Menu()

        menuOpen = filemenu.Append(wx.ID_OPEN,'&Open','Open a file')
        menuExit = filemenu.Append(wx.ID_EXIT,"exit",'exit program')
        menuAbout = filemenu.Append(wx.ID_ABORT,"About",'dahjdao')


        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,'File')
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU,self.OnOpen,menuOpen)
        self.Bind(wx.EVT_MENU,self.OnAbout,menuAbout)
        self.Bind(wx.EVT_MENU,self.OnEXit,menuExit)
        
        
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.buttons = []
        for i in range(0,6):
            self.buttons.append(wx.Button(self,-1,'Button &'+str(i))) 
            self.sizer2.Add(self.buttons[i] , 1, wx.SHAPED)
        
        self.sizer =  wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.control,1,wx.EXPAND)
        self.sizer.Add(self.sizer2,0,wx.GROW)

        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)
        self.sizer.Fit(self)



        



        self.Show()

    def OnAbout(self, e):
        dlg = wx.MessageDialog(self, "A small text editor.", \
            "About Sample Editor", wx.OK)   
        dlg.ShowModal()  
        dlg.Destroy()
    def OnEXit(self,e):
        self.Close(True)

    def OnOpen(self,e):
        import os
        self.dirname = ''
        dlg = wx.FileDialog(self,'Choose a file',self.dirname,'','*.*',wx.FD_OPEN)
        if dlg.ShowModal() ==wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname,self.filename),'r')
            self.control.SetValue(f.read())
        dlg.Destroy()

app = wx.App(False)
frame = MainWdindows(None,"Small editor")
app.MainLoop()