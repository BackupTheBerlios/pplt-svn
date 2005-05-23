import wx;
import ServerPanel;
import DevicePanel;
import SymbolTreePanel;
import UserDBPanel;

class NoteBook(wx.Notebook):
	def __init__(self, parent, ID, PPLTSys):
		wx.Notebook.__init__(self, parent, ID);
		self.__PPLTSys = PPLTSys;
		
		self.__SrvPanel = ServerPanel.ServerPanel(self, self.__PPLTSys);
		self.__DevPanel = DevicePanel.DevicePanel(self, self.__PPLTSys);
		self.__SymPanel = SymbolTreePanel.SymbolTreePanel(self, self.__PPLTSys);
		#self.__UDBPanel = UserDBPanel.UserDBPanel(self, self.__PPLTSys);

		self.AddPage(self.__DevPanel, "Devices");
		self.AddPage(self.__SymPanel, "SymbolTree");
		self.AddPage(self.__SrvPanel, "Server");
		#self.AddPage(self.__UDBPanel, "User DataBase");

		self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick);

	def OnRightClick(self,event):
		pt = event.GetPosition();
		(tab, flag) = self.HitTest(pt);
		if tab >= 0:
			self.SetSelection(tab);
		if tab == 0:
			menu = DevicePanel.DeviceMenu(self.__DevPanel);
			self.PopupMenu(menu, pt);
			menu.Destroy();
		elif tab == 2:
			menu = ServerPanel.ServerMenu(self.__SrvPanel);
			self.PopupMenu(menu,pt);
			menu.Destroy();

	

		

