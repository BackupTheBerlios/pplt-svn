import wxversion
wxversion.select("2.8")
import wx
import edef
from edef.dev.MainFrame import eDevMainFrame as MainFrame
import logging
from edef.dev import ComponentManager

print "Using wxPython version %s"%wx.__version__


class eDeveloper(wx.App):
    _components = None
    def OnInit(self):
        wx.InitAllImageHandlers()
        self._d_main_frame = MainFrame(None, "edef Developer")
        
        self._components = ComponentManager()


        self.SetTopWindow(self._d_main_frame)
        self._d_main_frame.Show(True)
        
        return True


    def OnExit(self):
        evt_hdl = edef.EventManager()
        evt_hdl.shutdown()



# init logging
edef.Logger(logging.DEBUG)

app = eDeveloper()
app.MainLoop()
