import wx
import logging


class NavigatorPanel( wx.Panel ):
    _label = None

    def __init__(self, parent, ID, title):
        wx.Panel.__init__(self, parent, ID)

        box = wx.BoxSizer(wx.VERTICAL)
        
        self.SetBackgroundColour(wx.Colour(0xef,0xef,0xff))
        self._label = wx.StaticText(self, -1, title)
        self._label.SetFont( wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD) )
      
        box.Add(self._label, 0, wx.ALL|wx.EXPAND, 2)
        self.SetSizer(box)

        self._label.Bind(wx.EVT_LEFT_DCLICK, self.OnActivate)
        self._logger = logging.getLogger("edef.dev")


    def OnActivate(self, evt):
        self._logger.debug("emmit EVT_NAV_ACTIVATE")
        event = NavigatorPanelActivateEvent(_event_panel_activated, self.GetId())
        event.setPanel( self )
        self.GetEventHandler().ProcessEvent(event)


class NavigatorPanelActivateEvent(wx.PyCommandEvent):
    _panel = None
    def __init(self, evtType, ID):
        wx.PyCommandEvent.__init__(self, evtType, ID)
    def setPanel(self, panel): self._panel = panel
    def getPanel(self): return self._panel

_event_panel_activated        = wx.NewEventType()
EVT_NAV_ACTIVATE = wx.PyEventBinder(_event_panel_activated, 1)
