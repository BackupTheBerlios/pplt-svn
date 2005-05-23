import wx;
import logging;
import sys;
import PPLT;
import os;

class DeviceSelectionDialog(wx.Dialog):
	def __init__(self, parent, PPLTSys):
		wx.Dialog.__init__(self, parent, -1, 
							"DeviceSelection",
							size = wx.Size(300,250));
		self.__PPLTSys = PPLTSys;
		
		sizer = wx.BoxSizer(wx.VERTICAL);

		self.__Tree = DeviceTree(self, PPLTSys);

		self.__Help = wx.TextCtrl(self, -1, style = wx.TE_MULTILINE);
		self.__Help.SetEditable(False);

		sizer.Add(self.__Tree, 1, wx.ALIGN_CENTRE|wx.GROW, 3);
		sizer.Add(self.__Help, 0, wx.ALIGN_CENTRE|wx.GROW|wx.TOP, 3);

		self.SetSizer(sizer);
		self.SetAutoLayout(True);
		sizer.Fit(self.__Tree);

		self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelect, self.__Tree);
		self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnDClick, self.__Tree);


	def OnSelect(self, event):
		item = event.GetItem();
		if item:
			dat = self.__Tree.GetPyData(item);
			if dat:
				self.__Help.Clear();
				info = self.__PPLTSys.GetDeviceInfo(dat);
				if info:
					txt = info.GetDescription();
					self.__Help.AppendText(txt);
		
	def OnDClick(self, event):
		item = event.GetItem();
		if item:
			dat = self.__Tree.GetPyData(item);
			if dat:
				self.SelectedDevice = dat;
				self.EndModal(wx.ID_OK);


class DeviceTree(wx.TreeCtrl):
	def __init__(self, parent, PPLTSys):
		self.__PPLTSys = PPLTSys;
		wx.TreeCtrl.__init__(self, parent, -1, style=wx.TR_NO_LINES|wx.TR_HIDE_ROOT|wx.TR_TWIST_BUTTONS|wx.TR_HAS_BUTTONS);
	
		#store icons
		iconpath = PPLT.Config().GetIconPath();
		self.__IL = wx.ImageList(16,16);
		bmp = wx.Bitmap(os.path.normpath(iconpath+"/device.xpm"));
		if not bmp:
			bmp = wx.NullBitmap;
		self.__DevImg = self.__IL.Add(bmp);
		bmp = wx.Bitmap(os.path.normpath(iconpath+"/class.xpm"));
		if not bmp:
			bmp = wx.NullBitmap;
		self.__ClsImg = self.__IL.Add(bmp);
		self.SetImageList(self.__IL);
	
		self.__Root = self.AddRoot("DDB");
		self.SetPyData(self.__Root, None);

		self.__AddDevices(None, self.__Root);

	def __AddDevices(self, Class, PItem):
		classes = self.__PPLTSys.ListKnownDeviceClasses(Class);
		for cl in classes:
			item = self.AppendItem(PItem, cl);
			self.SetItemImage(item, self.__ClsImg, wx.TreeItemIcon_Normal);
			self.SetItemImage(item, self.__ClsImg, wx.TreeItemIcon_Expanded);
			self.SetPyData(item,None);
			if not Class:
				nclass = cl;
			else:
				nclass = "%s.%s"%(Class,cl);
			self.__AddDevices(nclass,item);
		devs = self.__PPLTSys.ListKnownDevices(Class);
		for dev in devs:
			item = self.AppendItem(PItem, dev);
			self.SetItemImage(item, self.__DevImg, wx.TreeItemIcon_Normal);
			self.SetItemImage(item, self.__DevImg, wx.TreeItemIcon_Normal);
			self.SetPyData(item, "%s.%s"%(Class,dev));

