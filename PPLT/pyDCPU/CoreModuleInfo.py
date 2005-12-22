import pyDCPU;
import zipfile;
import logging;
import xml.dom.minidom;
import Version;
import sys;
import imp;
import string;
import pyDCPU.Exceptions as Exceptions;
import os.path;


def GetMetaData(FileName):
    Logger = logging.getLogger("pyDCPU");
    if not os.path.exists(FileName):
        raise Exceptions.ItemNotFound("Module @ %s not found!"%FileName);
    zipobj = zipfile.ZipFile(FileName,"r");
    lst = zipobj.namelist();
    #check if meta-data exists in zip file:
    if not "meta.xml" in lst:
        raise Exceptions.BadModule("Invalid module format: no meta.xml found in file %s"%FileName);
    meta = zipobj.read("meta.xml");
    zipobj.close();
    return(meta);



class MetaData:
    def __init__(self, FileName):
        self.__Logger = logging.getLogger("pyDCPU");
        self.__Authors = [];
        self.__LastUpdate = None;
        self.__URLs = [];
        self.__Descriptions = {};
        self.__ChildNeedAddress = None;
        self.__pyDCPUVersion = None;
        self.__PythonVersion = None;
        self.__PythonModules = [];
        self.__Parameters = {}

        xmlstr = GetMetaData(FileName);
        
        try: doc = xml.dom.minidom.parseString(xmlstr).documentElement;
        except Exception, e:
            self.__Logger.error("Error while parse meta-file in %s: %s"%(FileName, str(e)));
            raise Exceptions.BadModule("Error while parse mata-file in %s: %s"%(FileName, str(e)));

        self.__FileName = FileName;
        self.__VersionString = str(doc.getAttribute("version"));

        if not doc.hasAttribute("root"):
            self.__IsRoot = False;
        elif str(doc.getAttribute("root")) == "True":
            self.__IsRoot = True;
        else:
            self.__IsRoot = False;

        tmp = doc.getElementsByTagName("Author");
        self._addAuthors(tmp);
        tmp = doc.getElementsByTagName("LastUpdate");
        self._addLastUpdate(tmp);
        tmp = doc.getElementsByTagName("URL");
        self._addURLs(tmp);

        tmp = doc.getElementsByTagName("ChildAddress");
        self._addChildAddress(tmp);
        tmp = doc.getElementsByTagName("pyDCPUVersion");
        self._addDCPUVersion(tmp);
        tmp = doc.getElementsByTagName("PythonVersion");
        self._addPythonVersion(tmp);
        tmp = doc.getElementsByTagName("PythonModule");
        self._addPythonModule(tmp);
        tmp = doc.getElementsByTagName("Parameter");
        self._addParameter(tmp);
        tmp = doc.getElementsByTagName("Description");
        self._addModDescription(tmp);
        doc.unlink();
        #--- done ---

    def _addAuthors(self, Nodes):
        for node in Nodes:
            Author = GetText(node.firstChild);
            if Author != "":
                self.__Authors.append(Author);
                
    def _addLastUpdate(self, Nodes):
        if len(Nodes)>0:
            self.__LastUpdate = GetText(Nodes[0].firstChild);
        if self.__LastUpdate == "":
            self.__LastUpdate = None;

    def _addURLs(self, Nodes):
        for node in Nodes:
            URL = GetText(node.firstChild);
            if URL !=  "":
                self.__URLs.append(URL);
    
    def _addChildAddress(self, Nodes):
        if len(Nodes)>0:
            tmp = GetText(Nodes[0].firstChild);
        if tmp == 'True':
            self.__ChildNeedAddress = True;
        else:
            self.__ChildNeedAddress = False;
        return(None);

    def _addDCPUVersion(self, Nodes):
        if len(Nodes)>0:
            tmp = GetText(Nodes[0].firstChild);
        if tmp == '':
            self.__pyDCPUVersion = None;
            return(None);
        self.__pyDCPUVersion = Version.Version(tmp);

    def _addPythonVersion(self, Nodes):
        if len(Nodes)>0:
            tmp = GetText(Nodes[0].firstChild);
        if tmp == '':
            self.__PythonVersion = None;
            return(None);
        self.__PytonVersion = Version.Version(tmp);

    def _addPythonModule(self, Nodes):
        for node in Nodes:
            Mod = GetText(node.firstChild);
            if Mod != '':
                self.__PythonModules.append(Mod);
    
    def _addParameter(self, Nodes):
        for node in Nodes:
            if node.hasAttribute("name"):
                name = str(node.getAttribute("name"));
                duty = False; default = None;
                if node.hasAttribute("duty"):
                    t = str(node.getAttribute("duty"));
                    if t == "True":
                        duty = True;
                    else:
                        duty = False;
                if node.hasAttribute("default"):
                    default = str(node.getAttribute("default"));
                self.__Parameters.update( {name:(duty,default)} );
                
    def _addModDescription(self, xmlNodes):
        for xmlNode in xmlNodes:
            langAttr = xmlNode.attributes.get("lang");
            if not langAttr:
                return(False);
            lang = langAttr.value;
            if not xmlNode.hasChildNodes(): continue;
            if xmlNode.firstChild.nodeType == xmlNode.TEXT_NODE:
                text = xmlNode.firstChild.wholeText;
                self.__Descriptions.update( {lang:text} );
        return(True);

    def GetVersionString(self): return(self.__VersionString);
    def GetVersion(self): return(Version.Version(self.__VersionString));
    def GetAuthors(self): return(self.__Authors);
    def GetLastUpdate(self): return(self.__LastUpdate);
    def GetURLs(self): return(self.__URLs);
    def GetDescription(self, lang, alt_lang):
        if self.__Descriptions.has_key(lang):
            return(self.__Descriptions[lang]);
        return(self.__Descriptions.get(alt_lang));
    def GetParameterNames(self): return(self.__Parameters.keys());
    def IsParameterDuty(self, Name):
        ret = self.__Parameters.get(Name);
        if not ret:
            return(False);
        return(ret[0]);
    def GetParameterDefaultValue(self, Name):
        ret = self.__Parameters.get(Name);
        if not ret:
            return("");
        return(ret[1]);
    def ChildNeedAddress(self): return(self.__ChildNeedAddress);
    def IsRootModule(self): return(self.__IsRoot);
        
    def CheckDCPUVersion(self, DCPUVersion=pyDCPU.__version__):
        if not self.__pyDCPUVersion:
            return(True);
        ver = Version.Version(DCPUVersion);
        if abs(int(ver)-int(self.__pyDCPUVersion)) >= 0x10000:
            self.__Logger.error("Need pyDCPU version %s got %s: diff %i"%(ver,self.__pyDCPUVersion, 
                    abs(int(ver)-int(self.__pyDCPUVersion))))
            return(False);
        return(True);

    def CheckPythonVersion(self):
        if not self.__PythonVersion:
            return(True);
        (major,minor,bug,name,patch) = sys.version_info;
        ver = (major<<16)|(minor<<8)|bug;
        if abs(ver-int(self.__PythonVersion)) >= 0x10000:
            self.__Logger.error("Need Python version %i got %s: diff %i"%(ver,self.__PythonVersion, 
                    abs(ver-int(self.__pyDCPUVersion))))
            return(False);
        return(True);

    def CheckPythonModules(self):
        for mod in self.__PythonModules:
            try:
                if not imp.find_module(mod):
                    return(False);
            except:
                return(False);
            return(True);

    def CheckParameters(self, Names):
        for para in self.__Parameters.keys():
            (duty, default) = self.__Parameters[para];
            if duty and para not in Names:
                return(False);
        return(True);

    def ExtendParameters(self, Paras):
        for para in self.__Parameters.keys():
            (duty, default) = self.__Parameters[para];
            if (not para in Paras.keys()) and default:
                Paras.update( {para:default} );
        return(None);
    

def GetText(Node, txt = ""):
    if Node == None:
        return(txt);
    if Node.nodeType == Node.TEXT_NODE:
        txt += string.strip(Node.data);
    return(GetText(Node.nextSibling, txt));



if __name__ == "__main__":
    import pyDCPU;
    md = MetaData("/usr/PPLT/Export/JVisu.zip");
    print "Check pyDCPU Version: %s"%str(md.CheckDCPUVersion());
    print "Check Python Version: %s"%str(md.CheckPythonVersion())
    print "Check Python Modules: %s"%str(md.CheckPythonModules());
    para = {"Address":"127.0.0.1"};
    print "Paramters:            %s"%str(para);
    print "Known Parameters      %s"%str(md.GetParameterNames());
    print "Check Paramters:      %s"%str(md.CheckParameters(para.keys()));
    md.ExtendParameters(para);
    print "Extended Parameters:  %s"%str(para);
    print "Is Root Module:       %s"%str(md.IsRootModule());
    print "Child need address:   %s"%str(md.ChildNeedAddress());
