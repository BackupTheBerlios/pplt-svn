#!/usr/bin/python
import wx;
import PPLT;
from NoteBook import NoteBook;
from LogWindow import LogWindow;
from LoadBitmaps import LoadBitmaps;




class MainFrame(wx.Frame):
	def __init__(self, parent, title,PPLTSys):
		wx.Frame.__init__(self, parent, -1, title,
							pos = wx.DefaultPosition,
							size = wx.DefaultSize,
							style = wx.DEFAULT_FRAME_STYLE);
		
		self.__PPLTSys = PPLTSys;
		bmplst = LoadBitmaps(PPLT.Config().GetIconPath());

		self.__LoadID = wx.NewId();
		self.__SaveID = wx.NewId();
		self.__SaveAsID = wx.NewId();
		self.__PackAddID = wx.NewId();
		self.__PackDelID = wx.NewId();

		self.__ToolBar = self.CreateToolBar(wx.VERTICAL);
		#self.__ToolBar.AddLabelTool(self.__LoadID, "Load", bmplst.get("Load"), shortHelp="Load a project...");
		#self.__ToolBar.AddLabelTool(self.__SaveID, "Save", bmplst.get("Save"), shortHelp="Save this project...");
		#self.__ToolBar.AddLabelTool(self.__SaveAsID, "Save As", bmplst.get("SaveAs"), shortHelp="Save this project as...");
		#self.__ToolBar.AddSeparator();
		self.__ToolBar.AddLabelTool(self.__PackAddID, "PackAdd", bmplst.get("PackAdd"), shortHelp="Module Install.");
		self.__ToolBar.AddLabelTool(self.__PackDelID, "PackDel", bmplst.get("PackDel"), shortHelp="Module Uninstall");

		self.__ToolBar.Realize();

		self.__VBox = wx.SplitterWindow(self, -1);
		self.__NoteBook = NoteBook(self.__VBox, -1, self.__PPLTSys);
		self.__LogWindow = LogWindow(self.__VBox, -1, self.__PPLTSys);
		
		self.__VBox.SetMinimumPaneSize(20)
		self.__VBox.SplitHorizontally(self.__NoteBook, self.__LogWindow);
		self.__VBox.SetSashPosition(10000);


class Application(wx.App):
	def __init__(self, PPLTSys):
		self.__PPLTSys = PPLTSys;
		wx.App.__init__(self);

	def OnInit(self):
		#self.__PPLTSys = PPLT.System();
		frame = MainFrame(None,'PPLT Center',self.__PPLTSys);
		self.SetTopWindow(frame);
		frame.Show(True);
		return(True);

if __name__ == '__main__':
	ps = PPLT.System();
	app = Application(ps);
	app.MainLoop();
		
