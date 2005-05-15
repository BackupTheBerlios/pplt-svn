import wx;
import ServerPanel;
import DevicePanel;
import SymbolTreePanel;

class NoteBook(wx.Notebook):
	def __init__(self, parent, ID, PPLTSys):
		wx.Notebook.__init__(self, parent, ID);
		self.__PPLTSys = PPLTSys;
		
		self.__SrvPanel = ServerPanel.ServerPanel(self, self.__PPLTSys);
		self.__DevPanel = DevicePanel.DevicePanel(self, self.__PPLTSys);
		self.__SymPanel = SymbolTreePanel.SymbolTreePanel(self, self.__PPLTSys);

		self.AddPage(self.__DevPanel, "Devices");
		self.AddPage(self.__SymPanel, "SymbolTree");
		self.AddPage(self.__SrvPanel, "Server");

		self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick);

	def OnRightClick(self,event):
		pt = event.GetPosition();
		(tab, flag) = self.HitTest(pt);
		if tab >= 0:
			self.SetSelection(tab);
		if tab == 0:
			menu = DeviceMenu(self.__DevPanel);
			self.PopupMenu(menu, pt);
			menu.Destroy();
		elif tab == 2:
			menu = ServerMenu(self.__SrvPanel);
			self.PopupMenu(menu,pt);
			menu.Destroy();

	

		



class DeviceMenu(wx.Menu):
	def __init__(self, parent):
		self.__ADD_ID = wx.NewId();
		wx.Menu.__init__(self);
		item = wx.MenuItem(self, self.__ADD_ID, "Add Device");
		self.AppendItem(item);
		self.Bind(wx.EVT_MENU, parent.OnAddDevice, id=self.__ADD_ID);

class ServerMenu(wx.Menu):
	def __init__(self, parent):
		self.__ADD_ID = wx.NewId();
		wx.Menu.__init__(self);
		item = wx.MenuItem(self, self.__ADD_ID, "Add Server");
		self.AppendItem(item);
		self.Bind(wx.EVT_MENU, parent.OnAddServer, id=self.__ADD_ID);

