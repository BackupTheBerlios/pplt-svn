import xml.xpath
import imp
import os.path
from zipimport import zipimporter
from ModuleMeta import CModuleMeta
from Exceptions import * 


class CCoreModuleMeta (CModuleMeta):
    _d_file_path = None

    def __init__(self, xml_dom, file_path):
        CModuleMeta.__init__(self, xml_dom)
    
        self._d_file_path = file_path

        # check grammar version:
        vers_attr = xml.xpath.Evaluate("/Module/@version", self._d_dom)
        if not vers_attr[0].nodeValue == "1.0":
            raise InvalidGrammarVersion("Can't handle grammar version %s"%vers_attr[0].nodeValue)


    def getArchive(self):
        node = xml.xpath.Evaluate("/Module/Archive/text()",self._d_dom)
        return node[0].wholeText.strip()


    def getClass(self):
        node = xml.xpath.Evaluate("/Module/Class/text()",self._d_dom)
        return node[0].wholeText.strip()


    def isInnerModule(self):
        node = xml.xpath.Evaluate("/Module/Type/text()",self._d_dom)
        return node[0].wholeText.strip()=="inner"


    def checkDependencies(self):
        # to check all dependencies get all <PyModule> tags and try to find 
        # them using imp.find_module()
        nodes = xml.xpath.Evaluate("/Module/Require/PyModule/text()", self._d_dom)
        for node in nodes:
            mod_name = node.wholeText.strip()
            #FIXME this can't handle doted names
            (fp, path, desc) = imp.find_module(mod_name)
            if fp: fp.close()
 

    def instance(self, parameters, parent=None, address=None):

        # if no absolute path is given im mod-meta -> take it relative to the
        # meta-file
        mod_archive = self.getArchive()
        if not os.path.isabs(mod_archive):
            mod_archive = os.path.join( os.path.dirname(self._d_file_path), mod_archive)
         
        # try to find module:
        zipimp = zipimporter(mod_archive);
        mod = zipimp.load_module(self.getClass());
 
        #load class from module
        try:
            cls = mod.__dict__[self.getClass()]
        except:
            raise ItemNotFound("Can't find class %s in %s [%s]"%
                        (self.getClass(), mod_archive, mod.__dict__.keys()))

        #instance class:
        if not self.isInnerModule():
            return cls(parameters)
        else:
            return cls(parent, address, parameters)


