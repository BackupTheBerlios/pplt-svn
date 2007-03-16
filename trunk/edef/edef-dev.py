#!/env/python

import wxversion
wxversion.select("2.8")

import wx
import edef
import logging
from optparse import OptionParser
from edef.dev.MainFrame import eDevMainFrame as MainFrame
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



if __name__ == "__main__":
    # handle commandline arguments:
    parser = OptionParser()
    parser.add_option("-d", "--debug", help='set loglevel to "debug"',
                      action="store_true", dest="debug")
    (opts, args) = parser.parse_args()

    # init logging
    if opts.debug: edef.Logger(logging.DEBUG)
    else: edef.Logger()

    # start application
    app = eDeveloper()
    app.MainLoop()


