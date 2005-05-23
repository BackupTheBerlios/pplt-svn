import wx;
import logging;
import sys;
import string;
from DeviceSelectionDialog import DeviceSelectionDialog;
from DeviceParameterDialog import DeviceParameterDialog;
import PPLT;
import os;

class DevicePanel(wx.ListCtrl):
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
		self.InsertColumn(1,"FQDN",width=150);
		self.InsertColumn(2,"Parameter",width=200);

		self.__IL = wx.ImageList(16,16);
		bmp = wx.Bitmap(os.path.normpath(conf.GetIconPath()+"/device.xpm"));
		if not bmp:
			bmp = wx.NullBitmap;
		self.__DevImg = self.__IL.Add(bmp);
		self.SetImageList(self.__IL, wx.IMAGE_LIST_SMALL);

		self.Bind(wx.EVT_RIGHT_UP, self.OnRightClick);

	def OnAddDevice(self, event):
		self.__Logger.debug("Add device...");
		ret = LoadADevice(self, self.__PPLTSys);
		if ret:
			(Alias, DevName, Paras) = ret;
			index = self.InsertImageStringItem(sys.maxint, Alias,self.__DevImg);
			self.SetStringItem(index, 1, DevName);
			self.SetStringItem(index, 2, Paras);
	
	def OnDelDevice(self,event):
		item = self.GetFocusedItem();
		alias = self.GetItemText(item);
		if not self.__PPLTSys.UnLoadDevice(alias):
			return(None);
		self.DeleteItem(item);

	def OnRightClick(self, event):
		pt = event.GetPosition();
		(item, flag) = self.HitTest(pt);
		if item == -1:
			menu = DeviceMenu(self);
			self.PopupMenu(menu,pt);
			menu.Destroy();
		else:
			self.Select(item);
			menu = DeviceCtxMenu(self);
			self.PopupMenu(menu,pt);
			menu.Destroy();
	

def LoadADevice(parent, PPLTSys):
	dlg = DeviceSelectionDialog(parent, PPLTSys);
	ret = dlg.ShowModal();
	if ret != wx.ID_OK:
		return(None);
	DevName = dlg.SelectedDevice;
	dlg.Destroy();
	#print "Selected Device: %s"%DevName;
	
	dlg = DeviceParameterDialog(parent, DevName, PPLTSys);
	ret = dlg.ShowModal();
	if not ret == wx.ID_OK:
		return(None);
	Alias = dlg.Alias.GetValue();
	Vals  = dlg.Values;
	dlg.Destroy();

	#print "%s as %s : %s"%(DevName, Alias, str(vals))
	if PPLTSys.LoadDevice(DevName, Alias, Vals):
		return( (Alias, DevName, ParaToString(Vals)) );
	return(None);


def ParaToString(para):
	keys = para.keys();
	keys.sort();
	lst = [];
	for key in keys:
		lst.append("%s=%s"%(key,para[key]));
	return(string.join(lst, ", "));


class DeviceMenu(wx.Menu):
	def __init__(self, parent):
		self.__ADD_ID = wx.NewId();
		wx.Menu.__init__(self);
		item = wx.MenuItem(self, self.__ADD_ID, "Add Device");
		self.AppendItem(item);
		self.Bind(wx.EVT_MENU, parent.OnAddDevice, id=self.__ADD_ID);

class DeviceCtxMenu(wx.Menu):
	def __init__(self, parent):
		self.__DEL_ID = wx.NewId();
		wx.Menu.__init__(self);
		item = wx.MenuItem(self, self.__DEL_ID, "Del Device");
		self.AppendItem(item);
		self.Bind(wx.EVT_MENU, parent.OnDelDevice, id=self.__DEL_ID);

