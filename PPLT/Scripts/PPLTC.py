#!/usr/bin/python

#ChangeLog:
# 2005-08-27:
#	- fixed wrong getopt call
#	- added "verbose" option
# 2005-08-20:
#	- fixed problem with fileselction dialog.
# 2005-06-03:
#	+ Add save and saveas tools

import wx;
import PPLT;
import logging;
import os;
import sys;
import getopt;
from PPLT.Center.NoteBook import NoteBook;
from PPLT.Center.LogWindow import LogWindow;
from PPLT.Center.LoadBitmaps import LoadBitmaps;
from PPLT.Center.I18N import InitI18N;
from PPLT.Center.InfoFrame import InfoFrame;


class MainFrame(wx.Frame):
	def __init__(self, parent, title, PPLTSys, SFile):
		wx.Frame.__init__(self, parent, -1, title,
							pos = wx.DefaultPosition,
							size = (400,300),
							style = wx.DEFAULT_FRAME_STYLE);
		
		self.__PPLTSys = PPLTSys;
		self.__SessionFileName = SFile;
		if self.__SessionFileName:
			self.SetTitle("PPLT Center (%s)"%os.path.basename(self.__SessionFileName));

		self.__Logger = logging.getLogger("PPLT");

		bmplst = LoadBitmaps(PPLT.Config().GetIconPath());

		self.__NewID = wx.NewId();
		self.__LoadID = wx.NewId();
		self.__SaveID = wx.NewId();
		self.__SaveAsID = wx.NewId();
		self.__PackAddID = wx.NewId();
		self.__PackDelID = wx.NewId();
		self.__InfoID = wx.NewId();

		self.__ToolBar = self.CreateToolBar(wx.VERTICAL|wx.TB_FLAT);
		self.__ToolBar.AddLabelTool(self.__NewID, "New", bmplst.get("New"), shortHelp=_("New session"));
		self.__ToolBar.AddLabelTool(self.__LoadID, "Load", bmplst.get("Load"), shortHelp=_("Load a session..."));
		self.__ToolBar.AddLabelTool(self.__SaveID, "Save", bmplst.get("Save"), shortHelp=_("Save session..."));
		self.__ToolBar.AddLabelTool(self.__SaveAsID, "Save As", bmplst.get("SaveAs"), shortHelp=_("Save session as..."));
		self.__ToolBar.AddSeparator();
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
		self.Bind(wx.EVT_MENU, self.OnSave, id = self.__SaveID);
		self.Bind(wx.EVT_MENU, self.OnSaveAs, id = self.__SaveAsID);
		self.Bind(wx.EVT_MENU, self.OnNewSession, id = self.__NewID);
		self.Bind(wx.EVT_MENU, self.OnLoad, id = self.__LoadID);

	def OnInstall(self, event):
		dlg = wx.FileDialog(self, _("Select InstallFile"), wildcard=_("Install Description File (*.idf)|*.idf"));
		if not dlg.ShowModal() == wx.ID_OK:
			return(None);
		path = dlg.GetPath();
		dlg.Destroy();
		self.__PPLTSys.Install(path);

	def OnNewSession(self, event):
		self.__PPLTSys.StopAll();
		self.__NoteBook.Clean();
		self.__NoteBook.Build();
		self.__SessionFileName = None;
		self.SetTitle("PPLT Center");


	def OnLoad(self, event):
		dlg = wx.FileDialog(self, _("Select a SessionFile"), style=wx.OPEN);
		if not dlg.ShowModal() == wx.ID_OK:
			return(None);
		path = dlg.GetPath();
		if not os.path.isfile(path):
			return(None);
		self.__Logger.info("Clear Session");
		self.OnNewSession(None);
		if not self.__PPLTSys.LoadSession(path):
			self.__Logger.warning("Can't load %s"%path);
			return(None);
		self.__NoteBook.Build();
		self.__SessionFileName = path;
		self.SetTitle("PPLT Center (%s)"%os.path.basename(path));

	def OnSave(self, event):
		if not self.__SessionFileName:
			return(self.OnSaveAs(None));
		if not self.__PPLTSys.SaveSession(self.__SessionFileName):
			self.__Logger.error("Error while save session to file %s"%self.__SessionFileName);
			return(None);
		self.__Logger.info("Session Saved");

	def OnSaveAs(self, event):
		dlg = wx.FileDialog(self, _("Save Session as..."), style=wx.SAVE);
		if not dlg.ShowModal() == wx.ID_OK:
			return(None);
		path = dlg.GetPath();
		dlg.Destroy();
		if not self.__PPLTSys.SaveSession(path):
			self.__Logger.error("Error while save session to file %s"%path);
			return(None);
		self.__SessionFileName = path;
		self.SetTitle("PPLT Center (%s)"%os.path.basename(self.__SessionFileName));
		self.__Logger.info("Session saved as %s"%os.path.basename(self.__SessionFileName));

	def OnShowInfo(self, event):
		frm = InfoFrame(self);
		frm.Show();
		

class Application(wx.App):
	def __init__(self, PPLTSys, SFile):
		self.__PPLTSys = PPLTSys;
		self.__SFile = SFile;
		InitI18N();
		wx.App.__init__(self);

	def OnInit(self):
		self.RestoreStdio();
		frame = MainFrame(None,'PPLT Center',self.__PPLTSys, self.__SFile);
		self.SetTopWindow(frame);
		frame.Show(True);
		return(True);

def PrintUseage():
	print "Useage: PPLTC.py [-v] [SESSIONFILE]";


if __name__ == '__main__':
	(ops, args) = getopt.getopt(sys.argv[1:], "v");

	CoreLL = None;
	PPLTLL = None;

	for opt in ops:
		(arg, value) = opt;
		print "process %s"%arg
		if arg == "-v":
			CoreLL = "debug";
			PPLTLL = "debug";
	
	ps = PPLT.System(CoreLogLevel=CoreLL, PPLTLogLevel=PPLTLL);
	SessionFile = None;

	if len(args) >2:
		PrintUseage();
		sys.exit();
	elif len(args) == 2:
		if not os.path.isfile(args[1]):
			print "Can't open file %s"%args[1];
			sys.exit();
		if ps.LoadSession(args[1]):
			SessionFile = args[1];

	app = Application(ps, SessionFile);
	app.MainLoop();
		
