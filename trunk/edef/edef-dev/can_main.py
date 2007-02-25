import wxversion
wxversion.select("2.8")

import wx
import sys
import edef
from ElementMap import ElementMap




class CanvasFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, size=(640,480))
        
        self.canvas = ElementMap(self, -1)

        self.canvas.loadModule( "logic.AND", (10,10) )
        self.canvas.loadModule( "logic.OR", (40,10) )
        self.canvas.loadModule( "logic.NOT", (70, 10) )
        self.canvas.redraw()



class CanvasMain(wx.App):

    def OnInit(self):
        main_frame = CanvasFrame(None, "Canvas Test")
        self.SetTopWindow(main_frame)
        main_frame.Show(True)
        return True

app = CanvasMain()
app.MainLoop()
