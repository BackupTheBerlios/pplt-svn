#!/usr/bin/python
from PPLT.ModSrc import DataBase;
import PPLT;
from PPLT.ModSrc import Set
import wx;
import os.path;
import sys;
from PPLT.ModSrc.ModInstallList import ModInstallList;
from PPLT.Center.I18N import InitI18N;

class ReposSelectionDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, _("Select a repositority..."));
        VBox = wx.BoxSizer(wx.VERTICAL);
    
        txt = wx.StaticText(self, -1, _(" Select Repositorities"))
        font = wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD);
        txt.SetFont(font);
        VBox.Add(txt, 0, wx.TOP,5)
        self.StdHTTPRepos = wx.CheckBox(self, -1, _("Default PPLT Module Responsidority (HTTP)"))
        self.StdHTTPRepos.SetValue(True);
        self.StdFTPRepos = wx.CheckBox(self, -1, _("Default PPLT Module Responsidority (FTP)"))
        self.StdFTPRepos.SetValue(False);
        VBox.Add(self.StdHTTPRepos,1, wx.EXPAND|wx.LEFT, 3);
        VBox.Add(self.StdFTPRepos,1, wx.EXPAND|wx.LEFT, 3);
        box = wx.BoxSizer(wx.HORIZONTAL);
        self.AddURLRepos = wx.CheckBox(self, -1, _("Other URL: "));
        self.AddURLRepos.SetValue(False);
        self.URLRepos = wx.TextCtrl(self,-1,"proto://host/path_to_repos");
        self.URLRepos.Disable();
        box.Add(self.AddURLRepos, 0, wx.ALIGN_CENTER);
        box.Add(self.URLRepos, 1, wx.RIGHT, 10);
        VBox.Add(box, 1, wx.EXPAND|wx.LEFT, 3)
        box = wx.BoxSizer(wx.HORIZONTAL);
        self.AddFileRepos = wx.CheckBox(self, -1, _("Local File: "));
        self.AddFileRepos.SetValue(False)
        self.FileRepos = wx.TextCtrl(self,-1);
        self.FileRepos.Disable();
        self.FSB = wx.Button(self, -1, "...", style=wx.BU_EXACTFIT);
        self.FSB.Disable();
        box.Add(self.AddFileRepos, 0, wx.ALIGN_CENTER);
        box.Add(self.FileRepos, 1, wx.RIGHT|wx.ALIGN_CENTER, 3);
        box.Add(self.FSB, 0, wx.RIGHT|wx.ALIGN_CENTER, 10)
        VBox.Add(box, 1, wx.EXPAND|wx.LEFT, 3)
        
        txt = wx.StaticText(self, -1, _(" Options: "))
        font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)
        txt.SetFont(font);
        VBox.Add(txt, 0, wx.TOP, 15)
        box = wx.BoxSizer(wx.HORIZONTAL);
        self.FollowLinks = wx.CheckBox(self, -1, _("Follow links"))
        self.FollowLinks.SetValue(True);
        box.Add(self.FollowLinks, 1, wx.ALIGN_LEFT|wx.ALL, 3);
        self.FollowOtherSite = wx.CheckBox(self, -1, _("Follow also links to other sides."))
        self.FollowOtherSite.SetValue(False);
        box.Add(self.FollowOtherSite, 1, wx.ALIGN_RIGHT|wx.LEFT, 3);
        VBox.Add(box, 0, wx.RIGHT, 3)
    
        line = wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL);
        VBox.Add(line, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 5)
    
        self.Bind(wx.EVT_CHECKBOX, self.ToggleFollowLinks, self.FollowLinks);
        self.Bind(wx.EVT_CHECKBOX, self.ToggleAddURL, self.AddURLRepos);
        self.Bind(wx.EVT_CHECKBOX, self.ToggleAddFile, self.AddFileRepos);
        self.Bind(wx.EVT_BUTTON, self.SelectFile, self.FSB);
    
        box = wx.BoxSizer(wx.HORIZONTAL);
        ok = wx.Button(self, wx.ID_OK, "OK");
        ca = wx.Button(self, wx.ID_CANCEL, "Cancel");
        box.Add(ca, wx.ALL|wx.ALIGN_LEFT|wx.GROW, 3);
        box.Add(ok, wx.ALL|wx.ALIGN_RIGHT|wx.GROW, 3);
        VBox.Add(box, 1, wx.TOP|wx.GROW, 0)
        self.SetSizer(VBox);
        VBox.Fit(self);

    def ToggleFollowLinks(self, event):
        cb = event.GetEventObject();
        if not cb.GetValue(): self.FollowOtherSite.Disable();
        else: self.FollowOtherSite.Enable();
    def ToggleAddURL(self, event):
        cb = event.GetEventObject();
        if not cb.GetValue(): self.URLRepos.Disable();
        else: self.URLRepos.Enable();
    def ToggleAddFile(self, event):
        cb = event.GetEventObject();
        if not cb.GetValue():
            self.FileRepos.Disable();
            self.FSB.Disable()
        else:
            self.FileRepos.Enable();
            self.FSB.Enable();

    def SelectFile(self, event):
        dlg = wx.DirDialog(self, _("Select Module Folder"));
        if dlg.ShowModal() != wx.ID_OK:
            dlg.Destroy()
            return;
        Folder = os.path.abspath(dlg.GetPath());
        Folder = os.path.normpath(Folder);
        self.FileRepos.SetValue(Folder);
        dlg.Destroy()
    
    def GetSettings(self):
        URLs = list();
        if self.StdHTTPRepos.GetValue(): URLs.append("http://pplt.local.de/Modules/");
        if self.StdFTPRepos.GetValue(): URLs.append("ftp://10.1.1.4/Modules/");
        if self.AddURLRepos.GetValue(): URLs.append(self.URLRepos.GetValue());
        if self.AddFileRepos.GetValue(): URLs.append("file://"+self.FileRepos.GetValue());
        return (URLs, self.FollowLinks.GetValue(), self.FollowOtherSite.GetValue(),);

    
    
def CreateRemoteDB(URLs, FollowLinks, FollowOtherSites, Proxies):
    RemoteDB = DataBase.DataBase(FollowLinks, FollowOtherSites);
    count = len(URLs);
    
    dlg = wx.ProgressDialog(_("Import Module Repositorities"), _("Start..."), 
                            maximum=count, style=wx.PD_CAN_ABORT|wx.PD_AUTO_HIDE);
               
    for i in range(count):
        URL = URLs[i];
        if not dlg.Update(dlg.Update(i, _("Import: ")+URL)):
            dlg.Destroy();
            return None;
        try: RemoteDB.AddSource(URL, Proxies);
        except Exception, e:
            dlg.Destroy()
            msg = wx.MessageDialog(None, _("Could not import repositority ")+URL+_("\n ErrorCode: ")+str(e),
                                   _("Error while import"), 
                                   wx.OK | wx.ICON_ERROR);
            msg.ShowModal();
            msg.Destroy();
            return None;
    dlg.Destroy()
    return RemoteDB;
    


class MainWin(wx.Frame):
    def __init__(self, localDB, remoteDB, BasePath, Lang, AltLang):
        wx.Frame.__init__(self, None, -1, _("PPLT Module Manager"), size=(710,500));
        self.MyPanel = wx.Panel(self, -1);
 
        vBox = wx.BoxSizer(wx.VERTICAL);

        box = wx.BoxSizer(wx.HORIZONTAL);
        cb = wx.CheckBox(self.MyPanel, -1, _("Hide Core-Modules"));
        cb.SetValue(True);
        self.Bind(wx.EVT_CHECKBOX, self.EvtHideCoreMods, cb);
        box.Add(cb);
        vBox.Add(cb, 0, wx.LEFT|wx.TOP, 5);
    
        self.List = ModInstallList(self.MyPanel, -1, localDB, remoteDB, BasePath, True, Lang, AltLang);
        vBox.Add(self.List, 1, wx.ALL|wx.EXPAND, 5);
    
        self.MyPanel.SetSizer(vBox);

    def EvtHideCoreMods(self, evt):
        cb = evt.GetEventObject();
        self.List.SetHideCoreMods(cb.IsChecked());

class myApp(wx.App):
    def OnInit(self):#
        self.RestoreStdio();
        Config = PPLT.Config()
        InitI18N(Config.GetBasePath(), Config.GetLang(), Config.GetAltLang());
    
        # get proxysettings
        Proxies = {};
        if not Config.GetFTPProxy() and not Config.GetHTTPProxy():
            Proxies = None; #will try to get it from environment
        else:
            Proxies.update( {"ftp":Config.GetFTPProxy()} );
            Proxies.update( {"http":Config.GetHTTPProxy()} );
        #setup logging
        Logger = PPLT.Logging.Logger(Config.GetPPLTLogLevel(),
                                     Config.GetLogFile(),
                                     Config.GetSysLog())
        #create databases:
        localDB = PPLT.DataBase.DataBase(Config.GetBasePath(), 
                                         Config.GetBasePath()+"/Mods/",
                                         Config.GetLang(),
                                         Config.GetAltLang());
        RemoteDB = None;
        while not RemoteDB:
            ReposDlg = ReposSelectionDialog();
            if not ReposDlg.ShowModal() == wx.ID_OK: return False;
            URLs, FollowLinks, FollowOtherSites = ReposDlg.GetSettings()
            ReposDlg.Destroy()
            RemoteDB = CreateRemoteDB(URLs, FollowLinks, FollowOtherSites, Proxies);
            
    
    
        win = MainWin(localDB, RemoteDB, Config.GetBasePath(),
                      Config.GetLang(), Config.GetAltLang());
        self.SetTopWindow(win)
        win.Show();
        return True;
    
    
App = myApp();
App.MainLoop();
    
