import wx
from wx.lib.fancytext import StaticFancyText
from edef.dev import Model
import re



class SaveAsDialog(wx.Dialog):
    def __init__(self, parent, ID):
        wx.Dialog.__init__(self,parent, ID, title="Save circuit as")

        self._model = Model()

        box = wx.BoxSizer(wx.VERTICAL)

        dlg_txt = """<font size="14">Enter new (full) circuit name.</font>
            For example "class.subclass.name". A class or circuit name
            can only contain a-z, A-Z, 0-9 and _."""

        txt = StaticFancyText(self, -1, dlg_txt)
        box.Add(txt, 0, wx.ALL, 10)

        self._name = wx.TextCtrl(self, -1)
        box.Add(self._name, 1, wx.EXPAND|wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT|wx.BOTTOM, 20)

        bbox = self.CreateStdDialogButtonSizer(wx.OK|wx.CANCEL)
        box.Add(bbox, 1, wx.ALIGN_CENTER|wx.ALL, 10)

        self.SetSizer(box)
        box.Fit(self)

        self.Bind(wx.EVT_BUTTON, self.OnOk, id=wx.ID_OK)


    def validate(self, name):
        if not re.match("^[\w\_]+[\.[\w\_]+]*$", name): return False
        return True


    def circuitExists(self, name):
        uri = "circ://"+"/".join( name.split(".") )
        if self._model.checkURI(uri):
            return True
        return False


    def getSelection(self):
        # FIXME maybe we will return the uri
        return "circ://"+"/".join(self._name.GetValue().split("."))


    def OnOk(self, evt):
        name = self._name.GetValue()

        if not self.validate(name):
            wx.MessageBox("Invalid circuit name.\n"+
                           "The name should only constists of [a-zA-Z0-9_] "+
                           "seperated by dots!",
                          "Invalid circuit name", wx.OK|wx.ICON_ERROR, self, -1)
            return              
        
        if self.circuitExists(name):
            ret = wx.MessageBox("There exists allready a circuit named %s. Override?"%name,
                                "Override?", wx.YES|wx.NO|wx.ICON_QUESTION,
                                self, -1)
            if ret == wx.NO: return

        self.EndModal(wx.ID_OK)
                    


