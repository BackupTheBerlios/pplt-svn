import wx

class NewPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        wx.StaticText(self, -1, "...")

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="title")
        
        self.pan = wx.Panel(self)
        
        box = wx.BoxSizer(wx.VERTICAL)

        self.button = wx.Button(self.pan, -1, "Close")
        self.nb = wx.Notebook(self.pan)

        self.page = NewPage(self.nb)
        
        self.nb.AddPage(self.page, "Page")
        
        box.Add(self.button,0)
        box.Add(self.nb, 1, wx.EXPAND)
        self.pan.SetSizer(box)

        self.button.Bind(wx.EVT_BUTTON, self.OnClose)

    def OnClose(self, evt):
        self.nb.DeletePage(self.nb.GetSelection())


if __name__ == "__main__":
    app = wx.App()
    MainFrame().Show()
    app.MainLoop()
