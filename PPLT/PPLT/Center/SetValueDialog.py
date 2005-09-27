import wx;
import time;

class SetValueDialog(wx.Dialog):
    def __init__(self, Parent, Path, PPLTSys):
        self.__PPLTSys = PPLTSys;
        self.__Path = Path;

        wx.Dialog.__init__(self, Parent, -1, _("Set Value"));
        Value = str(PPLTSys.GetValue(Path));


        VBox = wx.BoxSizer(wx.VERTICAL);

        hbox = wx.BoxSizer(wx.HORIZONTAL);
        label = wx.StaticText(self, -1, _("Value: "));
        self.__Value = wx.TextCtrl(self, -1, Value);
        self.__Set = wx.Button(self, -1, _("Set"), size=(50,25));
        self.__Set.SetSize(self.__Set.GetBestSize());
        hbox.Add(label, 0, wx.ALIGN_CENTER|wx.RIGHT, 10)
        hbox.Add(self.__Value, 1, wx.ALIGN_CENTER|wx.RIGHT, 3);
        hbox.Add(self.__Set, 0, wx.ALIGN_CENTER, 0);
        VBox.Add(hbox, 0, wx.ALL|wx.GROW, 5);
       
        hbox = wx.BoxSizer(wx.HORIZONTAL);
        label = wx.StaticText(self, -1, _("Type: "));
        t = wx.StaticText(self, -1, PPLTSys.GetSymbolType(Path));
        hbox.Add(label, 0, wx.ALIGN_CENTER|wx.RIGHT, 10);
        hbox.Add(t, 1, wx.ALIGN_CENTER,0);
        VBox.Add(hbox, 0, wx.GROW|wx.LEFT|wx.RIGHT, 5);
        
        hbox = wx.BoxSizer(wx.HORIZONTAL);
        label = wx.StaticText(self, -1, _("Time: "));
        txt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(PPLTSys.GetSymbolTimeStamp(Path)));
        t = wx.StaticText(self, -1, txt);
        hbox.Add(label, 0, wx.ALIGN_CENTER|wx.RIGHT, 10);
        hbox.Add(t, 1, wx.ALIGN_CENTER,0);
        VBox.Add(hbox, 0, wx.GROW|wx.LEFT|wx.RIGHT|wx.TOP, 5);
        hl = wx.StaticLine(self, -1);
        VBox.Add(hl, 0, wx.GROW|wx.TOP, 10);

        hbox = wx.BoxSizer(wx.HORIZONTAL);
        ca = wx.Button(self, wx.ID_CANCEL, _("Close"));
        hbox.Add(ca, 1, wx.ALL, 5);
        VBox.Add(hbox, 0, wx.GROW|wx.TOP, 3);
        
        self.Bind(wx.EVT_BUTTON, self.OnSet, self.__Set);
        
        self.SetSizer(VBox);
        VBox.Fit(self);

    def OnSet(self, event):
        Val = self.__Value.GetValue();
        
        Type = self.__PPLTSys.GetSymbolType(self.__Path);
        
        if Type in ("Bool", "Integer", "uInteger", "uLong", "Long"): Val = int(Val);
        elif Type in ("Float","Double"): Val = float(Val);
        elif Type == "String": Val = str(Val);
        else: return None;

        if not self.__PPLTSys.SetValue(self.__Path, Val):
            dlg = wx.MessageDialog(self, _("Error while set value of symbol ")+self.__Path, _("Error while set value"), wx.OK|wx.ICON_ERROR);
            dlg.ShowModal();
            dlg.Destroy();
            return
        Val = self.__PPLTSys.GetValue(self.__Path);
        self.__Value.SetValue(str(Val));
        
