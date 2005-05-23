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
		self.InsertColumn(0,"Alias");
		self.InsertColumn(1,"FQSN",width=100);
		self.InsertColumn(2,"DefaultUser");
		self.InsertColumn(3,"Parameter",width=200);

		self.__IL = wx.ImageList(16,16);
		bmp = wx.Bitmap(os.path.normpath(conf.GetIconPath()+"/server.xpm"));
		if not bmp:
			bmp = wx.NullBitmap;
		self.__SrvImg = self.__IL.Add(bmp);
		self.SetImageList(self.__IL,wx.IMAGE_LIST_SMALL);

		self.Bind(wx.EVT_RIGHT_UP, self.OnRightClick);


	def OnAddServer(self, event):
		self.__Logger.debug("Add Server...");
		ret = LoadAServer(self, self.__PPLTSys);
		if ret:
			(Alias, SrvName, DefUser, Paras) = ret;
			index = self.InsertImageStringItem(sys.maxint, Alias,self.__SrvImg);
			self.SetStringItem(index, 1, SrvName);
			self.SetStringItem(index, 2, DefUser);
			self.SetStringItem(index, 3, Paras);

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
	dlg.Destroy();

	#print "%s as %s(%s) : %s"%(SrvName, Alias, DefUser,str(Vals))
	if PPLTSys.LoadServer(SrvName, Alias, DefUser, Vals):
		return( (Alias, SrvName, DefUser, ParaToString(Vals)) );
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
		item = wx.MenuItem(self, self.__ADD_ID, "Add Server");
		self.AppendItem(item);
		self.Bind(wx.EVT_MENU, parent.OnAddServer, id=self.__ADD_ID);

class ServerCtxMenu(wx.Menu):
	def __init__(self, parent):
		self.__DEL_ID = wx.NewId();
		wx.Menu.__init__(self);
		item = wx.MenuItem(self, self.__DEL_ID, "Stop Server");
		self.AppendItem(item);
		self.Bind(wx.EVT_MENU, parent.OnStopServer, id=self.__DEL_ID);

