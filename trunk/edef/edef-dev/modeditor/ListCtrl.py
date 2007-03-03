import wx
import wx.lib.mixins.listctrl as listmix
from edef.dev import Events

class eDevListCtrl(wx.ListCtrl,
                   listmix.ListCtrlAutoWidthMixin,
                   listmix.TextEditMixin):
    _d_item_data = None
    selectedItem = -1

    def __init__(self, parent, ID, sty, cols=[]):
        wx.ListCtrl.__init__(self, parent, ID, style=sty)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        for idx in range(len(cols)):
            self.InsertColumn(idx,cols[idx])
        listmix.TextEditMixin.__init__(self)
        
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onSelection)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onDeselection)
        self.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.onModified)
        
        self._d_item_data = {}

    def setColumnWidth(self, colw):
        for idx in range(len(colw)):
            self.SetColumnWidth(idx, colw[idx])

    def setItemData(self, idx, data):
        self._d_item_data[idx] = data

    def getItemData(self, idx):
        return self._d_item_data[idx]

    def delItemData(self, idx):
        if idx < 0: return
        del self._d_item_data[idx]

    def onSelection(self, evt):
        self.selectedItem = evt.GetIndex()
        evt.Skip()
    
    def onDeselection(self, evt):
        self.selectedItem = -1
        evt.Skip()

    def onModified(self, event):
        if not event.IsEditCancelled():
            evt = Events.ModifiedEvent(Events._event_modified, self.GetId())
            self.GetEventHandler().ProcessEvent(evt)
        event.Skip()



