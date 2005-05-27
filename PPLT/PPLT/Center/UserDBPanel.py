import PPLT;
import UserDBDialogs;
import wx;
import os;
import logging;

class UserDBPanel(wx.TreeCtrl):
	def __init__(self, Parent, PPLTSys):
		wx.TreeCtrl.__init__(self, Parent, -1,
								style=wx.TR_NO_LINES|wx.TR_TWIST_BUTTONS|wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT);
		self.__PPLTSys = PPLTSys;
		self.__SuperUserName = PPLTSys.GetSuperUser();
		self.__Logger = logging.getLogger("PPLT");

		self.__IL = wx.ImageList(16,16);
		iconp = PPLT.Config().GetIconPath();
		bmp = wx.Bitmap(os.path.normpath(iconp+"/group.xpm"));
		if not bmp:
			bmp = wx.NullBitmap;
		self.__GroupIcon = self.__IL.Add(bmp);
		bmp = wx.Bitmap(os.path.normpath(iconp+"/user.xpm"));
		if not bmp:
			bmp = wx.NullBitmap;
		self.__UserIcon = self.__IL.Add(bmp);
		bmp = wx.Bitmap(os.path.normpath(iconp+"/superuser.xpm"));
		if not bmp:
			bmp = wx.NullBitmap;
		self.__SUserIcon = self.__IL.Add(bmp);
		self.SetImageList(self.__IL);

		self.__RootItem = self.AddRoot("UserDB");
		self.SetPyData(self.__RootItem, (True, False));
		
		self._InsertGroups();

		self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick);
		

	def SelectRoot(self):
		self.SelectItem(self.__RootItem);


	def _InsertGroups(self,Group=None,Item=None):
		if Item==None:
			Item = self.__RootItem;
	
		grplst = self.__PPLTSys.ListGroups(Group);
		for grp in grplst:
			nitem = self.AppendItem(Item,grp);
			self.SetItemImage(nitem,self.__GroupIcon, wx.TreeItemIcon_Normal);
			self.SetItemImage(nitem,self.__GroupIcon, wx.TreeItemIcon_Expanded);
			self.SetPyData(nitem,(True,False));
			self._InsertGroups(grp,nitem);
			self._InsertMembers(grp,nitem);
		
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

	def OnRightClick(self, event):
		pt = event.GetPosition();
		(item, flag) = self.HitTest(pt);
		if item:
			self.SelectItem(item);
		else:
			item = None;
			self.SelectRoot();

		menu = CtxMenu(self, item);
		self.PopupMenu(menu);
		menu.Destroy();



	def OnAddUser(self, Event):
		item = self.GetSelection();
		if not item:
			return(None);
		
		(IsGroup, IsSuperUser) = self.GetPyData(item);
		if not IsGroup:
			return(None);
		Name = self.GetItemText(item);

		dlg = UserDBDialogs.CreateMemberDialog(self,-1,"Create Memeber");
		if not dlg.ShowModal() == wx.ID_OK:
			return(None);
		
		user = dlg.Name;
		pass1 = dlg.Pass1;
		pass2 = dlg.Pass2;
		dlg.Destroy();

		if not pass1 == pass2:
			self.__Logger.warning("Passwords are not equial");
			return(None);
		if not self.__PPLTSys.CreateMember(Name, user, pass1, ""):
			self.__Logger.warning("Error while create member %s in %s"%(user,Name));
			return(None);
		nitem = self.AppendItem(item, user);
		self.SetItemImage(nitem, self.__UserIcon, wx.TreeItemIcon_Normal);
		self.SetPyData(nitem, (False,False));


	def OnDelUser(self, Event):
		item = self.GetSelection();
		if not item:
			return(None);
		(IsGroup, IsSuperUser) = self.GetPyData(item);
		Name = self.GetItemText(item);

		if IsGroup or IsSuperUser:
			self.__Logger.warning("Can't del SuperUser");
			return(None);
		if self.__PPLTSys.DeleteMember(Name):
			self.Delete(item);
		else:
			self.__Logger.warning("Error while Del User %s"%Name);


	def OnAddGroup(self, Event):
		item = self.GetSelection();
		if not item:
			return(None);
		(IsFolder, IsSuperUser) = self.GetPyData(item);
		if not IsFolder:
			return(None);

		if item == self.__RootItem:
			Name = None;
		else:
			Name = self.GetItemText(item);

		dlg = UserDBDialogs.CreateGroupDialog(self, -1, "Create Group");
		if not dlg.ShowModal() == wx.ID_OK:
			return(None);
		grp = dlg.Name;
		dlg.Destroy();

		if not self.__PPLTSys.CreateGroup(Name,grp):
			self.__Logger.warning("Error while create group %s"%grp);
			return(None);
		
		nitem = self.AppendItem(item,grp);
		self.SetItemImage(nitem, self.__GroupIcon, wx.TreeItemIcon_Normal);
		self.SetItemImage(nitem, self.__GroupIcon, wx.TreeItemIcon_Expanded);
		self.SetPyData(nitem, (True, False));


	def OnDelGroup(self, Event):
		item = self.GetSelection();
		if not item:
			return(None);
		(IsGroup, IsSuperUser) = self.GetPyData(item);
		Name = self.GetItemText(item);
		if not IsGroup:
			return(None);
		if not self.__PPLTSys.DeleteGroup(Name):
			self.__Logger.warning("Error while delete group %s"%Name);
			return(None);
		self.Delete(item);

	def OnSetSUser(self, Event):
		item = self.GetSelection();
		if not item:
			return(None);
		(IsGroup, IsSuperUser) = self.GetPyData(item);
		Name = self.GetItemText(item);
		if IsGroup or IsSuperUser:
			return(None);

		sitem = self.__GetSuperUserItem();

		if not self.__PPLTSys.SetSuperUser(Name):
			self.__Logger.warning("Error while set SuperUser to %s"%Name);
			return(None);
		
		self.SetPyData(sitem, (False,False));
		self.SetPyData(item, (False, True));

		self.SetItemImage(sitem, self.__UserIcon, wx.TreeItemIcon_Normal);
		self.SetItemImage(item, self.__SUserIcon, wx.TreeItemIcon_Normal);


	def OnPasswd(self, event):
		item = self.GetSelection();
		if not item:
			return(None);
		(IsFolder, IsSuperUser) = self.GetPyData(item);
		if IsFolder:
			return(None);
		Name = self.GetItemText(item);
		
		dlg = UserDBDialogs.PasswdDialog(self, -1, "Change Password of %s"%Name);
		if not dlg.ShowModal() == wx.ID_OK:
			return(None);
		pass1 = dlg.Pass1;
		pass2 = dlg.Pass2;
		
		if not pass1 == pass2:
			self.__Logger.warning("Passwords are not equeal");
			return(None);
		if not self.__PPLTSys.ChangePassword(Name,pass1):
			self.__Logger.warning("Error while change passwd");
	
	
	def __GetSuperUserItem(self,item=None):
		if not item:
			item = self.__RootItem;

		(IsGroup, IsSuperUser) = self.GetPyData(item);
		if IsSuperUser:
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


		if IsGroup:
			if Name:
				item = wx.MenuItem(self, self.__AddUsrID, "Add User");
				self.AppendItem(item);
			item = wx.MenuItem(self, self.__AddGrpID, "Add Group");
			self.AppendItem(item);
			if Name:
				item = wx.MenuItem(self, self.__DelGrpID, "Del Group");
				self.AppendItem(item);
		else:
			if not IsSuperUser:
				item = wx.MenuItem(self, self.__DelUsrID, "Del User");
				self.AppendItem(item);
				item = wx.MenuItem(self, self.__SetSUsrID,"Set SuperUser");
				self.AppendItem(item);
			item = wx.MenuItem(self, self.__ChPassID, "Change Password");
			self.AppendItem(item);

		self.Bind(wx.EVT_MENU, Tree.OnAddUser, id = self.__AddUsrID);
		self.Bind(wx.EVT_MENU, Tree.OnDelUser, id = self.__DelUsrID);
		self.Bind(wx.EVT_MENU, Tree.OnAddGroup, id = self.__AddGrpID);
		self.Bind(wx.EVT_MENU, Tree.OnDelGroup, id = self.__DelGrpID);
		self.Bind(wx.EVT_MENU, Tree.OnSetSUser, id = self.__SetSUsrID);
		self.Bind(wx.EVT_MENU, Tree.OnPasswd, id = self.__ChPassID);
