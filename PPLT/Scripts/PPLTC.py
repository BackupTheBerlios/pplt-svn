#!/usr/bin/python
import wx;
import PPLT;
from PPLT.Center.NoteBook import NoteBook;
from PPLT.Center.LogWindow import LogWindow;
from PPLT.Center.LoadBitmaps import LoadBitmaps;
from PPLT.Center.I18N import InitI18N;
from PPLT.Center.InfoFrame import InfoFrame;


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
		self.__InfoID = wx.NewId();

		self.__ToolBar = self.CreateToolBar(wx.VERTICAL);
		#self.__ToolBar.AddLabelTool(self.__LoadID, "Load", bmplst.get("Load"), shortHelp="Load a project...");
		#self.__ToolBar.AddLabelTool(self.__SaveID, "Save", bmplst.get("Save"), shortHelp="Save this project...");
		#self.__ToolBar.AddLabelTool(self.__SaveAsID, "Save As", bmplst.get("SaveAs"), shortHelp="Save this project as...");
		#self.__ToolBar.AddSeparator();
		self.__ToolBar.AddLabelTool(self.__PackAddID, "PackAdd", bmplst.get("PackAdd"), shortHelp=_("Install Module"));
		self.__ToolBar.AddSeparator();
		self.__ToolBar.AddLabelTool(self.__InfoID, "Info", bmplst.get("Info"), shortHelp="Show Info");

		self.__ToolBar.Realize();

		self.__VBox = wx.SplitterWindow(self, -1);
		self.__NoteBook = NoteBook(self.__VBox, -1, self.__PPLTSys);
		self.__LogWindow = LogWindow(self.__VBox, -1, self.__PPLTSys);
		
		self.__VBox.SetMinimumPaneSize(35)
		self.__VBox.SplitHorizontally(self.__NoteBook, self.__LogWindow);
		self.__VBox.SetSashPosition(10000);
	
		self.Bind(wx.EVT_MENU, self.OnInstall, id = self.__PackAddID);
		self.Bind(wx.EVT_MENU, self.OnShowInfo, id = self.__InfoID);

	def OnInstall(self, event):
		dlg = wx.FileDialog(self, "Select InstallFile", wildcard="Install Description File (*.idf)|*.idf");
		if not dlg.ShowModal() == wx.ID_OK:
			return(None);
		path = dlg.GetPath();
		#print "Install: %s"%path;
		dlg.Destroy();
		self.__PPLTSys.Install(path);

	def OnShowInfo(self, event):
		frm = InfoFrame(self);
		frm.Show();
		

class Application(wx.App):
	def __init__(self, PPLTSys):
		self.__PPLTSys = PPLTSys;
		InitI18N();
		#print _("Hello world")
		wx.App.__init__(self);

	def OnInit(self):
		self.RestoreStdio();
		#print "Stdio restored...";
		#self.__PPLTSys = PPLT.System();
		frame = MainFrame(None,'PPLT Center',self.__PPLTSys);
		self.SetTopWindow(frame);
		frame.Show(True);
		return(True);

if __name__ == '__main__':
	ps = PPLT.System();
	app = Application(ps);
	app.MainLoop();
		
