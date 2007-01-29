import wxversion
wxversion.select("2.8")
import wx

from MainFrame import eDevMainFrame
from Model import eDevModel

print "Using wxPython version %s"%wx.__version__

class eDeveloper(wx.App):

    def OnInit(self):
        self._d_model = eDevModel.instance()
        self._d_main_frame = eDevMainFrame(None, "edef Developer")
        self.SetTopWindow(self._d_main_frame)

        self._d_main_frame.Show(True)
        return True



app = eDeveloper()
app.MainLoop()
