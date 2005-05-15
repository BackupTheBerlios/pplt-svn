import wx;
import logging;
import sys;

class ServerSelectionDialog(wx.Dialog):
	def __init__(self, parent, PPLTSys):
		wx.Dialog.__init__(self, parent, -1, 
							"ServerSelection",
							size = wx.Size(300,250));
		self.__PPLTSys = PPLTSys;
		
		sizer = wx.BoxSizer(wx.VERTICAL);

		self.__Tree = ServerTree(self, PPLTSys);

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
				info = self.__PPLTSys.GetServerInfo(dat);
				if info:
					txt = info.GetDescription();
					self.__Help.AppendText(txt);
		
	def OnDClick(self, event):
		item = event.GetItem();
		if item:
			dat = self.__Tree.GetPyData(item);
			if dat:
				self.SelectedServer = dat;
				self.EndModal(wx.ID_OK);


class ServerTree(wx.TreeCtrl):
	def __init__(self, parent, PPLTSys):
		self.__PPLTSys = PPLTSys;
		wx.TreeCtrl.__init__(self, parent, -1);
		
		self.__Root = self.AddRoot("SDB");
		self.SetPyData(self.__Root, None);

		self.__AddServers(None, self.__Root);

	def __AddServers(self, Class, PItem):
		classes = self.__PPLTSys.ListKnownServerClasses(Class);
		for cl in classes:
			item = self.AppendItem(PItem, cl);
			self.SetPyData(item,None);
			if not Class:
				nclass = cl;
			else:
				nclass = "%s.%s"%(Class,cl);
			self.__AddServers(nclass,item);
		srvs = self.__PPLTSys.ListKnownServers(Class);
		for srv in srvs:
			item = self.AppendItem(PItem, srv);
			self.SetPyData(item, "%s.%s"%(Class,srv));

