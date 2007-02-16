import wx
import sys
from ModuleEditorBasic import eDevModDescriptionListCtrl


class eDevDescriptionDialog(wx.Dialog):
    def __init__(self, parent, ID, title, desc_dict):
        wx.Dialog.__init__(self, parent, ID, "Edit description")
        self._desc_dict = desc_dict
        
        self._new_bmp = wx.ArtProvider_GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, (16,16))
        self._del_bmp = wx.ArtProvider_GetBitmap(wx.ART_DELETE, wx.ART_TOOLBAR, (16,16))
       
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, title)
        hbox.Add(label,1, wx.LEFT|wx.ALIGN_CENTER_VERTICAL,5)
        self._del_descr = wx.BitmapButton(self, -1, self._del_bmp, style=wx.NO_BORDER)
        hbox.Add(self._del_descr,0, wx.LEFT|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 100)
        self._add_descr = wx.BitmapButton(self, -1, self._new_bmp, style=wx.NO_BORDER)
        hbox.Add(self._add_descr,0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.onAddDesc, self._add_descr)
        self.Bind(wx.EVT_BUTTON, self.onDelDesc, self._del_descr)
        sizer.Add(hbox, 0, wx.TOP|wx.EXPAND, 10)
       

        self._desc = eDevModDescriptionListCtrl(self, -1)
        for lang in self._desc_dict.keys():
            idx = self._desc.InsertStringItem(sys.maxint, lang)
            self._desc.SetStringItem(idx,1, self._desc_dict[lang])
        self._desc.setColumnWidth([50,wx.LIST_AUTOSIZE])
        sizer.Add(self._desc, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 20)
        
        bsizer = self.CreateStdDialogButtonSizer(wx.OK|wx.CANCEL)
        sizer.Add(bsizer, 1, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,5)
        self.SetSizer(sizer)
        sizer.Fit(self)

    def onAddDesc(self, evt):
        self._desc.AddNew()
    def onDelDesc(self, evt):
        self._desc.DeleteSelected()

    def getDescriptions(self):
        descs = {}
        idx = -1
        while 1:
            idx = self._desc.GetNextItem(idx, wx.LIST_NEXT_BELOW)
            if idx < 0: break
            lang = self._desc.GetItemText(idx)
            desc = self._desc.GetItem(idx, 1).GetText()
            if not lang.strip() == "":
                descs[lang] = desc
        return descs



