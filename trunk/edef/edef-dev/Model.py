import os
import os.path
import fnmatch
#from pyeditor.ModelArchive import eDevModelArchive
#from modeditor.ModelModule import eDevModelModule
import re
import logging
from edef import Singleton
import Tools
from zipfile import ZipFile


class eDevModel:
    _logger             = None
    _protocol_handler   = None

    __metaclass__ = Singleton
    def __init__(self):
        #FIXME if local path not exists -> create
        self._protocol_handler = dict()
        self._logger = logging.getLogger("edef.Developer")


    def registerProtocol(self, proto, handler):
        self._protocol_handler[proto] = handler


    def openURI(self, uri):
        self._logger.debug("Open URI: %s"%uri)
        
        (proto, path) = Tools.splitURI(uri)
        if not proto in self._protocol_handler.keys():
            raise Exception("Unkonwn protocol: %s"%proto)
        
        return self._protocol_handler[proto].openURI(uri)


    def saveURI(self, uri, txt):
        self._logger.debug("Save %s"%uri)

        (proto, path) = Tools.splitURI(uri)
        if not proto in self._protocol_handler.keys():
            raise Exception("Unknown protocol %s"%proto)
        
        self._protocol_handler[proto].saveURI(uri, txt)


    def checkURI(self, uri):
        self._logger.debug("checks if %s exists"%uri)

        (proto, path) = Tools.splitURI(uri)
        if not proto in self._protocol_handler.keys():
            raise Exception("Unknown protocol %s"%proto)
        
        return self._protocol_handler[proto].checkURI(uri)

    
    def deleteURI(self, uri):
        self._logger.debug("delete %s"%uri)

        (proto, path) = Tools.splitURI(uri)
        if not proto in self._protocol_handler.keys():
            raise Exception("Unknonw protocol %S"%proto)
        
        self._protocol_handler[proto].deleteURI(uri)

        #FIXME
        #if proto == "mod":

