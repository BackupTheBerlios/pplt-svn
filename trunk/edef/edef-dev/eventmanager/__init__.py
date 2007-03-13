import wx
import edef
from edef.dev import Controller
from play import getBitmap as getPlayBitmap
from pause import getBitmap as getPauseBitmap

class EventManagerComponent:
    
    __metaclass__ = edef.Singleton
    def __init__(self):
        self._controller = Controller()
        self._main_frame = self._controller.getMainFrame()
        self._event_manager = edef.EventManager()

        self._start_id = wx.NewId()
        self._pause_id = wx.NewId()
       
        # check if there is a menu "EventManager" in bar
        menu_bar = self._main_frame.GetMenuBar()
        
        if menu_bar.FindMenu("EventManager") >= 0: return

        # append
        self._menu = wx.Menu()
        menu_bar.Append(self._menu, "EventManager")
        start_item = wx.MenuItem(self._menu, self._start_id, "Start")
        pause_item = wx.MenuItem(self._menu, self._pause_id, "Pause")
        start_item.SetBitmap(getPlayBitmap())
        pause_item.SetBitmap(getPauseBitmap())
        self._menu.AppendItem(start_item)
        self._menu.AppendItem(pause_item)

        self._update_menu()

        self._main_frame.Bind(wx.EVT_MENU, self.OnStart, id=self._start_id)
        self._main_frame.Bind(wx.EVT_MENU, self.OnPause, id=self._pause_id)

    
    def _update_menu(self):
        if self._event_manager.isPaused():
            self._menu.Enable(self._start_id, True)
            self._menu.Enable(self._pause_id, False)
        else:
            self._menu.Enable(self._start_id, False)
            self._menu.Enable(self._pause_id, True)

   
    def OnStart(self, evt):
        self._event_manager.resume()
        self._update_menu()
   

    def OnPause(self, evt):
        self._event_manager.pause()
        self._update_menu()



component = EventManagerComponent
        
