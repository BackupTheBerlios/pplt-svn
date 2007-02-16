import wx
from Model import eDevModel
import Tools

class eDevSaveAsDialog(wx.Dialog):
    def __init__(self, parent, ID):
        wx.Dialog.__init__(self,parent, ID, title="Save file in")
        model = eDevModel()

        box = wx.BoxSizer(wx.VERTICAL)
        
        txt = wx.StaticText(self, -1, "Save file as:")
        box.Add(txt, 0, wx.LEFT|wx.TOP|wx.RIGHT, 3)
      
        archives = model.openURI("zip://")
        for i in range(len(archives)):
            (proto, archives[i]) = Tools.splitURI(archives[i])
        if len(archives) > 0: archive = archives[0]
        self.combo = wx.ComboBox(self, -1, choices=archives)
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



class eDevSaveModuleAsDialog(wx.Dialog):
    def __init__(self, parent, ID):
        wx.Dialog.__init__(self,parent, ID, title="Save module as")

        box = wx.BoxSizer(wx.VERTICAL)

        txt = wx.StaticText(self, -1, "Enter new (full) module name:")
        box.Add(txt, 0, wx.ALL, 10)

        self._name = wx.TextCtrl(self, -1)
        box.Add(self._name, 1, wx.EXPAND|wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT|wx.BOTTOM, 20)

        bbox = self.CreateStdDialogButtonSizer(wx.OK|wx.CANCEL)
        box.Add(bbox, 1, wx.ALIGN_CENTER|wx.ALL, 10)

        self.SetSizer(box)
        box.Fit(self)

    def getSelection(self):
        return "/".join(self._name.GetValue().split("."))


class eDevDiscardDialog(wx.Dialog):
    def __init__(self, parent, ID):
        wx.Dialog.__init__(self, parent, ID, title="Discard changes?")

        box = wx.BoxSizer(wx.VERTICAL)
        
        txt = wx.StaticText(self, -1, "Discard changes? All work will gonna be lost!")
        box.Add(txt, 0, wx.ALL, 15)
       
        btnbox = self.CreateStdDialogButtonSizer(wx.YES|wx.CANCEL)
        box.Add(btnbox, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        
        self.SetSizer(box)
        box.Fit(self)


