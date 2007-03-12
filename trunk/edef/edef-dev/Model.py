import os
import re
import os.path
import fnmatch
import logging
from edef import Singleton
import Tools
from zipfile import ZipFile
from Config import eDevConfig as Config

class eDevModel:
    _logger             = None
    _protocol_handler   = None

    __metaclass__ = Singleton
    def __init__(self):
        self._logger = logging.getLogger("edef.Developer")
        self._protocol_handler = dict()
        # create base_path if not exists:
        self._base_path = os.path.normpath( os.path.expanduser("~/.edef") )
        if not os.path.isdir(self._base_path):
            self._logger.debug("Private edef-dir %s doesn't extist -> create")
            os.mkdir(self._base_path)


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


    def isEditable(self, uri):
        self._logger.debug("check if %s is editable")
        (proto, path) = Tools.splitURI(uri)
        if not proto in self._protocol_handler.keys():
            raise Exception("Unknonw protocol %S"%proto)
        
        self._protocol_handler[proto].isURIEditable(uri)


    def isWriteable(self, uri):
        self._logger.debug("check if %s is editable")
        (proto, path) = Tools.splitURI(uri)
        if not proto in self._protocol_handler.keys():
            raise Exception("Unknonw protocol %S"%proto)
        
        self._protocol_handler[proto].isURIEditable(uri)
        


