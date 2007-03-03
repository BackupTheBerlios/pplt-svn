import os.path
import xml.dom.minidom
import xml.xpath
import logging
from edef.dev import Config
import fnmatch
from Tools import getModuleName


class Model:
    def __init__(self):
        self._logger = logging.getLogger("edef.dev")
        self._base_path = Config().getBasePath()
        self._module_list = dict()

        file_list = os.listdir(self._base_path)
        xmlfile_list = fnmatch.filter(file_list, "*.xml")
        for filename in xmlfile_list:
            self._logger.debug("Found xml file %s"%filename)
            path = os.path.abspath( os.path.join(self._base_path, filename) )
            try:
                module = eDevModelModule(path)
            except:
                self._logger.exception("Exception while load xml %s"%path)
                continue
            self._module_list[module.GetURI()] = module


    def openURI(self, uri):
        if uri == "mod://":
            return self._module_list.keys()
        try: mod = self._module_list[uri]
        except: raise Exception("Unknown module %s"%uri)
        return mod.getText()

    
    def saveURI(self, uri, txt=None):
        if not uri in self._module_list.keys():
            # create module...
            mod_name = getModuleName(uri)+".xml"
            mod_path = os.path.join(self._base_path, mod_name)
            if os.path.isfile(mod_path): raise Exception("File %s allready exists!"%mod_path)
            f = open(mod_path,"w")
            f.write(txt)
            f.close()
            mod = eDevModelModule(mod_path)
            self._module_list[uri] = mod
            return
        # save module
        mod = self._module_list[uri]
        mod.setText(txt)
    
    
    def checkURI(self, uri):
        return uri in self._module_list.keys()


    def deleteURI(self, uri):
        if not uri in self._module_list.keys():
            raise Exception("Module %s not known"%uri)
        os.unlink(self._module_list[uri].getPath())
        del self._module_list[uri]



class eDevModelModule:
    _d_name = None

    def __init__(self, path):
        self._d_full_path = path
        if not os.path.isfile(path):
            raise Exception("%s doesn't point to a file!"%path)
        (tmp, name) = os.path.split(path)
        (name, tmp) = os.path.splitext(name)
        (tmp, self._d_name) = os.path.splitext(name)
        if self._d_name == "": self._d_name = tmp
        self._d_uri = "mod://"+"/".join(name.split("."))

        # FIXME replace by TREX
        dom = xml.dom.minidom.parse(path)
        if len(xml.xpath.Evaluate("/Module", dom))==0:
            raise Exception("Not an module!")

    def GetURI(self): return self._d_uri
    def getName(self): return self._d_name
    def getPath(self): return self._d_full_path

    def getText(self):
        f = open(self._d_full_path,"r")
        txt = f.read()
        f.close()
        return txt

    def setText(self, xml_txt):
        # FIXME check xml_txt
        f = open(self._d_full_path, "w")
        f.write(xml_txt)
        f.close()

