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
# 2005-09-23:
#   Added SetValueDialog
# 2005-09-21:
#   fixed crash if moveing symbols/folders
# 2005-08-29:
#   add move folders.
# 2005-08-28:
#   add rename of folders
# 2005-08-26
#   added rename/move symbols feature
# 2005-06-05:
#   - fixed hidden root problem (under windows)
# 2005-05-28:
#   - fixed missing return(None) in SymbolTreePanel.OnAddSymbol() when 
#       aborting SymbolPropertyDialog.
# 2005-05-27:
#   Release as version 0.2.0 (alpha)

import wx;
from AddFolderDialog import AddFolderDialog;
from AddSymbolDialog import SelectSlotDialog, PropertyDialog;
from SetPropertyDialog import SetPropertyDialog;
from SetValueDialog import SetValueDialog;
import string;
import PPLT;
import os;
import logging;


class SymbolTreePanel(wx.TreeCtrl):
    def __init__(self, parent, PPLTSys):
        styleflags =wx.TR_NO_LINES|wx.TR_HIDE_ROOT|wx.TR_TWIST_BUTTONS|wx.TR_HAS_BUTTONS|wx.TR_FULL_ROW_HIGHLIGHT|wx.TR_EDIT_LABELS;
#       if wx.Platform == "__WXMSW__":
#           styleflags = wx.TR_NO_LINES|wx.TR_HAS_BUTTONS;
            
        wx.TreeCtrl.__init__(self, parent, -1,style = styleflags);
        self.__PPLTSys = PPLTSys;
        self.__Logger = logging.getLogger("PPLT");
        self.__DragMode = False;
        self.__DragItem = None;
        self.__ExpandTimer = wx.FutureCall(1000, self.OnTimedExpand, None);

        #load icons:
        iconp = PPLT.Config().GetBasePath()+"/icons";
        self.__IL = wx.ImageList(16,16);
        bmp = wx.Bitmap(os.path.normpath(iconp+"/folder.xpm"));
        if not bmp:
            bmp = wx.NullBitmap;
        self.__FolderIcon = self.__IL.Add(bmp);
        bmp = wx.Bitmap(os.path.normpath(iconp+"/folder2.xpm"));
        if not bmp:
            bmp = wx.NullBitmap;
        self.__FolderIcon2 = self.__IL.Add(bmp);
        bmp = wx.Bitmap(os.path.normpath(iconp+"/symbol.xpm"));
        if not bmp:
            bmp = wx.NullBitmap;
        self.__SymbolIcon = self.__IL.Add(bmp);
        self.SetImageList(self.__IL);

        self.__myRoot = self.AddRoot(_("SymbolTree (/)"));
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick);
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown);
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp);
        self.Bind(wx.EVT_MOTION, self.OnMove);
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectionChanged);
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick);
        self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.OnEditLabel);
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnStopEditLabel);
        self.Build(self.__myRoot);


    def Build(self, Item=None, Path="/"):
        if Item == None:
            Item = self.__myRoot;
        # build symbols:
        symlst = self.__PPLTSys.ListSymbols(Path);
        for sym in symlst:
            if Path[-1] == "/":
                symp = Path+sym;
            else:
                symp = Path+"/"+sym;
            slot = str(self.__PPLTSys.GetSymbolSlot(symp));
            nitem = self.AppendItem(Item, "%s  @ %s"%(sym,slot));
            self.SetPyData(nitem, (False, str(sym)));
            self.SetItemImage(nitem, self.__SymbolIcon, wx.TreeItemIcon_Normal);
            self.SortChildren(Item);

        follst = self.__PPLTSys.ListFolders(Path);
        for fol in follst:
            if Path[-1] == "/":
                folp = Path+fol;
            else:
                folp = Path+"/"+fol;
            nitem = self.AppendItem(Item, fol);
            self.SetPyData(nitem, (True, str(fol)));
            self.SetItemImage(nitem, self.__FolderIcon, wx.TreeItemIcon_Normal);
            self.SetItemImage(nitem, self.__FolderIcon2, wx.TreeItemIcon_Expanded);
            self.Build(nitem, folp);
            self.SortChildren(Item);

    def Clean(self):
        self.DeleteChildren(self.__myRoot);

    def OnCompareItems(self, item1, item2):
        Label1 = self.GetItemText(item1);
        Label2 = self.GetItemText(item2);
        (IsFolder1, Path1) = self.GetPyData(item1);
        (IsFolder2, Path2) = self.GetPyData(item2);
        if IsFolder1 and not IsFolder2: return -1;
        elif IsFolder2 and not IsFolder1: return 1;
        if Label1 > Label2: return 1;
        if Label1 == Label2: return 0;
        return -1;

    def OnRightClick(self, event):
        pt = event.GetPosition();
        (item,flag) = self.HitTest(pt);
        if not item:
            item = None;
            self.Unselect();
        else:
            self.SelectItem(item);
    
        menu = CtxMenu(self, item);
        self.PopupMenu(menu,pt);
        menu.Destroy();


    def OnDoubleClick(self, event):
        pt = event.GetPosition();
        (item, flag) = self.HitTest(pt);
        if not item:
            return(None);
        (IsFolder, Name) = self.GetPyData(item);
        if IsFolder:
            if self.IsExpanded(item):
                self.Collapse(item);
            else:
                self.Expand(item);

    def OnEditLabel(self, event):
        print event;
        item = event.GetItem();
        (IsFolder, OldName) = self.GetPyData(item);
        self.SetItemText(item, OldName)
        
    def OnStopEditLabel(self, event):
        OldItem = event.GetOldItem();
        NewItem = event.GetItem();
        print "old %s\nnew %s"%(OldItem, NewItem)
        if not OldItem: OldItem = NewItem;

        (IsFolder, OName) = self.GetPyData(OldItem);
        if event.IsEditCancelled():
            if IsFolder:
                self.SetPyData(OldItem, (IsFolder,OName));
                return;
            path = self._FindPathByItem(OldItem);
            txt = "%s  @ %s"%(OName, str(self.__PPLTSys.GetSymbolSlot(path)));
            self.SetItemText(OldItem, txt);
            self.SetPyData(OldItem, (IsFolder, OName));
            return;
        
        NName = event.GetLabel();
        OPath = self._FindPathByItem(OldItem);
        NPList = OPath.split("/")[:-1];
        NPList.append(NName);
        NPath = "/"+string.join(NPList,"/");
        if IsFolder:
            NLabel = NName;
            if not self.__PPLTSys.MoveFolder(OPath, NPath):
                event.SetEditCanceled(True);
                self.SetItemText(NewItem, OName);
                self.SetPyData(NewItem, (IsFolder, OName));
                return;
        else:
            Slot = str(self.__PPLTSys.GetSymbolSlot(OPath))
            NLabel = "%s  @ %s"%(NName, Slot);
            if not self.__PPLTSys.MoveSymbol(OPath, NPath):
                event.SetEditCanceled(True);
                txt = "%s  @ %s"%(OName, Slot);
                self.SetItemText(NewItem,txt);
                self.SetPyData(NewItem, (IsFolder, OName));
                return;
        self.SetItemText(NewItem, NLabel);
        self.SetPyData(NewItem, (IsFolder,NName));
        pitem = self.GetItemParent(NewItem);
        self.SortChildren(pitem);
        event.Veto();
        return;


    def OnLeftDown(self, event):
        pt = event.GetPosition();
        (item, flag) = self.HitTest(pt);

        if not item:
            self.Unselect();
            return(None);

        if flag&wx.TREE_HITTEST_ONITEMBUTTON:
            if self.IsExpanded(item):
                self.Collapse(item);
            else:
                self.Expand(item);
            return(None);

        self.SelectItem(item);
        (IsItemFolder, Name) = self.GetPyData(item);
        self.__DragMode = False;
        self.__DragItem = item;


    def OnLeftUp(self, event):
        self.SetCursor(wx.STANDARD_CURSOR);
        if not self.__DragMode or not self.__DragItem:
            self.__DragMode = False;
            self.__DragItem = None;
            return(None);

        self.__DragMode = False;
        DragItem = self.__DragItem;
        self.__DragItem = None;

        pt = event.GetPosition();
        (item, flags) = self.HitTest(pt);
        if not item:
            IsItemFolder = True;
            FPath = "/";
            item = self.__myRoot;
        else:
            (IsItemFolder, FName) = self.GetPyData(item);
            FPath = self._FindPathByItem(item);

        if not IsItemFolder:
            self.__DragItem = None;
            return(None);
        
        (IsDragItemFolder, ItemName) = self.GetPyData(DragItem);
        OPath = self._FindPathByItem(DragItem);
        tmpList = FPath.split("/");
        FPList = [];
        for tmp in tmpList:
            if tmp and tmp!="":
                FPList.append(tmp);
        NPList = FPList;
        NPList.append(ItemName);
        NPath = "/"+string.join(NPList,"/");
        
        if NPath == OPath:
            return(None);

        if IsDragItemFolder:
            if not self.__PPLTSys.MoveFolder(OPath, NPath):
                return(None);
        else:
            if not self.__PPLTSys.MoveSymbol(OPath,NPath):
                return(None);

        # rebuild tree
        self.Clean();
        self.Build();
        # make moved item visible
        (startItem, flag) = self.GetFirstChild(self.__myRoot);
        nitem = self._FindItemByPath(NPath, startItem);
        if nitem: self.EnsureVisible(nitem)
        #return;
        self.SortChildren(nitem);


    def OnMove(self, event):
        if not self.__DragItem :
            self.SetCursor(wx.STANDARD_CURSOR);
            return(None);
        self.SetCursor(wx.StockCursor(wx.CURSOR_HAND));
        pt = event.GetPosition();
        (item, flag) = self.HitTest(pt);
        if not item:
            self.Unselect();
            return(None);
        
        self.SelectItem(item);
        (IsFolder, Name) = self.GetPyData(item); 
        if IsFolder:
            self.__ExpandTimer.Restart(1000,item);

    def OnSelectionChanged(self, event):
        if self.__DragItem:
            self.__DragMode = True
        if self.__ExpandTimer.IsRunning():
            self.__ExpandTimer.Stop();

    def OnTimedExpand(self, Item):
        if not Item:
            return(None);
        self.Expand(Item);

    def OnAddSymbol(self, event):
        item = self.GetSelection();
        if not item or item == self.__myRoot:   # == self.__myRoot:
            item = self.__myRoot;
            ItemIsFolder = True;
            Path = "/";
        else:
            (ItemIsFolder, ItemName) = self.GetPyData(item);
            Path = self._FindPathByItem(item);
            
        dlg = SelectSlotDialog(self, self.__PPLTSys);
        if not dlg.ShowModal() == wx.ID_OK:
            dlg.Destroy();
            return(None);
        (slot, SType) = dlg.RETURN;
        dlg.Destroy();

        dlg = PropertyDialog(self, slot, SType, self.__PPLTSys);
        if not dlg.ShowModal() == wx.ID_OK:
            dlg.Destroy();
            return(None);
        name = dlg.GetName();
        stype= dlg.GetType();
        rate = dlg.GetRate();
        modus= dlg.GetModus();
        owner= dlg.GetOwner();
        group= dlg.GetGroup();
        dlg.Destroy()

        if Path != "/":
            npath = Path+"/"+name;
        else:
            npath = "/"+name;

        if not self.__PPLTSys.CreateSymbol(npath,slot, stype, modus, owner, group):
            self.__Logger.error("Error while create symbol");
            return(None);
        nitem = self.AppendItem(item, "%s  @ %s"%(name,slot));
        self.SetPyData(nitem, (False, str(name)));
        self.SetItemImage(nitem, self.__SymbolIcon, wx.TreeItemIcon_Normal);
        if item != self.__myRoot:
            self.Expand(item);
        self.SortChildren(item);

    def OnAddFolder(self, event):
        item = self.GetSelection();
        if not item or item == self.__myRoot:
            (ItemIsFolder, Path, Name) = (True,"/","");
            item = self.__myRoot;
        else:
            (ItemIsFolder, Name) = self.GetPyData(item);
            Path = self._FindPathByItem(item);
        dlg = AddFolderDialog(self, self.__PPLTSys, Path);
        ret = dlg.ShowModal();
        if not ret == wx.ID_OK:
            return(False);
        
        mod = dlg.GetModus();
        name = dlg.GetName();
        owner = dlg.GetOwner();
        group = dlg.GetGroup();

        dlg.Destroy();

        if Path != "/":
            npath = Path+"/"+name;
        else:
            npath = Path+name;
        if not self.__PPLTSys.CreateFolder(npath, "%o"%mod, owner, group):
            return(None);
        nitem = self.AppendItem(item, "%s"%name);
        self.SetPyData(nitem, (True, str(name)));
        self.SetItemImage(nitem, self.__FolderIcon, wx.TreeItemIcon_Normal);
        self.SetItemImage(nitem, self.__FolderIcon2, wx.TreeItemIcon_Expanded);
        if item != self.__myRoot:
            self.Expand(item);
        self.SortChildren(item);

    def OnRename(self, event):
        item = self.GetSelection();
        if not item:
            return(None);
        (ItemIsFolder, Name) = self.GetPyData(item);
        self.EditLabel(item);
        

    def OnDelSymbol(self, event):
        item = self.GetSelection();
        if not item:
            self.__Logger.info("Can't del root");
            return(None);
        (ItemIsFolder, Name) = self.GetPyData(item);
        Path = self._FindPathByItem(item);
        if not self.__PPLTSys.DeleteSymbol(Path):
            self.__Logger.error("Can't del symbol %s"%Path);
            return(None);
        self.Delete(item);


    def OnDelFolder(self, event):
        item = self.GetSelection();
        if not item:
            self.__Logger.info("Can't del root");
            return(None);
        (IsFolder, Name) = self.GetPyData(item);
        path = self._FindPathByItem(item);
        if not self.__PPLTSys.DeleteFolder(path):
            self.__Logger.warning("Can't del Folder %s (is it empty)"%path);
            return(None);
        self.Delete(item);


    def OnProperty(self, event):
        item = self.GetSelection();
        if not item:
            return(None);
        (IsFolder, Name) = self.GetPyData(item);
        Path = self._FindPathByItem(item);
        own = self.__PPLTSys.GetOwner(Path);
        grp = self.__PPLTSys.GetGroup(Path);
        mod = self.__PPLTSys.GetModus(Path);
        if not (own and grp and mod):
            return(None);

        dlg = SetPropertyDialog(self, self.__PPLTSys, own, grp, mod);
        ret = dlg.ShowModal();
        if not ret == wx.ID_OK:
            return(None);

        own = dlg.GetOwner();
        grp = dlg.GetGroup();
        mod = dlg.GetModus();
        dlg.Destroy();
        
        self.__PPLTSys.ChangeOwner(Path,own);
        self.__PPLTSys.ChangeGroup(Path,grp);
        self.__PPLTSys.ChangeModus(Path,mod);


    def OnSetValue(self, event):
        item = self.GetSelection();
        if not item: return None;

        Path = self._FindPathByItem(item);
        dlg = SetValueDialog(self, Path, self.__PPLTSys);
        dlg.ShowModal();
        dlg.Destroy();


    def _FindItemByPath(self, Path, StartItem):
        if not StartItem:
            return(None);
        (IsFolder, Name) = self.GetPyData(StartItem);
        myPath = self._FindPathByItem(StartItem);
        if myPath==Path:
            return(StartItem);
        if self.ItemHasChildren(StartItem):
            (childItem, flag) = self.GetFirstChild(StartItem);
            item = self._FindItemByPath(Path, childItem);
            if item: return(item);
        return(self._FindItemByPath(Path, self.GetNextSibling(StartItem)));

    def _FindPathByItem(self, Item, Path=None):
        if not Path:
            Path = list();
        if not Item or Item == self.__myRoot:
            return "/"+string.join(Path,"/");
        (IsFolder, Name) = self.GetPyData(Item);
        Path.insert(0, Name);           #prepend item
        return self._FindPathByItem(self.GetItemParent(Item),Path);
            

class CtxMenu(wx.Menu):
    def __init__(self, tree, obj=None):
        if obj == None:
            ObjIsFolder = True;
            Path = "/";
        else:
            (ObjIsFolder, Path) = tree.GetPyData(obj);      #XXX
        self.__AddSym = wx.NewId();
        self.__AddFol = wx.NewId();
        self.__DelFol = wx.NewId();
        self.__DelSym = wx.NewId();
        self.__Prop   = wx.NewId();
        self.__Rename = wx.NewId();
        self.__SetVal = wx.NewId();

        wx.Menu.__init__(self);

        if ObjIsFolder:
            item = wx.MenuItem(self, self.__AddSym, _("Add Symbol"));
            self.AppendItem(item);
            item = wx.MenuItem(self, self.__AddFol, _("Add Folder"));
            self.AppendItem(item)
        else:
            item = wx.MenuItem(self, self.__SetVal, _("Get/Set Value"));
            self.AppendItem(item);
            item = wx.MenuItem(self, self.__DelSym, _("Delete Symbol"));
            self.AppendItem(item);

        if Path != "/":
            item = wx.MenuItem(self, self.__Rename, _("Rename"));
            self.AppendItem(item);

        if ObjIsFolder and Path!="/":
            item = wx.MenuItem(self, self.__DelFol, _("Delete Folder"));
            self.AppendItem(item);
        
        if Path!="/":
            item = wx.MenuItem(self, self.__Prop, _("Properties"));
            self.AppendItem(item);

        self.Bind(wx.EVT_MENU, tree.OnAddSymbol, id = self.__AddSym);
        self.Bind(wx.EVT_MENU, tree.OnAddFolder, id = self.__AddFol);
        self.Bind(wx.EVT_MENU, tree.OnProperty,  id = self.__Prop);
        self.Bind(wx.EVT_MENU, tree.OnDelFolder, id = self.__DelFol);
        self.Bind(wx.EVT_MENU, tree.OnDelSymbol, id = self.__DelSym);
        self.Bind(wx.EVT_MENU, tree.OnRename, id = self.__Rename);
        self.Bind(wx.EVT_MENU, tree.OnSetValue, id = self.__SetVal);

