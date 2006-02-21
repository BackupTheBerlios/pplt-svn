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
#   2005-05-27:
#       Release as version 0.2.0 (alpha)

import wx;
import string;


class ModusBox(wx.BoxSizer):
    def __init__(self, parent, PPLTSys, usr=None, grp=None, mod="600"):
        self.__PPLTSys = PPLTSys;

        if not usr:
            self.__UserName = self.__PPLTSys.GetSuperUser();
            print "SuperUser: %s"%self.__UserName;
        else:
            self.__UserName = usr;
        
        if not grp:
            self.__GroupName = self.__PPLTSys.GetSuperUserGrp();
        else:
            self.__GroupName = grp;
        self.__UsrLST = GetUserList(PPLTSys);
        self.__GrpLST = GetGroupList(PPLTSys);

        self.__MODUS = ModStr2List(mod);

        wx.BoxSizer.__init__(self, wx.VERTICAL);
        
        label = wx.StaticText(parent, -1, _("Owner: "));
        self.Owner = wx.ComboBox(parent, -1, self.__UserName, choices=self.__UsrLST);
        self.Owner.SetEditable(False);
        box = wx.BoxSizer(wx.HORIZONTAL);
        box.Add(label, 1, wx.LEFT|wx.ALIGN_CENTER);
        box.Add(self.Owner, 3, wx.EXPAND);
        self.Add(box, 0, wx.EXPAND);
        
        label = wx.StaticText(parent, -1, _("Group: "));
        self.Group = wx.ComboBox(parent, -1, self.__GroupName, choices=self.__GrpLST);
        self.Group.SetEditable(False);
        box = wx.BoxSizer(wx.HORIZONTAL);
        box.Add(label, 1, wx.LEFT|wx.ALIGN_CENTER);
        box.Add(self.Group, 3, wx.EXPAND);
        self.Add(box, 0, wx.EXPAND);

        own  = wx.StaticText(parent, -1, _("Owner:"));
        grp  = wx.StaticText(parent, -1, _("Group:"));
        any  = wx.StaticText(parent, -1, _("Any:"));
        self.__ownr = wx.CheckBox(parent, -1, _("read"));
        self.__ownw = wx.CheckBox(parent, -1, _("write"));
        self.__grpr = wx.CheckBox(parent, -1, _("read"));
        self.__grpw = wx.CheckBox(parent, -1, _("write"));
        self.__anyr = wx.CheckBox(parent, -1, _("read"));
        self.__anyw = wx.CheckBox(parent, -1, _("write"));
        ownb = wx.BoxSizer(wx.VERTICAL);
        grpb = wx.BoxSizer(wx.VERTICAL);
        anyb = wx.BoxSizer(wx.VERTICAL);
        box  = wx.BoxSizer(wx.HORIZONTAL);
        ownb.AddMany([  (own),
                        (self.__ownr,),
                        (self.__ownw)]);
        grpb.AddMany([grp,self.__grpr,self.__grpw]);
        anyb.AddMany([any,self.__anyr,self.__anyw]);
        box.AddMany( [ownb,grpb,anyb]);
        self.Add(box, 0, wx.ALIGN_CENTER|wx.TOP,3);

        self.__SetCheckBoxes();
        
        parent.Bind(wx.EVT_CHECKBOX, self.GetCheckBoxes, self.__ownr);
        parent.Bind(wx.EVT_CHECKBOX, self.GetCheckBoxes, self.__ownw);
        parent.Bind(wx.EVT_CHECKBOX, self.GetCheckBoxes, self.__grpr);
        parent.Bind(wx.EVT_CHECKBOX, self.GetCheckBoxes, self.__grpw);
        parent.Bind(wx.EVT_CHECKBOX, self.GetCheckBoxes, self.__anyr);
        parent.Bind(wx.EVT_CHECKBOX, self.GetCheckBoxes, self.__anyw);
        parent.Bind(wx.EVT_COMBOBOX, self.UpdateGroup, self.Owner);
#       self.Fit(parent);


    def UpdateGroup(self, event):
        user = self.Owner.GetValue();
        grp = self.__PPLTSys.GetGroupByUser(user);
        if grp:
            self.Group.SetValue(grp);


    def __SetCheckBoxes(self):
        lst = [ [self.__ownr,self.__ownw, 0],
                [self.__grpr,self.__grpw, 0],
                [self.__anyr,self.__anyw, 0]];
        for n in range(0,3):
            for m in range(0,2):
                if self.__MODUS[n][m]:
                    lst[n][m].SetValue(True);
                else:
                    lst[n][m].SetValue(False);


    def GetCheckBoxes(self, event):
        lst = [ [self.__ownr,self.__ownw, 0],
                [self.__grpr,self.__grpw, 0],
                [self.__anyr,self.__anyw, 0]];
        for n in range(0,3):
            for m in range(0,2):
                if lst[n][m].GetValue():
                    self.__MODUS[n][m]=1;
                else:
                    self.__MODUS[n][m]=0;


    def GetModus(self):
        tmp = 0;
        for n in range(0,3):
            for m in range(0,3):
                tmp |= self.__MODUS[n][m]
                tmp = tmp << 1;
        return(tmp>>1);






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

def GetGroupList(PPLTSys, Group=None):
    grplst = PPLTSys.ListGroups(Group);
    for grp in grplst:
        tmp = GetGroupList(PPLTSys, grp);
        if tmp:
            grplst.extend(tmp);
    for item in grplst:
        if grplst.count(item)>1:
            grplst.remove(item);
    return(grplst);

def ModStr2List(mod):
    modus = string.atoi(mod,8);
    lst = [[0,0,0],[0,0,0],[0,0,0]];

    for n in range(2,-1,-1):
        for m in range(2,-1,-1):
            lst[n][m] = modus&0x1;
            modus = modus>>1;
    return(lst);
