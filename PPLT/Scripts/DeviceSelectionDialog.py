import wx;
import logging;
import sys;

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
		wx.TreeCtrl.__init__(self, parent, -1);
		
		self.__Root = self.AddRoot("DDB");
		self.SetPyData(self.__Root, None);

		self.__AddDevices(None, self.__Root);

	def __AddDevices(self, Class, PItem):
		classes = self.__PPLTSys.ListKnownDeviceClasses(Class);
		for cl in classes:
			item = self.AppendItem(PItem, cl);
			self.SetPyData(item,None);
			if not Class:
				nclass = cl;
			else:
				nclass = "%s.%s"%(Class,cl);
			self.__AddDevices(nclass,item);
		devs = self.__PPLTSys.ListKnownDevices(Class);
		for dev in devs:
			item = self.AppendItem(PItem, dev);
			self.SetPyData(item, "%s.%s"%(Class,dev));

