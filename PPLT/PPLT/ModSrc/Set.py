import urlparse;
import Version;
import pyDCPU;
import os;
import urllib
import urlparse
import sys;
import imp;
import string;

def CollectCoreMods(localDB, Class=""):
    List = [];
    sClassList = localDB.ListCoreModClasses(Class);
    if sClassList:
        for sClass in sClassList:
            if Class!="": sClass = Class+"."+sClass;
            List.extend(CollectCoreMods(localDB, sClass));
    CMList = localDB.ListCoreMods(Class);
    if CMList: 
        if Class!="":
            for CoreMod in CMList:
                List.append(Class+"."+CoreMod)
        else: List.extend(CMList);
    return List;

def CollectServers(localDB, Class=None):
    List = [];
    sClassList = localDB.ListServerClasses(Class);
    if sClassList:
        for sClass in sClassList: 
            List.extend(CollectServers(localDB, sClass));
    SList = localDB.ListServers(Class);
    if SList: 
        if Class:
            for Server in SList:
                List.append(Class+"."+Server)
        else: List.extend(SList);
    return List;
    
def CollectDevices(localDB, Class=None):
    List = [];
    sClassList = localDB.ListDeviceClasses(Class);
    if sClassList:
        for sClass in sClassList:       
            List.extend(CollectDevices(localDB, sClass));
    DList = localDB.ListDevices(Class);
    if DList: 
        if Class:
            for Device in DList:
                List.append(Class+"."+Device)
        else: List.extend(DList);
    return List;

class SetItem:
    def __init__(self, LocalDB, Name, Vers, Description, URL, IsInstalled, IsLocal):
        self.LocalDB = LocalDB;
        self.Name = Name;
        self.Description = Description;
        self.ModuleURL = URL;
        self.ReferenceCounter = 0;
        self.isInstalled = IsInstalled;
        self.isLocal = IsLocal;
        self.Version = Vers;
        
    def GetName(self): return self.Name;
    def GetDescription(self): return self.Description;
    def GetURL(self): return self.ModuleURL;
    def IsDeletable(self): 
        if self.ReferenceCounter == 0: return True;
        return False;
    def IsLocal(self): return(self.isLocal);
    def IsInstalled(self): return self.isInstalled;
    def GetVersion(self): return self.Version;
    def Install(self): return False;
    def UnInstall(self): return False;
    def IsInstallable(self): return False;
    def Toggle(self):
        if self.IsInstalled() and self.IsLocal(): return self.UnInstall();      #delete
        if self.IsInstalled() and (not self.IsLocal()): 
            if self.IsInstallable():
                return self.Install()   #update
            return self.UnInstall()     #delete
        if not self.IsInstalled(): return self.Install();
        self.Error = _("Unpossible combination of beeing not installed and being local.");
        return False;
    
    def GetState(self):
        if self.IsInstallable():
            if self.IsInstalled() and self.IsLocal() : return "INST";
            if self.IsInstalled() and not self.IsLocal(): return "INSTUP";
            return "NINST"
        if self.IsInstalled() and not self.IsLocal(): return "INSTUPERR";
        return "ERR"

class CoreModItem(SetItem):
    def __init__(self, LocalDB, Name, Vers, Description, URL, IsInstalled, IsLocal, DCPUVersion=None, PythonVersion=None, PythonModules=[]):
        SetItem.__init__(self, LocalDB, Name, Vers, Description, URL, IsInstalled, IsLocal);
        self.ReqDCPUVersion = DCPUVersion;
        self.ReqPythonVersion = PythonVersion;
        self.ReqPythonModules = PythonModules;
        self.Error = ""
        
    def IsInstallable(self):
        #check python version:
        if self.ReqPythonVersion:
            major, minor, bug, name, patch = sys.version_info;
            VersionStr = "%i.%i.%i"%(major,minor,bug);
            InstPyVers = Version.Version(VersionStr);
            ReqPyVers = Version.Version(self.ReqPythonVersion);
            if abs(int(InstPyVers) - int(ReqPyVers))>= 0x1000:
                self.Error = _("Mismatching Python version: Need %s <-> has %s")%(ReqPyVers, InstPyVers);
                return False;
        #check dcpu version:
        if self.ReqDCPUVersion:
            InstDCPUVers = Version.Version(pyDCPU.__version__);
            ReqDCPUVers = Version.Version(self.ReqDCPUVersion);
            if abs(int(InstDCPUVers)-int(ReqDCPUVers))>= 0x1000:
                self.Error = _("Mismatching pyDCPU version: Need %s <-> has %s")%(ReqDCPUVers, InstDCPUVers);
                return False;
        #check python modules:
        for PyMod in self.ReqPythonModules:
            try: imp.find_module(PyMod)
            except:
                self.Error = _("Needed Python library %s not found (not installed?!?)")%PyMod;
                return False;
        return True;

    def Install(self):
        if not self.IsInstallable():
            return False;
        if self.IsInstalled(): return True;
        FileName, Header = urllib.urlretrieve(self.GetURL());
        if not FileName:
            self.Error = _("Unable to get file from URL %s")%self.GetURL();
            return False;
        if not self.LocalDB.InstallCoreMod(FileName, self.GetName()):
            os.remove(FileName);
            self.Error = _("Error while install %s")%self.GetName();
            return False;
        os.remove(FileName);
        return True;
        
    def UnInstall(self):
        if not self.IsDeletable():
            self.Error = _("This CoreMdoule is used by other Modules.");
            return False;
        if not self.IsInstalled(): return True;
        return self.LocalDB.UnInstallCoreMod(self.GetName());
    
    def IncReference(self): self.ReferenceCounter += 1;

class ServerItem(SetItem):
    def __init__(self, localDB, Name, Version, Description, URL, IsInstalled, IsLocal, CoreModules=[], KnownCoreMods={}):
        SetItem.__init__(self, localDB, Name, Version, Description, URL, IsInstalled, IsLocal);
        self.ReqCoreModules = CoreModules;
        self.KnownCoreMods = KnownCoreMods;
        self.Error = "";
    
    def IsInstallable(self):
        for CoreMod in self.ReqCoreModules:
            if not CoreMod in self.KnownCoreMods.keys():
                self.Error = _("Core module %s not known!")%CoreMod;
                return False;
            CMObj = self.KnownCoreMods.get(CoreMod);
            if not CMObj.IsInstallable():
                self.Error = _("Core mod %s is not installable. (%s)")%(CoreMod, CMObj.Error);
                return False;
        return True;

    def Install(self):  
        if not self.IsInstallable():
            return False;
        #if self.IsInstalled(): return True;
        FileName, Header = urllib.urlretrieve(self.GetURL());
        if not FileName:
            self.Error = _("Unable to get file from URL %s")%self.GetURL();
            return False;
        #resolve depencies:
        for CMName in self.ReqCoreModules:
            CoreMod = self.KnownCoreMods[CMName];
            if not CoreMod.Install():
                self.Error = _("Unable to install %s: Install of %s failed.(%s)")%(self.GetName(), CMName, CoreMod.Error);
                return False;
        if not self.LocalDB.InstallServer(FileName):
            os.remove(FileName);
            self.Error = _("Error while install %s")%self.GetName();
            return False;
        os.remove(FileName);
        return True;

    def UnInstall(self):
        if not self.IsInstalled(): return True;
        return self.LocalDB.UnInstallServer(self.GetName());

class DeviceItem(ServerItem):
    def Install(self):  
        if not self.IsInstallable():
            return False;
        #if self.IsInstalled(): return True;
        FileName, Header = urllib.urlretrieve(self.GetURL());
        if not FileName:
            self.Error = _("Unable to get file from URL %s")%self.GetURL();
            return False;
        #resolve depencies:
        for CMName in self.ReqCoreModules:
            CoreMod = self.KnownCoreMods[CMName];
            if not CoreMod.Install():
                self.Error = _("Unable to install %s: Install of %s failed.(%s)")%(self.GetName(), CMName, CoreMod.Error);
                return False;
        if not self.LocalDB.InstallDevice(FileName):
            os.remove(FileName);
            self.Error = _("Error while install %s")%self.GetName();
            return False;
        os.remove(FileName);
        return True;

    def UnInstall(self):
        if not self.IsInstalled(): return True;
        return self.LocalDB.UnInstallDevice(self.GetName());


class Set:
    def __init__(self, localDB, remoteDB, Lang, AltLang):
        self.LocalDB = localDB;
        self.RemoteDB = remoteDB;
        self.CoreMods = {};
        self.Servers = {};
        self.Devices = {};
        self.Lang = Lang;
        self.AltLang = AltLang;
        
        #add core modules:
        cMods = CollectCoreMods(self.LocalDB);
        for CoreMod in cMods:
            cName = CoreMod;
            cDescription = self.LocalDB.GetCoreModDescription(cName);
            cURL = "file://"+os.path.abspath(os.path.normpath(self.LocalDB.GetCoreModPath(cName)));
            cVersion = self.LocalDB.GetCoreModVersion(cName);
            cModItem = CoreModItem(self.LocalDB, cName, cVersion, cDescription, cURL, True, True);
            self.CoreMods.update( {cName:cModItem} );
        cMods = self.RemoteDB.ListCoreModules();
        for cName in cMods:
            DBItem = remoteDB.GetCoreMod(cName);
            cDescription = DBItem.GetDescription(self.Lang,self.AltLang);
            cURL = DBItem.GetURL();
            cPyVers = str(DBItem.GetPyVersion());
            cDCPUVers = str(DBItem.GetDCPUVersion());
            cPyMods = DBItem.GetPyMods();
            cVersion = DBItem.GetVersion();
            if cName in self.ListCoreMods():
                oldMod = self.GetCoreMod(cName)
                if int(cVersion) <= int(oldMod.GetVersion()): continue;
                isInst = True;
            else: isInst = False;
            cModItem = CoreModItem(self.LocalDB, cName, cVersion, 
                                   cDescription, cURL, isInst, False,
                                   cDCPUVers, cPyVers, cPyMods);
            self.CoreMods.update( {cName:cModItem} );
        #add installed servers:
        SrvLst = CollectServers(self.LocalDB);
        for Srv in SrvLst:
            sDesc = self.LocalDB.GetServerDescription(Srv);
            sVers = self.LocalDB.GetServerVersion(Srv);
            sCoreMods = self.LocalDB.GetServerReqCoreMods(Srv);
            sURL = "file://"+os.path.abspath(os.path.normpath(self.LocalDB.GetServerPath(Srv)));
            SrvItem = ServerItem(self.LocalDB, Srv, sVers, sDesc, sURL, True, True, sCoreMods, self.CoreMods);
            self.Servers.update( {Srv:SrvItem} )
            if SrvItem.IsInstallable(): 
                for CoreMod in sCoreMods: self.CoreMods[CoreMod].IncReference();
        #add installed devices:
        DevLst = CollectDevices(self.LocalDB);
        for Dev in DevLst:
            sDesc = self.LocalDB.GetDeviceDescription(Dev);
            sVers = self.LocalDB.GetDeviceVersion(Dev);
            sCoreMods = self.LocalDB.GetDeviceReqCoreMods(Dev);
            sURL = "file://"+os.path.abspath(os.path.normpath(self.LocalDB.GetDevicePath(Dev)));
            DevItem = DeviceItem(self.LocalDB, Dev, sVers, sDesc, sURL, True, True, sCoreMods, self.CoreMods);
            self.Devices.update( {Dev:DevItem} )
            if DevItem.IsInstallable(): 
                for CoreMod in sCoreMods: self.CoreMods[CoreMod].IncReference();
        #add remote server/device items:
        PPLTLst = self.RemoteDB.ListPPLTModules();
        for Mod in PPLTLst:
            mItem = self.RemoteDB.GetPPLTMod(Mod);
            IsServer = mItem.IsServer;
            mVersion = mItem.GetVersion();
            IsInst = False;
            if IsServer:
                if Mod in self.Servers.keys():
                    IsInst = True;
                    if mVersion <= self.Servers[Mod].GetVersion(): continue;
            else:
                if Mod in self.Devices.keys():
                    IsInst = True;
                    if mVersion <= self.Devices[Mod].GetVersion(): continue;

            mDesc = mItem.GetDescription(self.Lang,self.AltLang);
            mURL = mItem.GetURL();
            mReqMods = mItem.GetCoreMods();
            if IsServer: 
                ModItem = ServerItem(self.LocalDB, Mod, mVersion, mDesc, mURL, IsInst,False, mReqMods, self.CoreMods);
                self.Servers.update( {Mod:ModItem} );
            else: 
                ModItem = DeviceItem(self.LocalDB, Mod, mVersion, mDesc, mURL, IsInst,False, mReqMods, self.CoreMods);
                self.Devices.update( {Mod:ModItem} )
            
    def ListCoreMods(self): return self.CoreMods.keys();    
    def GetCoreMod(self, Name): return self.CoreMods.get(Name);
    def ListServers(self): return self.Servers.keys();
    def GetServer(self, Name): return self.Servers.get(Name);
    def ListDevices(self): return self.Devices.keys();
    def GetDevice(self, Name): return self.Devices.get(Name);
        
    
