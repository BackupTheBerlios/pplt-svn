import wx;
from ModusBox import ModusBox;


class SelectSlotDialog(wx.Dialog):
	def __init__(self, parent, PPLTSys):
		wx.Dialog.__init__(self, parent, -1, "Select DeviceSlot",size=(250,200));
		
		self.__PPLTSys = PPLTSys;

		sizer = wx.BoxSizer(wx.VERTICAL);
		
		self.__Tree = wx.TreeCtrl(self, -1,
									style =	wx.TR_HIDE_ROOT|
											wx.TR_NO_LINES|
											wx.TR_TWIST_BUTTONS|
											wx.TR_HAS_BUTTONS);
		self.__ROOT = self.__Tree.AddRoot("");
		sizer.Add(self.__Tree, 3, wx.EXPAND|wx.ALL,3);

		self.__HelpText = wx.TextCtrl(self, -1, size=(250,-1), style=wx.TE_MULTILINE);
		self.__HelpText.SetEditable(False);
		sizer.Add(self.__HelpText, 1, wx.EXPAND|wx.ALL, 3);

		self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelect, self.__Tree);

		self.SetSizer(sizer);
		sizer.Fit(self);

		self.__AddDevices();




	def OnSelect(self, event):
		item = event.GetItem();
		(iden, data, info) = self.__Tree.GetPyData(item);
		if iden == 1:
			txt = info.GetDescription();
			if txt:
				self.__HelpText.Clear();
				self.__HelpText.SetValue(txt);
		elif iden == 4:
			(fqdn, ns, name) = data;
			txt = info.GetSlotRangeDescription(ns,name);
			if txt:
				self.__HelpText.Clear();
				self.__HelpText.SetValue(txt);
		elif iden == 3:
			(fqdn, ns, name) = data;
			txt = info.GetSlotDescription(ns,name);
			if txt:
				self.__HelpText.Clear();
				self.__HelpText.SetValue(txt);
			

	def __AddDevices(self):
		devlst = self.__PPLTSys.ListDevices();
		for dev in devlst:
			print "Add device %s"%dev;
			item = self.__Tree.AppendItem(self.__ROOT,dev);
			fqdn = self.__PPLTSys.GetFQDeviceName(dev);
			info = self.__PPLTSys.GetDeviceInfo(fqdn);
			self.__Tree.SetPyData(item, (1, fqdn, info));
			self.__AddNameSpaces(item, fqdn, info);

	def __AddNameSpaces(self, pitem, fqdn, info):
		nslst = info.GetNameSpaces();
		for ns in nslst:
			item = self.__Tree.AppendItem(pitem, ns);
			self.__Tree.SetPyData(item, (2, None, info));
			self.__AddSlots(item, fqdn, ns, info);
			self.__AddSlotRanges(item, fqdn, ns, info);

	def __AddSlots(self, pitem, fqdn, ns, info):
		slst = info.GetSlots(ns);
		for s in slst:
			item = self.__Tree.AppendItem(pitem, s);
			self.__Tree.SetPyData(item, (3,(fqdn, ns, s),info));
			
	def __AddSlotRanges(self, pitem, fqdn, ns, info):
		slst = info.GetSlotRanges(ns);
		for s in slst:
			item = self.__Tree.AppendItem(pitem, s);
			self.__Tree.SetPyData(item, (4,(fqdn, ns, s),info));



