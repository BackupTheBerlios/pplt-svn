#!/usr/bin/python

#ChangeLog:
# 2005-08-27:
#   - fixed wrong getopt call
#   - added "verbose" option
# 2005-08-20:
#   - fixed problem with fileselction dialog.
# 2005-06-03:
#   + Add save and saveas tools

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
from wx.html import HtmlHelpController;

class MainFrame(wx.Frame):
    def __init__(self, parent, title, PPLTSys, SFile):
        wx.Frame.__init__(self, parent, -1, title,
                            pos = wx.DefaultPosition,
                            size = (565,400),
                            style = wx.DEFAULT_FRAME_STYLE);
        

        self.__PPLTSys = PPLTSys;
        self.__SessionFileName = SFile;
        if self.__SessionFileName:
            self.SetTitle("PPLT Center (%s)"%os.path.basename(self.__SessionFileName));

        self.__Logger = logging.getLogger("PPLT");

        bmplst = LoadBitmaps(PPLT.Config().GetBasePath()+"/icons/");

        self.SetIcon(bmplst.get("Logo"));


        self.__MenuBar = wx.MenuBar();
        self.__FileMenu = wx.Menu();
        self.__NewSessionID = wx.NewId();
        self.__OpenSessionID = wx.NewId();
        self.__SaveSessionID = wx.NewId();
        self.__SaveSessionAsID = wx.NewId();
        self.__CloseID = wx.NewId();
        item = wx.MenuItem(self.__FileMenu, self.__NewSessionID, _("&New session"), _("Create a new (epmty) session."), wx.ITEM_NORMAL);
        item.SetBitmap(bmplst.get("New"));
        self.__FileMenu.AppendItem(item);
        item = wx.MenuItem(self.__FileMenu, self.__OpenSessionID, _("&Open session"), _("Open a saved session."), wx.ITEM_NORMAL);
        item.SetBitmap(bmplst.get("Load"));
        self.__FileMenu.AppendItem(item);
        item = wx.MenuItem(self.__FileMenu, self.__SaveSessionID, _("&Save session"), _("Save the current session."), wx.ITEM_NORMAL);
        item.SetBitmap(bmplst.get("Save"));
        self.__FileMenu.AppendItem(item);
        item = wx.MenuItem(self.__FileMenu, self.__SaveSessionAsID, _("Save session &as ..."), _("Save the curent session under an other filename."), wx.ITEM_NORMAL);
        item.SetBitmap(bmplst.get("SaveAs"));
        self.__FileMenu.AppendItem(item);
        self.__FileMenu.AppendSeparator();
        item = wx.MenuItem(self.__FileMenu, self.__CloseID, _("&Quit"), _("Exit the application."), wx.ITEM_NORMAL);
        item.SetBitmap(bmplst.get("Quit"));
        self.__FileMenu.AppendItem(item);
        self.__MenuBar.Append(self.__FileMenu, _("&File"));

        self.__LoadMenu = wx.Menu();
        self.__LoadServerID = wx.NewId();
        self.__LoadDeviceID = wx.NewId();
        item = wx.MenuItem(self.__LoadMenu, self.__LoadDeviceID, _("Load &device..."), _("Loads a device to the device list."), wx.ITEM_NORMAL);
        item.SetBitmap(bmplst.get("DeviceAdd"));
        self.__LoadMenu.AppendItem(item);
        item = wx.MenuItem(self.__LoadMenu, self.__LoadServerID, _("Load &server..."), _("Loads a server to the server list."), wx.ITEM_NORMAL);
        item.SetBitmap(bmplst.get("ServerAdd"));
        self.__LoadMenu.AppendItem(item);
        self.__MenuBar.Append(self.__LoadMenu, _("&Load"));

        self.__HelpMenu = wx.Menu();
        self.__HelpID = wx.NewId();
        self.__AboutID = wx.NewId();
        item = wx.MenuItem(self.__HelpMenu, self.__HelpID, _("&Help..."), _("Shows the help book..."), wx.ITEM_NORMAL);
        item.SetBitmap(bmplst.get("Help"))
        self.__HelpMenu.AppendItem(item);
        item = wx.MenuItem(self.__HelpMenu, self.__AboutID, _("&About PPLT"), _("Shows a short info like version etc ..."), wx.ITEM_NORMAL);
        item.SetBitmap(bmplst.get("Info"));
        self.__HelpMenu.AppendItem(item);
        self.__MenuBar.Append(self.__HelpMenu, _("&Help"));
        self.SetMenuBar(self.__MenuBar);

        self.__VBox = wx.SplitterWindow(self, -1);
        self.__NoteBook = NoteBook(self.__VBox, -1, self.__PPLTSys);
        self.__LogWindow = LogWindow(self.__VBox, -1, self.__PPLTSys);
        
        self.__VBox.SetMinimumPaneSize(35)
        self.__VBox.SplitHorizontally(self.__NoteBook, self.__LogWindow);
        self.__VBox.SetSashPosition(10000);
    
        self.Bind(wx.EVT_MENU, self.OnNewSession, id = self.__NewSessionID);
        self.Bind(wx.EVT_MENU, self.OnLoad, id = self.__OpenSessionID);
        self.Bind(wx.EVT_MENU, self.OnSave, id = self.__SaveSessionID);
        self.Bind(wx.EVT_MENU, self.OnSaveAs, id = self.__SaveSessionAsID);

        self.Bind(wx.EVT_MENU, self.OnClose, id = self.__CloseID);
        
        self.Bind(wx.EVT_MENU, self.OnShowInfo, id = self.__AboutID);
        self.Bind(wx.EVT_MENU, self.OnShowHelp, id = self.__HelpID);
        
        self.Bind(wx.EVT_MENU, self.OnLoadDevice, id=self.__LoadDeviceID);
        self.Bind(wx.EVT_MENU, self.OnLoadServer, id=self.__LoadServerID);



    def OnLoadDevice(self, event): self.__NoteBook.LoadDevice();
    def OnLoadServer(self, event): self.__NoteBook.LoadServer();

    def OnClose(self, event): self.Destroy();
        
        
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
        dlg = wx.FileDialog(self, _("Select a SessionFile"), style=wx.OPEN, wildcard=_("PPLT Session File (*.psf)|*.psf"));
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
        dlg = wx.FileDialog(self, _("Save Session as..."), style=wx.SAVE, wildcard=_("PPLT Session File (*.psf)|*.psf"));
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

    def OnShowHelp(self, event):
        if not self.__HelpBooksLoaded:
            self.__HelpCtrl = HtmlHelpController();
            self.__HelpBooksLoaded = True;
            if os.path.exists(os.path.normpath(self.__BasePath+"/help-%s.htb"%self.__Lang)):
                self.__HelpCtrl.AddBook(os.path.normpath(self.__BasePath+"/help-%s.htb"%self.__Lang));
            elif os.path.exists(os.path.normpath(self.__BasePath+"/help-%s.htb"%self.__AltLang)):
                self.__HelpCtrl.AddBook(os.path.normpath(self.__BasePath+"/help-%s.htb"%self.__AltLang));
            else:
                self.__HelpCtrl.AddBook(os.path.normpath(self.__BasePath+"/help-en.htb"));
        self.__HelpCtrl.DisplayID(0);


    def InitHelp(self, BasePath, Lang, AltLang):
        wx.FileSystem.AddHandler(wx.ZipFSHandler());
        self.__BasePath = BasePath;
        self.__Lang = Lang;
        self.__AltLang = AltLang;
        self.__HelpBooksLoaded = False;
        
    


class Application(wx.App):
    def __init__(self, PPLTSys, SFile, BasePath, Lang, AltLang):
        self.__BasePath = BasePath;
        self.__Lang = Lang;
        self.__AltLang = AltLang;
        self.__PPLTSys = PPLTSys;
        self.__SFile = SFile;
        InitI18N(BasePath, Lang, AltLang);
        wx.App.__init__(self);

    def OnInit(self):
        self.RestoreStdio();
        frame = MainFrame(None,'PPLT Center',self.__PPLTSys, self.__SFile);
        frame.InitHelp(self.__BasePath, self.__Lang, self.__AltLang);
        self.SetTopWindow(frame);
        frame.Show(True);
        return(True);



def PrintUseage():
    print "Useage: PPLTC.py [-v] [SESSIONFILE]";




if __name__ == '__main__':
    (ops, args) = getopt.getopt(sys.argv[1:], "v");

    CoreLL = None;
    PPLTLL = None;
    
    Config = PPLT.Config();

    for opt in ops:
        (arg, value) = opt;
        print "process %s"%arg
        if arg == "-v":
            CoreLL = "debug";
            PPLTLL = "debug";
   
    if not CoreLL: CoreLL = Config.GetCoreLogLevel();
    if not PPLTLL: PPLTLL = Config.GetPPLTLogLevel();
 
    ps = PPLT.System(BasePath=Config.GetBasePath(), CoreLogLevel=CoreLL, PPLTLogLevel=PPLTLL,
                     LogFile=Config.GetLogFile(), SysLog=Config.GetSysLog(), Lang=Config.GetLang(),
                     AltLang=Config.GetAltLang());
    SessionFile = None;

    if len(args) >1:
        PrintUseage();
        sys.exit();
    elif len(args) == 1:
        if not os.path.isfile(args[0]):
            print "Can't open file %s"%args[0];
            sys.exit();
        if ps.LoadSession(args[0]):
            SessionFile = args[0];

    app = Application(ps, SessionFile, Config.GetBasePath(), Config.GetLang(), Config.GetAltLang());
    app.MainLoop();
        
