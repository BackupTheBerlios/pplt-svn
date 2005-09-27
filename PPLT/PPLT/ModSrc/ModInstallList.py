import wx;
import os;
import Set;
import sys;

def LoadIcons(BasePath):
    IconPath = os.path.normpath(BasePath+"/icons/");
    bmps = {};
    
    tmp = wx.Bitmap(os.path.normpath(IconPath+"/ok.xpm"));
    if not tmp: tmp = wx.NullBitmap;
    bmps.update( {"ok":tmp} )

    tmp = wx.Bitmap(os.path.normpath(IconPath+"/ok_up.xpm"));
    if not tmp: tmp = wx.NullBitmap;
    bmps.update( {"ok_up":tmp} )

    tmp = wx.Bitmap(os.path.normpath(IconPath+"/ok_uperr.xpm"));
    if not tmp: tmp = wx.NullBitmap;
    bmps.update( {"ok_uperr":tmp} )
    
    tmp = wx.Bitmap(os.path.normpath(IconPath+"/err.xpm"));
    if not tmp: tmp = wx.NullBitmap;
    bmps.update( {"err":tmp} )

    tmp = wx.Bitmap(os.path.normpath(IconPath+"/not.xpm"));
    if not tmp: tmp = wx.NullBitmap;
    bmps.update( {"not":tmp} )
    return bmps;
    
    
class ModInstallList(wx.ListCtrl):
    def __init__(self, parent, id, localDB, remoteDB, BasePath, HideCoreMods=True, Lang="en", AltLang="en"):
	wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT|wx.BORDER_NONE);
	self.Lang = Lang;
	self.AltLang = AltLang;
        self.HideCoreMods = HideCoreMods;
	self.LocalDB = localDB;
	self.RemoteDB = remoteDB;
	self.ModSet = None;
    	self.DataSet = {};
	self.IDNameTable = {};
        #handle (prepare) icons
	Icons = LoadIcons(BasePath);
        self.ImageList = wx.ImageList(16,16);
	self.__IcoOK = self.ImageList.Add(Icons.get("ok"));
	self.__IcoOKUP = self.ImageList.Add(Icons.get("ok_up"));
	self.__IcoOKUPERR = self.ImageList.Add(Icons.get("ok_uperr"));
	self.__IcoERR = self.ImageList.Add(Icons.get("err"));
	self.__IcoNOT = self.ImageList.Add(Icons.get("not"));
	self.SetImageList(self.ImageList, wx.IMAGE_LIST_SMALL)
	
        #make columns:
        self.InsertColumn(0,"Name");
	self.InsertColumn(1,_("Description"));
	self.InsertColumn(2,"URL");

        #fill up:
	self.Build();
	
    	self.Bind(wx.EVT_LEFT_DCLICK, self.OnItemToggle);

    def SetHideCoreMods(self, Value): 
        self.HideCoreMods = Value;
        self.Rebuild();
	
    def CompareItems(self, id1, id2):
	name1 = str(self.IDNameTable.get(id1));
	name2 = str(self.IDNameTable.get(id2));
	if name1 >= name2: return 1;
	return -1;
	
    def OnItemToggle(self, event):
	item, flag = self.HitTest(event.GetPosition());
	if item==None:
	    return;
        if flag&wx.LIST_HITTEST_ONITEMICON:
            FQName = self.GetItemText(item);
            ModItem = self.DataSet.get(FQName);
            if ModItem.IsInstalled() and ModItem.IsLocal():
                dlg = wx.MessageDialog(self, _("Do you realy want to uninstall ")+ModItem.GetName(), _("Uninstall"), wx.YES_NO|wx.ICON_QUESTION);
                if dlg.ShowModal() != wx.ID_YES: 
                    dlg.Destroy();
                    return;
                dlg.Destroy();
            if not ModItem.Toggle(): 
                ErrTxt = ModItem.Error.encode('ascii','replace');
                dlg = wx.MessageDialog(self, ErrTxt, _("Error"), wx.OK|wx.ICON_ERROR)
                dlg.ShowModal();
		dlg.Destroy();
            self.Rebuild();
        elif flag&wx.LIST_HITTEST_ONITEMLABEL:
            FQName = self.GetItemText(item);
            ModItem = self.DataSet.get(FQName);
	    txt  = _("Modulename: ")+ModItem.GetName();
	    txt += _("\nVersion: ") +str(ModItem.GetVersion());
	    if ModItem.IsInstallable():
		if ModItem.IsInstalled(): 
                    txt += _("\nModule is installed.")
                    if not ModItem.IsLocal():
                        txt += _("And update aviable.");
			txt +=_("\n\n To update the module: please double-click at the icon of the Module");
                else: 
                    txt += _("\nModule not installed.")
                    txt +=_("\n\nTo install the module: please double-click at the icon of the Module");
            else:
		if ModItem.IsInstalled(): txt += _("\nModule installed but the update is not installable.");
		else: txt += _("\nModule not installable!");
		txt += _("\nReason: ")+ModItem.Error.encode('ascii','replace');
            dlg = wx.MessageDialog(self, txt, _("Module Info"), wx.OK|wx.ICON_INFORMATION);
	    dlg.ShowModal();
	    dlg.Destroy();


    def Build(self):
        self.ModSet = Set.Set(self.LocalDB, self.RemoteDB, self.Lang, self.AltLang);
        if not self.HideCoreMods:
            CoreMods = self.ModSet.ListCoreMods();
	    for Name in CoreMods:
		ModObj = self.ModSet.GetCoreMod(Name);
                Desc   = ModObj.GetDescription();
		URL    = ModObj.GetURL();
		State  = ModObj.GetState();
		if State == "INST": Icon = self.__IcoOK;
		elif State == "INSTUP": Icon = self.__IcoOKUP;
		elif State == "INSTUPERR": Icon = self.__IcoOKUPERR;
		elif State == "ERR": Icon = self.__IcoERR;
		elif State == "NINST": Icon = self.__IcoNOT;
                self.DataSet.update( {Name: ModObj} );
		id = wx.NewId();
		self.IDNameTable.update({id:Name});
		idx = self.InsertImageStringItem(sys.maxint, Name, Icon);
		self.SetStringItem(idx,1,unicode(Desc));
		self.SetStringItem(idx,2,str(URL));
		self.SetItemData(idx,id);
                item = self.GetItem(idx);
                item.SetTextColour('#777777');
                self.SetItem(item);
        Servers = self.ModSet.ListServers();
        for Name in Servers:
            ModObj = self.ModSet.GetServer(Name);
            Desc   = ModObj.GetDescription();
            URL    = ModObj.GetURL();
            State  = ModObj.GetState();
            if State == "INST": Icon = self.__IcoOK;
            elif State == "INSTUP": Icon = self.__IcoOKUP;
            elif State == "INSTUPERR": Icon = self.__IcoOKUPERR;
            elif State == "ERR": Icon = self.__IcoERR;
            elif State == "NINST": Icon = self.__IcoNOT;
            self.DataSet.update( {Name: ModObj} );
	    id = wx.NewId();
	    self.IDNameTable.update( {id:Name} );
            idx = self.InsertImageStringItem(sys.maxint, Name, Icon);
            self.SetStringItem(idx,1,unicode(Desc));
            self.SetStringItem(idx,2,str(URL));
	    self.SetItemData(idx,id)
            item = self.GetItem(idx);
            self.SetItem(item);
        Devices = self.ModSet.ListDevices();
        for Name in Devices:
            ModObj = self.ModSet.GetDevice(Name);
            Desc   = ModObj.GetDescription();
            URL    = ModObj.GetURL();
            State  = ModObj.GetState();
            if State == "INST": Icon = self.__IcoOK;
            elif State == "INSTUP": Icon = self.__IcoOKUP;
            elif State == "INSTUPERR": Icon = self.__IcoOKUPERR;
            elif State == "ERR": Icon = self.__IcoERR;
            elif State == "NINST": Icon = self.__IcoNOT;
            self.DataSet.update( {Name: ModObj} );
	    id = wx.NewId();
	    self.IDNameTable.update( {id:Name} );
            idx = self.InsertImageStringItem(sys.maxint, Name, Icon);
            self.SetStringItem(idx,1,unicode(Desc));
            self.SetStringItem(idx,2,str(URL));
	    self.SetItemData(idx,id)
            item = self.GetItem(idx);
            self.SetItem(item);
	self.SetColumnWidth(0,200);
	self.SetColumnWidth(1,350);
	self.SetColumnWidth(2,150);
	self.SortItems(self.CompareItems)

    def Rebuild(self):
	self.DeleteAllItems()
	self.Build();
