import os
import os.path
from edef import Singleton
import ConfigParser
import wx


class eDevConfig:
    __metaclass__ = Singleton
    def __init__(self):
        self._d_base_path = os.path.abspath(os.path.expanduser("~/.edef"))
        self._d_config_path = os.path.join(self._d_base_path, "edef-developer.conf")

        if not os.path.isfile(self._d_config_path):
            _create_std_config_file(self._d_config_path)

        self._d_config = ConfigParser.ConfigParser()
        self._d_config.read( [self._d_config_path] )
        
   
    def save(self):
        f = open(self._d_config_path,"w")
        self._d_config.write(f)
        f.close()

    
    def getEditorTabSpace(self):
        if not self._d_config.has_option("Editor","TabSpace"): return 4
        return self._d_config.getint("Editor","TabSpace")
    def setEditorTabSpace(self, val=4):
        self._d_config.set("Editor","TabSpace",str(val))

    def getEditorExpandTab(self):
        if not self._d_config.has_option("Editor","ExpandTab"): return True
        return self._d_config.getboolean("Editor","ExpandTab")
    def setEditorExpandTab(self, val=True):
        self._d_config.set("Editor","ExpandTab",str(val))

    def getEditorFont(self):
        if not self._d_config.has_option("Editor","Font"): return "Courier"
        return self._d_config.get("Editor","Font")
    def setEditorFont(self, val="Courier"):
        self._d_config.set("Editor","Font",str(val))

    def getEditorFontSize(self):
        if not self._d_config.has_option("Editor","FontSize"): return 8
        return self._d_config.getint("Editor","FontSize")
    def setEditorFontSize(self, val=8):
        self._d_config.set("Editor","FontSize",str(val))

    def getEditorSecondFontSize(self):
        fs = self.getEditorFontSize()
        if fs-2 < 0: return fs
        return fs-2



class _FontSelection(wx.FontEnumerator):
    _d_fonts = []

    def OnFacename(self,name):
        self._d_fonts.append(name)
        return True



class eDevConfigDialog(wx.Dialog):

    def __init__(self, parent, ID):
        wx.Dialog.__init__(self, parent, ID, "Editor settings")
        self._config = eDevConfig()

        box = wx.BoxSizer(wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        txt = wx.StaticText(self, -1, "Font")
        hbox.Add(txt, 1, wx.LEFT|wx.RIGHT|wx.TOP|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT, 5)
        fontsel = _FontSelection()
        fontsel.EnumerateFacenames(fixedWidthOnly=True)
        self._font = wx.ComboBox(self, -1, self._config.getEditorFont(),
                                 choices=fontsel._d_fonts, style=wx.CB_DROPDOWN|wx.CB_READONLY|wx.CB_SORT)
        hbox.Add(self._font, 0, wx.TOP|wx.RIGHT, 5)
        box.Add(hbox, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 10)
       
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        txt = wx.StaticText(self, -1, "Font size")
        hbox.Add(txt, 1, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT, 5)
        self._fontsize = wx.SpinCtrl(self, -1)
        self._fontsize.SetRange(3,25)
        self._fontsize.SetValue(self._config.getEditorFontSize())
        hbox.Add(self._fontsize, 0, wx.RIGHT, 5)
        box.Add(hbox, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 10)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        txt = wx.StaticText(self, -1, "Tab space")
        hbox.Add(txt, 1, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT, 5)
        self._tabsp = wx.SpinCtrl(self, -1)
        self._tabsp.SetRange(1,16)
        self._tabsp.SetValue(self._config.getEditorTabSpace())
        hbox.Add(self._tabsp, 0, wx.RIGHT, 5)
        box.Add(hbox, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 10)
   
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        txt = wx.StaticText(self, -1, "Expand tabs")
        hbox.Add(txt, 1, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT, 5)
        self._exptab = wx.CheckBox(self, -1)
        self._exptab.SetValue(self._config.getEditorExpandTab())
        hbox.Add(self._exptab, 0, wx.RIGHT, 5)
        box.Add(hbox, 0, wx.EXPAND|wx.ALL, 10)
        

        bbox = self.CreateStdDialogButtonSizer(wx.OK|wx.CANCEL)
        box.Add(bbox, 0, wx.EXPAND|wx.ALL|wx.CENTER, 10)

        self.SetSizer(box)
        box.Fit(self)

        self.Bind(wx.EVT_BUTTON, self.OnOK, id=wx.ID_OK)


    def OnOK(self, evt):
        self._config.setEditorFont(self._font.GetValue())
        self._config.setEditorFontSize(self._fontsize.GetValue())
        self._config.setEditorTabSpace(self._tabsp.GetValue())
        self._config.setEditorExpandTab(self._exptab.GetValue())

        self._config.save()
        self.EndModal(wx.ID_OK)


def _create_std_config_file(path):
    cfg = """
[Editor]
TabSpace=4
ExpandTab=True
Font=Courier
FontSize=10
"""

    f = open(path,"w")
    f.write(cfg)
    f.close()


