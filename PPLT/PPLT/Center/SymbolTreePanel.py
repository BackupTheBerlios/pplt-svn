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
#	2005-05-27:
#		Release as version 0.2.0 (alpha)

import wx;
from AddFolderDialog import AddFolderDialog;
from AddSymbolDialog import SelectSlotDialog, PropertyDialog;
from SetPropertyDialog import SetPropertyDialog;
import PPLT;
import os;
import logging;


class SymbolTreePanel(wx.TreeCtrl):
	def __init__(self, parent, PPLTSys):
		styleflags = wx.TR_NO_LINES|wx.TR_HIDE_ROOT|wx.TR_TWIST_BUTTONS|wx.TR_HAS_BUTTONS;
		if wx.Platform == "__WXMSW__":
			styleflags = wx.TR_NO_LINES|wx.TR_HAS_BUTTONS;
			
		wx.TreeCtrl.__init__(self, parent, -1,style = styleflags);
		self.__PPLTSys = PPLTSys;
		self.__Logger = logging.getLogger("PPLT");

		#load icons:
		iconp = PPLT.Config().GetIconPath();
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

		self.__myRoot = self.AddRoot("SymbolTree (/)");
		self.SetPyData(self.__myRoot,(True,"/"));
#		self.SetItemImage(self.__myRoot,self.__FolderIcon, wx.TreeItemIcon_Normal);
#		self.SetItemImage(self.__myRoot,self.__FolderIcon2, wx.TreeItemIcon_Expanded);
		self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick);



	def OnRightClick(self, event):
		pt = event.GetPosition();
		(item,flag) = self.HitTest(pt);
		if not item:
			item = self.__myRoot;

		self.SelectItem(item);
	
		menu = CtxMenu(self, item);
		self.PopupMenu(menu,pt);
		menu.Destroy();


	def SelectRoot(self):
		self.SelectItem(self.__myRoot);

	def OnAddSymbol(self, event):
		item = self.GetSelection();
		if item == self.__myRoot:
			ItemIsFolder = True;
			Path = "/";
		else:
			(ItemIsFolder, Path) = self.GetPyData(item);

		dlg = SelectSlotDialog(self, self.__PPLTSys);
		if not dlg.ShowModal() == wx.ID_OK:
			dlg.Destroy();
			return(None);
		(slot, SType) = dlg.RETURN;
		dlg.Destroy();

		dlg = PropertyDialog(self, slot, SType, self.__PPLTSys);
		if not dlg.ShowModal() == wx.ID_OK:
			dlg.Destroy();
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
		self.SetPyData(nitem, (False, npath));
		self.SetItemImage(nitem, self.__SymbolIcon, wx.TreeItemIcon_Normal);

	def OnAddFolder(self, event):
		item = self.GetSelection();
		(ItemIsFolder, Path) = self.GetPyData(item);
		dlg = AddFolderDialog(self, self.__PPLTSys, Path);
		ret = dlg.ShowModal();
		if ret != wx.ID_OK:
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
		self.SetPyData(nitem, (True, npath));
		self.SetItemImage(nitem, self.__FolderIcon, wx.TreeItemIcon_Normal);
		self.SetItemImage(nitem, self.__FolderIcon2, wx.TreeItemIcon_Expanded);


	def OnDelSymbol(self, event):
		item = self.GetSelection();
		(ItemIsFolder, Path) = self.GetPyData(item);
		if not self.__PPLTSys.DeleteSymbol(Path):
			self.__Logger.error("Can't del symbol %s"%Path);
			return(None);
		self.Delete(item);


	def OnDelFolder(self, event):
		item = self.GetSelection();
		(IsFolder, path) = self.GetPyData(item);
		if not self.__PPLTSys.DeleteFolder(path):
			self.__Logger.warning("Can't del Folder %s (is it empty)"%path);
			return(None);
		self.Delete(item);


	def OnProperty(self, event):
		item = self.GetSelection();
		(IsFolder, Path) = self.GetPyData(item);

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




class CtxMenu(wx.Menu):
	def __init__(self, tree, obj=None):
		if obj == None:
			ObjIsFolder = True;
			Path = "/";
		else:
			(ObjIsFolder, Path) = tree.GetPyData(obj);
		self.__AddSym = wx.NewId();
		self.__AddFol = wx.NewId();
		self.__DelFol = wx.NewId();
		self.__DelSym = wx.NewId();
		self.__Prop   = wx.NewId();

		wx.Menu.__init__(self);
		if ObjIsFolder:
			item = wx.MenuItem(self, self.__AddSym, "Add Symbol");
			self.AppendItem(item);
			item = wx.MenuItem(self, self.__AddFol, "Add Folder");
			self.AppendItem(item)
		else:
			item = wx.MenuItem(self, self.__DelSym, "Delete Symbol");
			self.AppendItem(item);

		if ObjIsFolder and Path!="/":
			item = wx.MenuItem(self, self.__DelFol, "Delete Folder");
			self.AppendItem(item);
		
		if Path!="/":
			item = wx.MenuItem(self, self.__Prop, "Properties");
			self.AppendItem(item);
		self.Bind(wx.EVT_MENU, tree.OnAddSymbol, id = self.__AddSym);
		self.Bind(wx.EVT_MENU, tree.OnAddFolder, id = self.__AddFol);
		self.Bind(wx.EVT_MENU, tree.OnProperty,  id = self.__Prop);
		self.Bind(wx.EVT_MENU, tree.OnDelFolder, id = self.__DelFol);
		self.Bind(wx.EVT_MENU, tree.OnDelSymbol, id = self.__DelSym);


