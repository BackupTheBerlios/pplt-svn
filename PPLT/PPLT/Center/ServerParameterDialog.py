# ############################################################################ #
# This is part of the PPLT project. PPLT is a framework for industrial         # 
# communication.                                                               # 
# Copyright (C) 2003-2005 Hannes Matuschek <hmatuschek@gmx.net>                # 
#                                                                              # 
# This library is free software; you can redistribute it and/or                # 
# modify it under the terms of the GNU Lesser General Public                   # 
# License as published by the Free Software Foundation; either                 # 
# version 2.1 of the License, or (at your option) any later version.           # 
#                                                                              # 
# This library is distributed in the hope that it will be useful,              # 
# but WITHOUT ANY WARRANTY; without even the implied warranty of               # 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU             # 
# Lesser General Public License for more details.                              # 
#                                                                              # 
# You should have received a copy of the GNU Lesser General Public             # 
# License along with this library; if not, write to the Free Software          # 
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA    # 
# ############################################################################ # 

#ChangeLog:
# 2005-08-25:
#   fixed layout and made ComboBox not editable
# 2005-05-27:
#   Release as version 0.2.0 (alpha)

import wx;

class ServerParameterDialog(wx.Dialog):
    def __init__(self, parent, DevName, PPLTSys):
        self.__PPLTSys = PPLTSys;
        wx.Dialog.__init__(self, parent, -1, _("Setup ")+DevName);
        self.__DevName = DevName,
        self.__Info = self.__PPLTSys.GetServerInfo(DevName);
        self.__Parameters = {};
        self.Values = {};

        self.__MySizer = wx.BoxSizer(wx.VERTICAL);
        
        label = wx.StaticText(self, -1, _("Alias: "));
        self.Alias =  wx.TextCtrl(self, -1, _("SrvName"));
        box   = wx.BoxSizer(wx.HORIZONTAL);
        box.Add(label, 1, wx.ALIGN_CENTER, 0);
        box.Add(self.Alias, 2 , wx.EXPAND, 0);
        self.__MySizer.Add(box, 0, wx.EXPAND|wx.ALL, 3);
    
        label = wx.StaticText(self, -1, _("DefautUser: "));
        usrlst = GetUserList(self.__PPLTSys);
        self.DefUser = wx.ComboBox(self, -1, str(usrlst[0]),choices=usrlst);
        self.DefUser.SetEditable(False);
        box = wx.BoxSizer(wx.HORIZONTAL);
        box.Add(label, 1, wx.ALIGN_CENTER, 0);
        box.Add(self.DefUser, 2, wx.EXPAND, 0);
        self.__MySizer.Add(box, 0, wx.EXPAND|wx.ALL, 3);

        label = wx.StaticText(self, -1, _("Root: "));
        self.Root = wx.TextCtrl(self, -1, "/");
        box = wx.BoxSizer(wx.HORIZONTAL);
        box.Add(label, 1, wx.ALIGN_CENTER, 0);
        box.Add(self.Root, 2, wx.EXPAND, 0);
        self.__MySizer.Add(box, 0, wx.EXPAND|wx.ALL, 3);

        varlist = self.__Info.GetRequiredVariableNames();
        for var in varlist:
            self.__AddEntry(var);

        ok = wx.Button(self, wx.ID_OK,_(" OK "));
        ca = wx.Button(self, wx.ID_CANCEL, _(" Cancel "));
        box = wx.BoxSizer(wx.HORIZONTAL);
        box.Add(ok, 1, wx.ALIGN_CENTER|wx.ALL, 3);
        box.Add(ca, 1, wx.ALIGN_CENTER|wx.ALL,3);
        self.__MySizer.Add(box, 1, wx.ALIGN_CENTER|wx.GROW);

        self.Bind(wx.EVT_BUTTON, self.OnOK, ok);
        self.Bind(wx.EVT_KEY_UP, self.OnKey);

        self.SetSizer(self.__MySizer);
        self.__MySizer.Fit(self);

    def OnKey(self, event):
        if event.GetKeyCode() == wx.WXK_RETURN:
            self.EndModal(wx.ID_OK);
        elif event.GetKeyCode() == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_CANCEL);

    def __AddEntry(self, var):
        defval = self.__Info.GetVariableDefaultValue(var);
        helptxt= self.__Info.GetVariableDescription(var);
        if not defval:
            defval = "";

        label  = wx.StaticText(self, -1, var+": ");
        txt    = wx.TextCtrl(self, -1, defval);
        if helptxt:
            txt.SetToolTipString(helptxt);
        box    = wx.BoxSizer(wx.HORIZONTAL);
        box.Add(label, 1, wx.ALIGN_CENTER, 0);
        box.Add(txt, 2, wx.EXPAND, 0);

        self.__MySizer.Add(box, 0, wx.ALL|wx.EXPAND, 3);
        self.__Parameters.update( {var:txt} );

    
    def OnOK(self, event):
        self.Values = {};
        for var in self.__Parameters.keys():
            val = self.__Parameters[var].GetValue();
            self.Values.update( {var:val} );
        self.EndModal(wx.ID_OK);






def GetUserList(PPLTSys, Group=None):
    lst = [];
    grplst = PPLTSys.ListGroups(Group);
    for grp in grplst:
        tmp = GetUserList(PPLTSys, grp);
        if tmp:
            lst.extend(tmp);

    tmp = PPLTSys.ListMembers(Group);
    if tmp:
        lst.extend(tmp);
    return(lst);
