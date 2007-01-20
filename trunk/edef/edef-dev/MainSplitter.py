import wx


class eDevMainSplitter(wx.SplitterWindow):
    
    def __init__(self, parent, ID):
        wx.SplitterWindow.__init__(self, parent , ID,
                          style=wx.SP_LIVE_UPDATE)

        self.SetMinimumPaneSize(80)
