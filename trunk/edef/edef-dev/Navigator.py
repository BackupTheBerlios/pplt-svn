import wx
from wx.lib.splitter import MultiSplitterWindow
from Controller import eDevController
from NavigatorPanel import NavigatorPanel, EVT_NAV_ACTIVATE

class eDevNavigator(MultiSplitterWindow):
    _controller = None
    _panels     = None

    def __init__(self, parent, ID):
        MultiSplitterWindow.__init__(self, parent, ID)
        self.SetOrientation( wx.VERTICAL )

        self._controller = eDevController()
        self._controller.setNavigator(self)
        self._panels     = list()

    
    def OnActivated(self, evt):
        if len(self._panels) == 0: return
        panel = evt.getPanel()
        idx = self._panels.index(panel)
        max_idx = len(self._panels)-1
        
        (tmp, height) = panel._label.GetSize()
        height += 4
        (tmp, max_height) = self.GetSize()

        for i in range(max_idx):
            if i == idx: pos = max_height - (max_idx+1)*height
            else: pos = height
            self.SetSashPosition(i, pos)


    def addNavigatorPanel(self, panel):
        self._panels.append(panel)
        self.AppendWindow(panel)
        self.Bind(EVT_NAV_ACTIVATE, self.OnActivated, id=panel.GetId())
        self._minimize_all()

    def _minimize_all(self):
        if len(self._panels) == 0: return
        (tmp,height) = self._panels[0]._label.GetSize()
        for i in range(len(self._panels)-1):
            self.SetSashPosition(i, height+4)
