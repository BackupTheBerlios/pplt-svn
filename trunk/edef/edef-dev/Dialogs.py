import wx
from Model import eDevModel

class eDevSaveAsDialog(wx.Dialog):
    def __init__(self, parent, ID, archive):
        wx.Dialog.__init__(self,parent, ID, title="Save file in archive %s"%archive)
        model = eDevModel.instance()

        box = wx.BoxSizer(wx.VERTICAL)
        
        txt = wx.StaticText(self, -1, "Save file as:")
        box.Add(txt, 0, wx.LEFT|wx.TOP|wx.RIGHT, 3)
       
        self.combo = wx.ComboBox(self, -1, choices=model.getArchives())
        self.combo.SetValue(archive)
        box.Add(self.combo, 0, wx.GROW|wx.ALL, 3)

        self.entry = wx.TextCtrl(self, -1)
        box.Add(self.entry, 0, wx.GROW|wx.ALL, 3)
        
        line = wx.StaticLine(self,-1, style=wx.LI_HORIZONTAL)
        box.Add(line,0, wx.GROW|wx.ALL, 3)
        
        btnbox = wx.StdDialogButtonSizer()
        
        ok_btn = wx.Button(self, wx.ID_OK)
        btnbox.AddButton(ok_btn)

        c_btn = wx.Button(self, wx.ID_CANCEL)
        btnbox.AddButton(c_btn)
        btnbox.Realize()
        box.Add(btnbox, 0, wx.GROW|wx.ALL, 5)
        self.SetSizer(box)
        box.Fit(self)


    def getSelection(self):
        return (self.combo.GetValue(), self.entry.GetValue())





class eDevDiscardDialog(wx.Dialog):
    def __init__(self, parent, ID):
        wx.Dialog.__init__(self, parent, ID, title="Discard changes?")

        box = wx.BoxSizer(wx.VERTICAL)
        
        txt = wx.StaticText(self, -1, "Discard changes? All work will gonna be lost!")
        box.Add(txt, 0, wx.LEFT|wx.TOP|wx.RIGHT, 3)
       
        btnbox = wx.StdDialogButtonSizer()
        
        yes_btn = wx.Button(self, wx.ID_YES)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, yes_btn)
        btnbox.AddButton(yes_btn)
        
        c_btn = wx.Button(self, wx.ID_CANCEL)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, c_btn)
        btnbox.AddButton(c_btn)
        
        btnbox.Realize()
        box.Add(btnbox, 0, wx.GROW|wx.ALL, 5)
        self.SetSizer(box)
        box.Fit(self)


    def OnButtonClick(self, evt):
        self.EndModal(evt.GetId())
