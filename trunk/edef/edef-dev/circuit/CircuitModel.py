import os
import os.path
import xml.dom.minidom
import xml.xpath
import logging
import fnmatch
from edef.dev import Tools


class Model:
    def __init__(self):
        self._logger = logging.getLogger("edef.dev")
        self._base_path = os.path.normpath( os.path.expanduser("~/.edef/circuits") )

        if not os.path.isdir(self._base_path):
            self._logger.debug("Private circuit-dir %s doesn't extist -> create")
            os.mkdir(self._base_path)

        file_list = os.listdir(self._base_path)
        xmlfile_list = fnmatch.filter(file_list, "*.xml")

        self._circuits = dict()
        for xmlfile in xmlfile_list:
            if not os.path.isabs(xmlfile):
                xmlfile = os.path.abspath( os.path.join(self._base_path, xmlfile) )
            try:
                circ = CircuitModel(xmlfile)
            except:
                self._logger.exception("Error while load circuit %s"%xmlfile)
                continue
                       
            self._circuits[circ.getURI()] = circ


    def openURI(self, uri):
        if uri == "circ://": return self._circuits.keys()
        return self._circuits[uri].getText()


    def saveURI(self, uri, data):
        if uri == "circ://": raise Exception("Invaid uri %s"%uri)
        
        if not uri in self._circuits.keys():
            (proto, path) = Tools.splitURI(uri)
            path = ".".join(path.split("/"))+".xml"
            path = os.path.join(self._base_path, path)
            circ = CircuitModel(path)
            self._circuits[uri] = circ
           
        self._circuits[uri].setText(data)
        

    def deleteURI(self, uri):
        if not uri in self._circuits.keys():
            raise Exception("Can't delete uri %s: Not found!"%uri)
        path = self._circuits[uri].getPath()
        os.unlink(path)
        del self._circuits[uri]


    def checkURI(self, uri):
        return uri in self._circuits.keys()
    def isEditable(self, uri): return True
    def isWriteable(self, uri): return True



class CircuitModel:
    def __init__(self, path):
        self._logger = logging.getLogger("edef.dev")

        self._path = path
        (tmp, name) = os.path.split(path)
        (name, tmp) = os.path.splitext(name)
        (tmp, self._name) = os.path.splitext(name)
        if self._name == "": self._name = tmp
        self._uri = "circ://"+"/".join(name.split("."))

    def getText(self): return open(self._path, "r").read()
    def getURI(self): return self._uri
    def getPath(self): return self._path
    def setText(self, txt): open(self._path, "w").write(txt)
        

