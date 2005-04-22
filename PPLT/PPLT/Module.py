import xml.dom.minidom;
import logging;

class DataBase:
    def __init__(self, FileName):
        self.__ModuleList = [];
        self.__Logger = logging.getLogger("PPLT");
        self.Load(FileName);
        self.__DBFileName = FileName;
        
    def Load(self, FileName):
        try:
            doc = xml.dom.minidom.parse(FileName);
        except:
            self.__Logger.error("Error while parse file");
            return(False);
        if not doc.documentElement.localName=="ModuleDatabase":
            self.__Logger.error("Invalid file format");
            doc.unlink();
            return(False);
        modlst = doc.getElementsByTagName('Module');
        for mod in modlst:
            if mod.firstChild == mod.TEXT_NODE:
                self.Add(mod.firstChild.data.strip());
        doc.unlink();
        return(True);
    
    def Save(self):
        impl = xml.dom.minidom.getDOMImplementation();
        doc = impl.createDocument(None, "ModuleDatabase", None)
        top_element = newdoc.documentElement;
        for mod in self.__ModuleList:
            modtag = doc.createElement('Module');
            top_element.appendChild(modtag);
            nametag = doc.createTextNode(mod);
            modtag.appendChild(nametag);
        docstr = doc.toprettyxml('   ');
        #fp = open(
    def Add(self, ModName):
        if not self.__ModuleList.count(ModName):
            self.__ModuleList.append(ModName);
        return(True);
        
    def Install(self, FileName):
        pass;
    
