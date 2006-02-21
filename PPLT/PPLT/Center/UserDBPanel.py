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
# 2005-08-29:
#   - fixed sort-funtion:
#     now user-proxy are sorted as users
#     now sort ignore case
# 2005-08-25:
#   Add proxy-feature.
# 2005-06-04:
#   Fixed problem with hidden root item
# 2005-05-27:
#   Release as version 0.2.0 (alpha)

import PPLT;
import UserDBDialogs;
import wx;
import os;
import logging;

class UserDBPanel(wx.TreeCtrl):
    def __init__(self, Parent, PPLTSys):
        styleflags=wx.TR_NO_LINES|wx.TR_TWIST_BUTTONS|wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT;
        if wx.Platform == "__WXMSW__":
            styleflags=wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT;
            
        wx.TreeCtrl.__init__(self, Parent, -1, style=styleflags);
        self.__PPLTSys = PPLTSys;
        self.__SuperUserName = PPLTSys.GetSuperUser();
        self.__Logger = logging.getLogger("PPLT");

        self.__IL = wx.ImageList(16,16);
        iconp = PPLT.Config().GetBasePath()+"/icons";
        bmp = wx.Bitmap(os.path.normpath(iconp+"/group.xpm"));
        if not bmp:
            bmp = wx.NullBitmap;
        self.__GroupIcon = self.__IL.Add(bmp);
        bmp = wx.Bitmap(os.path.normpath(iconp+"/user.xpm"));
        if not bmp:
            bmp = wx.NullBitmap;
        self.__UserIcon = self.__IL.Add(bmp);
        bmp = wx.Bitmap(os.path.normpath(iconp+"/proxy.xpm"));
        if not bmp:
            bmp = wx.NullBitmap;
        self.__ProxyIcon = self.__IL.Add(bmp);
        bmp = wx.Bitmap(os.path.normpath(iconp+"/superuser.xpm"));
        if not bmp:
            bmp = wx.NullBitmap;
        self.__SUserIcon = self.__IL.Add(bmp);
        self.SetImageList(self.__IL);

        self.__RootItem = self.AddRoot("UserDB");
#       self.SetPyData(self.__RootItem, (True, False));
        
        self._InsertGroups();
        
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick);
        

#   def SelectRoot(self):
#       self.SelectItem(self.__RootItem);


    def _InsertGroups(self,Group=None,Item=None):
        if Item==None:
            Item = self.__RootItem;
    
        grplst = self.__PPLTSys.ListGroups(Group);
        for grp in grplst:
            nitem = self.AppendItem(Item,grp);
            self.SetItemImage(nitem,self.__GroupIcon, wx.TreeItemIcon_Normal);
            self.SetItemImage(nitem,self.__GroupIcon, wx.TreeItemIcon_Expanded);
            self.SetPyData(nitem,(True,False));
            self.SortChildren(Item);
            self._InsertGroups(grp,nitem);
            self._InsertMembers(grp,nitem);
            self._InsertProxys(grp, nitem);

    def _InsertMembers(self, Group, Item):
        memlst = self.__PPLTSys.ListMembers(Group);
        for mem in memlst:
            nitem = self.AppendItem(Item,mem);
            if self.__SuperUserName == mem:
                self.SetItemImage(nitem, self.__SUserIcon, wx.TreeItemIcon_Normal);
                self.SetPyData(nitem,(False,True));
            else:
                self.SetItemImage(nitem, self.__UserIcon, wx.TreeItemIcon_Normal);
                self.SetPyData(nitem, (False,False));
            self.SortChildren(Item);

    def _InsertProxys(self, Group, Item):
        memlst = self.__PPLTSys.ListProxys(Group);
        for mem in memlst:
            nitem = self.AppendItem(Item,mem);
            self.SetItemImage(nitem, self.__ProxyIcon, wx.TreeItemIcon_Normal);
            self.SetPyData(nitem, (True,True));
            self.SortChildren(Item);

    def __RemoveProxys(self, Name, item=None):
        if not item:
            item = self.GetFirstVisibleItem();
        else:
            (IsGroup, IsSuperUser) = self.GetPyData(item);
            IName = self.GetItemText(item);
            if IsSuperUser and IsGroup and IName==Name:
                self.Delete(item);

        if self.ItemHasChildren(item):
            (citem,c) = self.GetFirstChild(item);
            self.__RemoveProxys(Name, citem);
        
        sitem = self.GetNextSibling(item);
        if sitem:
            self.__RemoveProxys(Name, sitem);

    def OnCompareItems(self, item1, item2):
        Label1 = self.GetItemText(item1);
        Label2 = self.GetItemText(item2);
        (IsGrp1, IsSU1) = self.GetPyData(item1);
        if IsGrp1 and IsSU1: IsGrp1 = False;        # make user-paroxy handled like users
        (IsGrp2, IsSU2) = self.GetPyData(item2);
        if IsGrp2 and IsSU2: IsGrp2 = False;        # make user-paroxy handled like users
        if IsGrp1 and not IsGrp2:
            return 1;
        elif IsGrp2 and not IsGrp1:
            return -1;
        if Label1.lower() > Label2.lower():
            return 1;
        elif Label1.lower() == Label2.lower():
            return 0;
        return -1;

    def OnRightClick(self, event):
        pt = event.GetPosition();
        (item, flag) = self.HitTest(pt);
        if item:
            self.SelectItem(item);
        else:
            item = None;
            #self.SelectRoot();
            self.Unselect();

        menu = CtxMenu(self, item);
        self.PopupMenu(menu);
        menu.Destroy();



    def OnAddUser(self, Event):
        item = self.GetSelection();
#       if not item:
#           return(None);
        
        if item == None or item == self.__RootItem: #if nothing is selected:
            self.__Logger.warning("Can't create member with no group");
            return(None);
        (IsGroup, IsSuperUser) = self.GetPyData(item);
        if not IsGroup:
            return(None);
        Name = self.GetItemText(item);

        dlg = UserDBDialogs.CreateMemberDialog(self,-1,_("Create Memeber"));
        if not dlg.ShowModal() == wx.ID_OK:
            return(None);
        
        user = dlg.Name;
        pass1 = dlg.Pass1;
        pass2 = dlg.Pass2;
        dlg.Destroy();

        if not pass1 == pass2:
            self.__Logger.warning("Passwords are not equial");
            return(None);
        self.__PPLTSys.CreateMember(Name, user, pass1, "");
        nitem = self.AppendItem(item, user);
        self.SetItemImage(nitem, self.__UserIcon, wx.TreeItemIcon_Normal);
        self.SetPyData(nitem, (False,False));
        self.SortChildren(item);
        self.Expand(item);

    def OnDelUser(self, Event):
        item = self.GetSelection();
        if not item or item==self.__RootItem:
            return(None);
#       if item == self.__RootItem:
#           return(None);
        (IsGroup, IsSuperUser) = self.GetPyData(item);
        Name = self.GetItemText(item);

        if IsGroup or IsSuperUser:
            self.__Logger.warning("Can't del SuperUser");
            return(None);
        try: self.__PPLTSys.DeleteMember(Name);
        except Exception, e:
            self.__Logger.error("Unable to del user %s: %s"%(Name, str(e)));
            return;
        self.Delete(item);
        self.__RemoveProxys(Name);          #Remove all proxys of this user


    def OnAddProxy(self, Event):
        item = self.GetSelection();
        if not item or item == self.__RootItem:
            return(None);
        (IsGroup, IsSuperUser) = self.GetPyData(item);
        if not IsGroup and IsSuperUser:
            self.__Logger.warning("Selected item is not a group.");
            return(None);
        GrpName = self.GetItemText(item);

        UserList = GetUserList(self.__PPLTSys);
        Dlg = UserDBDialogs.CreateProxyDialog(self, -1, _("Create User-Proxy"), UserList);
        if not Dlg.ShowModal() == wx.ID_OK:
            return(None);

        User = Dlg.Name;
        Dlg.Destroy();
    
        try:self.__PPLTSys.CreateProxy(GrpName, User);
        except:
            self.__Logger.error("Error while create a new proxy for %s"%User);
            return;
        
        nitem = self.AppendItem(item, User);
        self.SetItemImage(nitem, self.__ProxyIcon, wx.TreeItemIcon_Normal);
        self.SetPyData(nitem, (True,True));
        self.SortChildren(item);
        self.Expand(item);

    def OnDelProxy(self, Event):
        item = self.GetSelection();
        if not item or item == self.__RootItem:
            return(None);
        (IsGroup, IsSuperUser) = self.GetPyData(item);
        if not (IsGroup and IsSuperUser):
            self.__Logger.error("Selcted item is not a userproxy.");
            return(None);
        pitem = self.GetItemParent(item);
        GrpName = self.GetItemText(pitem);
        Name = self.GetItemText(item);

        try: self.__PPLTSys.DeleteProxy(GrpName, Name);
        except:
            self.__Logger.error("Error while delete proxy for user %s"%Name);
            return;
        self.Delete(item);
        
    def OnAddGroup(self, Event):
        item = self.GetSelection();
        if not item or item == self.__RootItem:     #aka selected root
#           return(None);
#       if item == self.__RootItem:
            item = self.__RootItem;
            (IsFolder, IsSuperUser) = (True,False);
            Name = None;
        else:
            (IsFolder, IsSuperUser) = self.GetPyData(item);
            Name = self.GetItemText(item);
        if not IsFolder:
            return(None);

#       if item == self.__RootItem:
#           Name = None;
#       else:
#           Name = self.GetItemText(item);

        dlg = UserDBDialogs.CreateGroupDialog(self, -1, _("Create Group"));
        if not dlg.ShowModal() == wx.ID_OK:
            return(None);
        grp = dlg.Name;
        dlg.Destroy();

        try: self.__PPLTSys.CreateGroup(Name,grp);
        except:
            self.__Logger.warning("Error while create group %s"%grp);
            return;
        
        nitem = self.AppendItem(item,grp);
        self.SetItemImage(nitem, self.__GroupIcon, wx.TreeItemIcon_Normal);
        self.SetItemImage(nitem, self.__GroupIcon, wx.TreeItemIcon_Expanded);
        self.SetPyData(nitem, (True, False));
        if item != self.__RootItem:
            self.Expand(item);
        self.SortChildren(item);

    def OnDelGroup(self, Event):
        item = self.GetSelection();
        if not item or item==self.__RootItem:
            return(None);
#       stupid: root can't be deleted:
#       if item == self.__RootItem:
#           (IsGroup, IsSuperUser) = (True,False);
#       else:
        (IsGroup, IsSuperUser) = self.GetPyData(item);
        Name = self.GetItemText(item);
        if not IsGroup:
            return(None);
        try: self.__PPLTSys.DeleteGroup(Name);
        except:
            self.__Logger.warning("Error while delete group %s"%Name);
            return(None);
        self.Delete(item);

    def OnSetSUser(self, Event):
        item = self.GetSelection();
        if not item or item==self.__RootItem:
            return(None);
#       if item == self.__RootItem:
#           return(None);
        (IsGroup, IsSuperUser) = self.GetPyData(item);
        Name = self.GetItemText(item);
        if IsGroup or IsSuperUser:
            return(None);

        sitem = self.__GetSuperUserItem();

        try: self.__PPLTSys.SetSuperUser(Name);
        except:
            self.__Logger.warning("Error while set SuperUser to %s"%Name);
            return;
        
        self.SetPyData(sitem, (False,False));
        self.SetPyData(item, (False, True));

        self.SetItemImage(sitem, self.__UserIcon, wx.TreeItemIcon_Normal);
        self.SetItemImage(item, self.__SUserIcon, wx.TreeItemIcon_Normal);


    def OnPasswd(self, event):
        item = self.GetSelection();
        if not item or item == self.__RootItem:
            return(None);
#       if item == self.__RootItem:
#           return(None);
        (IsFolder, IsSuperUser) = self.GetPyData(item);
        if IsFolder:
            return(None);
        Name = self.GetItemText(item);
        
        dlg = UserDBDialogs.PasswdDialog(self, -1, _("Change Password of ")+Name);
        if not dlg.ShowModal() == wx.ID_OK:
            return(None);
        pass1 = dlg.Pass1;
        pass2 = dlg.Pass2;
        
        if not pass1 == pass2:
            self.__Logger.warning("Passwords are not equeal");
            return(None);
        try: self.__PPLTSys.ChangePassword(Name,pass1);
        except:
            self.__Logger.warning("Error while change passwd");
    
    
    def __GetSuperUserItem(self,item=None):
        if not item:
            item = self.GetFirstVisibleItem();
        else:
            (IsGroup, IsSuperUser) = self.GetPyData(item);
            if IsSuperUser and not IsGroup:
                return(item);

        if self.ItemHasChildren(item):
            (citem,c) = self.GetFirstChild(item);
            ret =  self.__GetSuperUserItem(citem);
            if ret:
                return(ret);
        
        sitem = self.GetNextSibling(item);
        if sitem:
            return(self.__GetSuperUserItem(sitem));





class CtxMenu(wx.Menu):
    def __init__(self, Tree, Item):
        if not Item:
            IsGroup = True;
            Name = None;
            IsSuperUser = False;
        else:
            (IsGroup, IsSuperUser) = Tree.GetPyData(Item);
            Name = Tree.GetItemText(Item);

        wx.Menu.__init__(self);

        self.__AddUsrID = wx.NewId();
        self.__AddGrpID = wx.NewId();
        self.__DelUsrID = wx.NewId();
        self.__DelGrpID = wx.NewId();
        self.__SetSUsrID= wx.NewId();
        self.__ChPassID = wx.NewId();
        self.__AddProxy = wx.NewId();
        self.__DelProxy = wx.NewId();

        if IsGroup:
            if IsSuperUser:
                item = wx.MenuItem(self, self.__DelProxy, _("Del User-Proxy"));
                self.AppendItem(item);
            else:
                if Name:
                    item = wx.MenuItem(self, self.__AddUsrID, _("Add User"));
                    self.AppendItem(item);
                    item = wx.MenuItem(self, self.__AddProxy, _("Add User-Proxy"));
                    self.AppendItem(item);
                item = wx.MenuItem(self, self.__AddGrpID, _("Add Group"));
                self.AppendItem(item);
                if Name:
                    item = wx.MenuItem(self, self.__DelGrpID, _("Del Group"));
                    self.AppendItem(item);
                
        else:
            if not IsSuperUser:
                item = wx.MenuItem(self, self.__DelUsrID, _("Del User"));
                self.AppendItem(item);
                item = wx.MenuItem(self, self.__SetSUsrID, _("Set SuperUser"));
                self.AppendItem(item);
            item = wx.MenuItem(self, self.__ChPassID, _("Change Password"));
            self.AppendItem(item);

        self.Bind(wx.EVT_MENU, Tree.OnAddUser, id = self.__AddUsrID);
        self.Bind(wx.EVT_MENU, Tree.OnDelUser, id = self.__DelUsrID);
        self.Bind(wx.EVT_MENU, Tree.OnAddGroup, id = self.__AddGrpID);
        self.Bind(wx.EVT_MENU, Tree.OnDelGroup, id = self.__DelGrpID);
        self.Bind(wx.EVT_MENU, Tree.OnSetSUser, id = self.__SetSUsrID);
        self.Bind(wx.EVT_MENU, Tree.OnPasswd, id = self.__ChPassID);
        self.Bind(wx.EVT_MENU, Tree.OnAddProxy, id = self.__AddProxy);
        self.Bind(wx.EVT_MENU, Tree.OnDelProxy, id = self.__DelProxy);



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

