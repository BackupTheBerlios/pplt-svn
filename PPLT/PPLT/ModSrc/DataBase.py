import string
import Version;
import URLSource;
import urllib;
import urlparse;

class ClassBase:
    """Base class for module classes."""
    def __init__(self, Name):
        self.Name = Name;
	self.SubClasses = {};
	self.Items = {};

    def AddItem(self, QItemName, Item):
        tList = QItemName.split(".");
	if len(tList) == 1: 
            self.Items.update( {tList[0]:Item} );
	    return True;
    
	nQItemName = string.join(tList[1:], ".");
        if not self.SubClasses.has_key(tList[0]):
            nClass = ClassBase(tList[0]);
            self.SubClasses.update( {tList[0]:nClass} );
        subClass = self.SubClasses.get(tList[0]);
        return subClass.AddItem(nQItemName, Item);
    
    def GetItem(self, QItemName):
	tList = QItemName.split(".");
	if len(tList)==1:
	    if not self.Items.has_key(tList[0]): return None;
            return self.Items.get(tList[0]);
        nQName = string.join(tList[1:],".");
	if not self.SubClasses.has_key(tList[0]): return None
	return self.SubClasses[tList[0]].GetItem(nQName);
	    
    def ListClasses(self): return self.SubCLasses.keys();
    def ListItems(self): return self.Items.keys();


    
class Item:
    def __init__(self, FQIN, URL, Vers, Desc={}):
        self.FQItemName = FQIN;
	self.ItemURL = URL;
        self.ItemVersion = Version.Version(Vers)
	self.ItemDescriptions = Desc;
    def GetName(self):
	tList = self.FQItemName.split(".");
	return tList[-1];
    def GetURL(self): return self.ItemURL;
    def GetFQIN(self): return self.FQItemName;
    def GetVersion(self): return self.ItemVersion;
    def GetDescription(self, Lang, AltLang):
	if self.ItemDescriptions.has_key(Lang): return self.ItemDescriptions.get(Lang);
	return self.ItemDescriptions.get(AltLang);

    
class CoreMod(Item):
    def __init__(self, FQIN, URL, Vers, PyVersion, DCPUVersion, PyMods=[], Desc={}):
	Item.__init__(self, FQIN, URL, Vers, Desc);
	self.RequiredPythonVersion = Version.Version(PyVersion);
    	self.RequiredDCPUVersion = Version.Version(DCPUVersion);
	self.RequiredPythonModules = PyMods;
        
    def GetPyVersion(self): return self.RequiredPythonVersion;
    def GetDCPUVersion(self): return self.RequiredDCPUVersion;
    def GetPyMods(self): return self.RequiredPythonModules;
    

class PPLTMod(Item):
    def __init__(self, FQIN, URL, Vers, CoreMods=[], Desc={}):
	Item.__init__(self, FQIN, URL, Vers, Desc);
	self.RequiredCoreModules = CoreMods;
	
    def GetCoreMods(self): return self.RequiredCoreModules;
    
class ServerMod(PPLTMod):
    def __init__(self, FQIN, URL, Vers, CoreMods=[], Desc={}):
	PPLTMod.__init__(self, FQIN, URL, Vers, CoreMods, Desc);
        self.IsServer = True;

class DeviceMod(PPLTMod):
    def __init__(self, FQIN, URL, Vers, CoreMods=[], Desc={}):
	PPLTMod.__init__(self, FQIN, URL, Vers, CoreMods, Desc);
        self.IsServer = False;

#
# Main remote respository DataBase
#	
class DataBase:
    def __init__(self, FollowLinks=True, FollowOtherServer=False):
	self.__CoreModules = ClassBase("");
        self.__CoreModList = [];
	self.__PPLTModules = ClassBase("");
        self.__PPLTModList = [];
        self.__SourceFilterFollowLinks = FollowLinks;
	self.__SourceFilterFollowOtherServer = FollowOtherServer;
	self.__SourceURLs = [];
	
    def AddCoreMod(self, FQName, Item):
	oItem = self.__CoreModules.GetItem(FQName);
	if oItem:
            if Item.GetVersion() <= oItem.GetVersion():
		return None;
        if self.__CoreModules.AddItem(FQName, Item):
	    self.__CoreModList.append(FQName);
        return

    def GetCoreMod(self, FQName): return self.__CoreModules.GetItem(FQName);
       
    def AddPPLTMod(self, FQName, Item):
	oItem = self.__PPLTModules.GetItem(FQName);
	if oItem:
	    if oItem.GetVersion() >= Item.Version():
		return None;
        if self.__PPLTModules.AddItem(FQName, Item):
	    self.__PPLTModList.append(FQName);
        return

    def GetPPLTMod(self, FQName): return self.__PPLTModules.GetItem(FQName);

    def ListCoreModules(self): return list(self.__CoreModList);
    def ListPPLTModules(self): return list(self.__PPLTModList);
    
    def AddSource(self, URL, Proxies={}):
        Source = URLSource.URLSource(self, URL, Proxies); #register URL and add contend to DB.
	self.__SourceURLs.append(URL);
	Links = Source.GetLinks();
	Links = self.FilterURLs(Links);
	del Source;
	for Link in Links: 
            Link = Link+"/";
            self.AddSource(Link, Proxies);
	
    def FilterURLs(self, URLs):
	""" Filter URLs by setted filters. """
	nURLs = list();
	for URL in URLs:
	    if URL in self.__SourceURLs: continue; 		#skip already used repos
	    if not self.__SourceFilterFollowLinks: continue;	#skip all if no FollowLinks
	    if not self.__SourceFilterFollowOtherServer:	
		if not self.isKnownServer(URL): continue;
            nURLs.append(URL);
        return nURLs;
    
    def isKnownServer(self, URL):
        net, nhost, path, query, id = urlparse.urlsplit(URL)
	nhost, port = urllib.splitport(nhost);
        for kURL in self.__SourceURLs:
	    net, khost, path, query, id = urlparse.urlsplit(kURL);
            khost, port = urllib.splitport(khost);
	    if nhost == khost: return True;
        return False;
            