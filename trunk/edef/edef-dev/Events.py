import wx


#
# Canvas Events:
#
class CanvasConnectEvent(wx.PyCommandEvent):
    _from, _to = None, None
    def __init(self, evtType, ID):
        wx.PyCommandEvent.__init__(self, evtType, ID)
    def SetFrom(self, obj): self._from=obj
    def SetTo(self, obj): self._to=obj
    def GetFrom(self): return self._from
    def GetTo(self): return self._to

class CanvasEvent(wx.PyCommandEvent):
    _coords = (0,0)
    def __init(self, evtType, ID):
        wx.PyCommandEvent.__init__(self, evtType, ID)
    def SetCoordinates(self, coords): self._coords = coords
    def GetCoordinates(self): return self._coords

class CanvasObjectEvent(CanvasEvent):
    _obj = None
    def SetObject(self, obj): self._obj=obj
    def GetObject(self): return self._obj

class CanvasMouseEvent(CanvasEvent): pass   #FIXME implement
class CanvasClick(CanvasObjectEvent): pass
class CanvasDClick(CanvasObjectEvent): pass
class CanvasRClick(CanvasObjectEvent): pass
class CanvasMouseOver(CanvasObjectEvent): pass
class CanvasMouseLeft(CanvasObjectEvent): pass
class CanvasShowToolTip(CanvasObjectEvent): pass
class CanvasHideToolTip(CanvasObjectEvent): pass
class CanvasBeginDrag(CanvasObjectEvent): pass
class CanvasDragging(CanvasEvent): pass
class CanvasEndDrag(CanvasObjectEvent): pass



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



_event_modified             = wx.NewEventType()
_event_page_modified        = wx.NewEventType()
_event_page_changed         = wx.NewEventType()

_event_canvas               = wx.NewEventType()
_event_can_mouse            = wx.NewEventType()
_event_can_click            = wx.NewEventType()
_event_can_dclick           = wx.NewEventType()
_event_can_rclick           = wx.NewEventType()
_event_can_mouse_over       = wx.NewEventType()
_event_can_mouse_left       = wx.NewEventType()
_event_can_show_tool_tip    = wx.NewEventType()
_event_can_hide_tool_tip    = wx.NewEventType()
_event_can_begin_drag       = wx.NewEventType()
_event_can_dragging         = wx.NewEventType()
_event_can_end_drag         = wx.NewEventType()
_event_can_connect          = wx.NewEventType()

EVT_MODIFIED            = wx.PyEventBinder(_event_modified, 1)
EVT_PAGE_MODIFIED       = wx.PyEventBinder(_event_page_modified, 1)
EVT_PAGE_CHANGED        = wx.PyEventBinder(_event_page_changed, 1)

EVT_CANVAS              = wx.PyEventBinder(_event_canvas, 1)
EVT_CAN_MOUSE           = wx.PyEventBinder(_event_canvas, 1)
EVT_CAN_CLICK           = wx.PyEventBinder(_event_can_click, 1)
EVT_CAN_DCLICK          = wx.PyEventBinder(_event_can_dclick, 1)
EVT_CAN_RCLICK          = wx.PyEventBinder(_event_can_rclick, 1)
EVT_CAN_MOUSE_OVER      = wx.PyEventBinder(_event_can_mouse_over, 1)
EVT_CAN_MOUSE_LEFT      = wx.PyEventBinder(_event_can_mouse_left, 1)
EVT_CAN_SHOW_TOOL_TIP   = wx.PyEventBinder(_event_can_show_tool_tip, 1)
EVT_CAN_HIDE_TOOL_TIP   = wx.PyEventBinder(_event_can_hide_tool_tip, 1)
EVT_CAN_BEGIN_DRAG      = wx.PyEventBinder(_event_can_begin_drag, 1)
EVT_CAN_DRAGGING        = wx.PyEventBinder(_event_can_dragging, 1)
EVT_CAN_END_DRAG        = wx.PyEventBinder(_event_can_end_drag, 1)
EVT_CAN_CONNECT         = wx.PyEventBinder(_event_can_connect, 1)

