import wx

class InfoDialog(wx.MessageDialog):
    def __init__(self, parent, ID):
        msg = """Event driven engeneering frame work.
           Version 0.1a

Hannes Matuschek <hmatuschek@gmail.com>"""

        wx.MessageDialog.__init__(self, parent, msg, "About", wx.OK|wx.ICON_INFORMATION,)


