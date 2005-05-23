import wx;

class ToolMenu(wx.ToolBar):
	def __init__(self, Parent, PPLTSys):
		wx.ToolBar.__init__(self, Parent, -1);
		
		self.__LoadID = wx.NewId();
		self.__SaveID = wx.NewId();
		self.__SavAsID = wx.NewId();
		self.__ModMngr = wx.NewId();

		self.AddLabelTool(self.__LoadID, "Load", wx.NullBitmap, shortHelp="Load a project");
#		self.DoAddTool(self.__SaveID, "Save", wx.NullBitmap, shortHelp="Save this project");
#		self.DoAddTool(self.__LoadID, "Save As", wx.NullBitmap, shortHelp="Save this project as ...");
#		self.DoAddTool(self.__LoadID, "Un/Install", wx.NullBitmap, shortHelp="Un/Install devices/servers/core-modules");

		self.Realize();
