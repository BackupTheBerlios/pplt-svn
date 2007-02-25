import wx
import wx.py as py
from EditorInterface import eDevEditorInterface
from Controller import eDevController

class eDevShell(py.shell.Shell, eDevEditorInterface):
    
    def __init__(self, parent, ID, uri, txt):
        py.shell.Shell.__init__(self, parent, ID, introText=txt)
        eDevEditorInterface.__init__(self,False, uri)
        self._controller = eDevController()
        self._mainframe = self._controller .getMainFrame()

    def OnSelected(self):
        self._mainframe.bindClose(self.onClose)

    def onClose(self, evt=None):
        self._controller.DocumentClose()
