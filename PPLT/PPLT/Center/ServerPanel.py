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
import logging;
import sys;
import string;
from ServerSelectionDialog import ServerSelectionDialog;
from ServerParameterDialog import ServerParameterDialog;
import PPLT;
import os;

class ServerPanel(wx.ListCtrl):
    def __init__(self, parent, PPLTSys):
        wx.ListCtrl.__init__(self, parent, -1,
                                style=wx.LC_REPORT|
                                        wx.LC_HRULES|
                                        wx.BORDER_SUNKEN|
                                        wx.LC_SINGLE_SEL);
        conf = PPLT.Config();

        self.__PPLTSys = PPLTSys;
        self.__Logger = logging.getLogger("PPLT");
        self.Fit();
        self.InsertColumn(0,_("Alias"));
        self.InsertColumn(1,_("FQSN"),width=100);
        self.InsertColumn(2,_("DefaultUser"));
        self.InsertColumn(3,_("Root"));
        self.InsertColumn(4,_("Parameter"),width=200);

        self.__IL = wx.ImageList(16,16);
        bmp = wx.Bitmap(os.path.normpath(conf.GetBasePath()+"/icons/server.xpm"));
        if not bmp:
            bmp = wx.NullBitmap;
        self.__SrvImg = self.__IL.Add(bmp);
        self.SetImageList(self.__IL,wx.IMAGE_LIST_SMALL);

        self.Bind(wx.EVT_RIGHT_UP, self.OnRightClick);

        self.Build();


    def Build(self):
        srvlst = self.__PPLTSys.ListRunningServers();
        for srv in srvlst:
            fqsn = self.__PPLTSys.GetFQServerName(srv);
            user = self.__PPLTSys.GetServerDefaultUser(srv);
            para = self.__PPLTSys.GetServerParameters(srv);
            root = self.__PPLTSys.GetServerRoot(srv);
            parastr = ParaToString(para);
            index = self.InsertImageStringItem(sys.maxint, srv,self.__SrvImg);
            self.SetStringItem(index, 1, fqsn);
            self.SetStringItem(index, 2, user);
            self.SetStringItem(index, 3, root);
            self.SetStringItem(index, 4, parastr);

    def Clean(self):
        self.DeleteAllItems();

    def OnAddServer(self, event):
        self.__Logger.debug("Add Server...");
        ret = LoadAServer(self, self.__PPLTSys);
        if ret:
            (Alias, SrvName, DefUser, Paras, Root) = ret;
            index = self.InsertImageStringItem(sys.maxint, Alias,self.__SrvImg);
            self.SetStringItem(index, 1, SrvName);
            self.SetStringItem(index, 2, DefUser);
            self.SetStringItem(index, 3, Root);
            self.SetStringItem(index, 4, Paras);

    def OnStopServer(self, event):
        item = self.GetFocusedItem();
        alias = self.GetItemText(item);
        if not self.__PPLTSys.UnLoadServer(alias):
            return(None);
        self.DeleteItem(item);

    def OnRightClick(self, event):
        pt = event.GetPosition();
        (item, flag) = self.HitTest(pt);
        if item == -1:
            menu = ServerMenu(self);
            self.PopupMenu(menu);
            menu.Destroy();
        else:
            self.Select(item);
            menu = ServerCtxMenu(self);
            self.PopupMenu(menu);
            menu.Destroy();


    
def LoadAServer(parent, PPLTSys):
    dlg = ServerSelectionDialog(parent, PPLTSys);
    ret = dlg.ShowModal();
    if ret != wx.ID_OK:
        return(None);
    SrvName = dlg.SelectedServer;
    dlg.Destroy();
    #print "Selected Server: %s"%SrvName;
    
    dlg = ServerParameterDialog(parent, SrvName, PPLTSys);
    ret = dlg.ShowModal();
    if not ret == wx.ID_OK:
        return(None);
    Alias = dlg.Alias.GetValue();
    DefUser = dlg.DefUser.GetValue();
    Vals  = dlg.Values;
    Root  = dlg.Root.GetValue();
    dlg.Destroy();

    #print "%s as %s(%s) : %s"%(SrvName, Alias, DefUser,str(Vals))
    if PPLTSys.LoadServer(SrvName, Alias, DefUser, Vals, Root):
        return( (Alias, SrvName, DefUser, ParaToString(Vals),Root) );
    return(None);


def ParaToString(para):
    keys = para.keys();
    keys.sort();
    lst = [];
    for key in keys:
        lst.append("%s=%s"%(key,para[key]));
    return(string.join(lst, ", "));




class ServerMenu(wx.Menu):
    def __init__(self, parent):
        self.__ADD_ID = wx.NewId();
        wx.Menu.__init__(self);
        item = wx.MenuItem(self, self.__ADD_ID, _("Add Server"));
        self.AppendItem(item);
        self.Bind(wx.EVT_MENU, parent.OnAddServer, id=self.__ADD_ID);

class ServerCtxMenu(wx.Menu):
    def __init__(self, parent):
        self.__DEL_ID = wx.NewId();
        wx.Menu.__init__(self);
        item = wx.MenuItem(self, self.__DEL_ID, _("Stop Server"));
        self.AppendItem(item);
        self.Bind(wx.EVT_MENU, parent.OnStopServer, id=self.__DEL_ID);

