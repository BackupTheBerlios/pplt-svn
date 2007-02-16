import wx


class ModifiedEvent(wx.PyCommandEvent):
    def __init__(self, evtType, ID):
        wx.PyCommandEvent.__init__(self, evtType, ID)
        
class PageModifiedEvent(wx.PyCommandEvent):
    def __init__(self, evtType, ID):
        self._d_current_tab = None
        wx.PyCommandEvent.__init__(self, evtType, ID)
    def SetPage(self, tab): self._d_current_tab = tab
    def GetPage(self): return self._d_current_tab

class PageChangedEvent(wx.PyCommandEvent):
    def __init__(self, evtType, ID):
        self._d_current_tab = None
        wx.PyCommandEvent.__init__(self, evtType, ID)
    def SetPage(self, tab): self._d_current_tab = tab
    def GetPage(self): return self._d_current_tab


_event_modified         = wx.NewEventType()
_event_page_modified    = wx.NewEventType()
_event_page_changed     = wx.NewEventType()

EVT_MODIFIED        = wx.PyEventBinder(_event_modified, 1)
EVT_PAGE_MODIFIED   = wx.PyEventBinder(_event_page_modified, 1)
EVT_PAGE_CHANGED    = wx.PyEventBinder(_event_page_changed, 1)
