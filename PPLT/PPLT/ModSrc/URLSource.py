import urllib
import xml.dom.minidom;
import DataBase;
import urlparse;

class URLSource:
    """ Class for installation source """
    def __init__(self, DB, ReposURL, Proxy={}):
        self.__BaseURL = str(ReposURL);
        self.__Proxies = Proxy;
        self.__ModuleListURL = urlparse.urljoin(self.__BaseURL+"/",".Modules");
        self.__DataBase = DB;
        self.__Links = list([]);
	
        #Open URL of modules-list:
        try: fd = urllib.urlopen(self.__ModuleListURL, proxies=self.__Proxies);
        except: 
            raise Exception(_("Can't open URL %s. Maybe bad proxy or network not reachable.")%self.__ModuleListURL);
	
        # Parse module-list;
        try: Doc = xml.dom.minidom.parse(fd);
        except Exception, e: 
            fd.close()
            raise Exception(_("Error while parse module-list at %s\n>>> %s")%(self.__ModuleListURL, str(e)));
        
	if not Doc.documentElement.localName == "ModuleListing":
	    raise Exception(_("Invalid Document."))
	    
	fd.close()
        del fd 

        #add core modules:
        CoreMods = Doc.getElementsByTagName("CoreModules");
	if CoreMods and len(CoreMods)>0:
            self.__ParseCoreMod(CoreMods[0].firstChild);

	PPLTMods = Doc.getElementsByTagName("PPLTModules");
	if PPLTMods and len(PPLTMods)>0:
            self.__ParsePPLTMod(PPLTMods[0].firstChild);

	LinkTags = Doc.getElementsByTagName("Link");
	for LinkTag in LinkTags:
	    if LinkTag.hasChildNodes():
		self.__ParseLink(LinkTag.firstChild);
	
    def __ParseCoreMod(self, xmlNode):
        if not xmlNode: return
        if xmlNode.nodeType == xmlNode.ELEMENT_NODE:
            if not xmlNode.hasAttribute("name"): 
                raise Exception(_("Invalid format of module-list %s. (no name)")%self.__ModuleListURL);
            if not xmlNode.hasAttribute("class"): 
                raise Exception(_("Invalid format of module-list %s. (no class)")%self.__ModuleListURL);
            if not xmlNode.hasAttribute("version"): 
                raise Exception(_("Invalid format of module-list %s. (no version)")%self.__ModuleListURL);
            if not xmlNode.hasAttribute("file"): 
                raise Exception(_("Invalid format of module-list %s. (no file-name)")%self.__ModuleListURL);
            Name = str(xmlNode.getAttribute("name"));
            Class = str(xmlNode.getAttribute("class"));
            Version = str(xmlNode.getAttribute("version"));
            FileName = str(xmlNode.getAttribute("file"));
            
            FileURL = urllib.basejoin(self.__BaseURL,FileName);

	    if xmlNode.hasChildNodes():
		if len(xmlNode.getElementsByTagName("Require"))>0:
                    elmRequire   = xmlNode.getElementsByTagName("Require")[0];
                    Requirements = self.__ParseRequire(elmRequire.firstChild, {});
                Description = {}
                for descNode in xmlNode.getElementsByTagName("Description"):
                    Desc = self.__ParseDescription(descNode);
		    if Desc: 
                        lang, txt = Desc;
			Description.update( {lang:txt} );
			
            # add to DB
            newItem = DataBase.CoreMod(Class+"."+Name, 
                                        FileURL, Version, Requirements.get("PythonVersion"),
					Requirements.get("pyDCPUVersion"),
					Requirements.get("PythonModule"), Description);
	    self.__DataBase.AddCoreMod(Class+"."+Name, newItem);
        self.__ParseCoreMod(xmlNode.nextSibling);


    def __ParsePPLTMod(self, xmlNode):
        if not xmlNode: return
	Type = xmlNode.localName;
        if xmlNode.nodeType == xmlNode.ELEMENT_NODE:
            if not Type in ("Server", "Device"):
                raise Exception(_("Invalid element (%s) in list.")%Type);
            if not xmlNode.hasAttribute("name"): 
                raise Exception(_("Invalid format of module-list %s. (no name)")%self.__ModuleListURL);
            if not xmlNode.hasAttribute("class"): 
                raise Exception(_("Invalid format of module-list %s. (no class)")%self.__ModuleListURL);
            if not xmlNode.hasAttribute("version"): 
                raise Exception(_("Invalid format of module-list %s. (no version)")%self.__ModuleListURL);
            if not xmlNode.hasAttribute("file"): 
                raise Exception(_("Invalid format of module-list %s. (no file-name)")%self.__ModuleListURL);
            Name = str(xmlNode.getAttribute("name"));
            Class = str(xmlNode.getAttribute("class"));
            Version = str(xmlNode.getAttribute("version"));
            FileName = str(xmlNode.getAttribute("file"));
            
            FileURL = urllib.basejoin(self.__BaseURL,FileName);

	    if xmlNode.hasChildNodes():
		if len(xmlNode.getElementsByTagName("Require"))>0:
                    elmRequire   = xmlNode.getElementsByTagName("Require")[0];
                    Requirements = self.__ParseRequire(elmRequire.firstChild, {});
                Description = {}
                for descNode in xmlNode.getElementsByTagName("Description"):
                    Desc = self.__ParseDescription(descNode);
		    if Desc: 
                        lang, txt = Desc;
			Description.update( {lang:txt} );
			
            # add to DB
            if Type=="Server":
                newItem = DataBase.ServerMod(Class+"."+Name, 
                                            FileURL, Version, Requirements.get("DCPUModule"), 
                                            Description);
            else:
                newItem = DataBase.DeviceMod(Class+"."+Name, 
                                            FileURL, Version, Requirements.get("DCPUModule"), 
                                            Description);
	    self.__DataBase.AddPPLTMod(Class+"."+Name, newItem);
	    
        self.__ParsePPLTMod(xmlNode.nextSibling);
    
    
    def __ParseRequire(self, xmlNode, Requirements):
        if not xmlNode:
	    return Requirements;
	if not xmlNode.nodeType == xmlNode.ELEMENT_NODE:
	    return self.__ParseRequire(xmlNode.nextSibling, Requirements);
        if xmlNode.localName == "PythonVersion":
            VerStr = xmlNode.firstChild.wholeText;
            Requirements.update( {"PythonVersion":VerStr} );
        elif xmlNode.localName == "pyDCPUVersion":
	    VerStr = xmlNode.firstChild.wholeText;
	    Requirements.update( {"pyDCPUVersion":VerStr} );
        elif xmlNode.localName == "DCPUModule":
	    ModList = Requirements.get("DCPUModule");
	    if not ModList: ModList = [];
	    ModName = xmlNode.firstChild.wholeText;
	    ModList.append(ModName);
	    Requirements.update( {"DCPUModule":ModList} );
        elif xmlNode.localName == "PythonModule":
	    ModList = Requirements.get("PythonModule");
	    if not ModList: ModList = [];
	    ModName = xmlNode.firstChild.wholeText;
	    ModList.append(ModName);
	    Requirements.update( {"PythonModule":ModList} );
        else: pass
	return self.__ParseRequire(xmlNode.nextSibling, Requirements);    


	
    def __ParseDescription(self, xmlNode):
	if not xmlNode.hasAttribute("lang"): lang = "en";
	else: lang = str(xmlNode.getAttribute("lang"));
	if xmlNode.hasChildNodes():
	    txtNode =xmlNode.firstChild;
	    if txtNode.nodeType == txtNode.TEXT_NODE:
		desc = txtNode.wholeText;
                return (lang, desc,);
        return None;
	
    def __ParseLink(self, xmlNode):
	if xmlNode.nodeType == xmlNode.TEXT_NODE:
             self.__Links.append(xmlNode.wholeText);
    def GetLinks(self): return self.__Links;
