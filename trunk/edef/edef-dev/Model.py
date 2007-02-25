import os
import os.path
import fnmatch
from pyeditor.ModelArchive import eDevModelArchive
from modeditor.ModelModule import eDevModelModule
import re
import logging
from edef import Singleton
import Tools
from zipfile import ZipFile


class eDevModel:
    _d_local_mod_path = None
    _d_archive_list = None

    __metaclass__ = Singleton
    def __init__(self):
        #FIXME if local path not exists -> create
        self._d_local_mod_path = os.path.abspath(os.path.expanduser("~/.edef"))
        self._d_logger = logging.getLogger("edef.Developer")
        self._d_archive_list = {}
        self._d_module_list  = {}

        # search for zip files:
        file_list = os.listdir(self._d_local_mod_path)
        zipfile_list = fnmatch.filter(file_list, "*.zip")
        for filename in zipfile_list:
            print "Found archive: %s"%filename
            path = os.path.abspath( os.path.join(self._d_local_mod_path, filename ) )
            try:
                archive = eDevModelArchive(path)
            except:
                self._d_logger.exception("Exception while load zip %s"%path)
                continue
            self._d_archive_list["zip://"+filename] = archive


        # search for xml files:
        file_list = os.listdir(self._d_local_mod_path)
        xmlfile_list = fnmatch.filter(file_list, "*.xml")
        for filename in xmlfile_list:
            print "Found xml file %s"%filename
            path = os.path.abspath( os.path.join(self._d_local_mod_path, filename) )
            try:
                module = eDevModelModule(path)
            except:
                self._d_logger.exception("Exception while load xml %s"%path)
                continue
            self._d_module_list[module.GetURI()] = module



    def openURI(self, uri):
        print "Open URI: %s"%uri
        (proto, path) = Tools.splitURI(uri)
        if not proto in ["zip","py","mod"]:
            raise Exception("Unkonwn protocol: %s"%proto)
        
        if proto == "zip":
            if not path: return self._d_archive_list.keys()
            path = Tools.getArchive(uri)
            ar = self._d_archive_list["zip://"+path]
            flist = ar.getFileList("*.py")
            uri_list = []
            for f in flist: uri_list.append("py://"+path+"/"+f)
            return uri_list
        elif proto == "py":
            (ar, py) = Tools.splitPyFile(path)
            ar = self._d_archive_list["zip://"+ar]
            return ar.readFile(py)
        elif proto == "mod":
            if not path:
                print "List known modules: %s"%self._d_module_list.keys()
                return self._d_module_list.keys()
            mod = self._d_module_list[uri]
            return mod.getText()


    def saveURI(self, uri, txt):
        print "Save %s"%uri
        (proto, path) = Tools.splitURI(uri)
        if not proto in ["py","mod","zip"]:
            raise Exception("Unknown protocol %s"%proto)
        if path == "":
            raise Exception("Path not set!")
        
        if proto == "py":
            (ar_name, py_name) = Tools.splitPyFile(path)
            ar = self._d_archive_list["zip://"+ar_name]
            if not py_name in ar.getFileList("*.py"):
                ar.createFile(py_name, txt)
            else:
                ar.writeFile(py_name, txt)
        elif proto=="mod":
            if not uri in self._d_module_list.keys():
                # create module...
                mod_name = Tools.getModule(uri)+".xml"
                mod_path = os.path.join(self._d_local_mod_path, mod_name)
                if os.path.isfile(mod_path):
                    raise Exception("File %s allready exists!"%mod_path)
                f = open(mod_path,"w")
                f.write(txt)
                f.close()
                mod = eDevModelModule(mod_path)
                self._d_module_list[uri] = mod
                return
            # save module
            mod = self._d_module_list[uri]
            mod.setText(txt)
        elif proto=="zip":
            if uri in self._d_archive_list.keys():
                raise Exception("Archive %s allready known!"%uri)
            name = Tools.getArchive(uri)
            zip_path = os.path.join(self._d_local_mod_path, name)
            ZipFile(zip_path, "w")
            ar = eDevModelArchive(zip_path)
            self._d_archive_list[uri] = ar

    def checkURI(self, uri):
        (proto, path) = Tools.splitURI(uri)
        if not proto in ["zip","py","mod"]:
            raise Exception("Unknown protocol %s"%proto)

        if proto == "zip":
            return uri in self._d_archive_list.keys()
        elif proto == "mod":
            return uri in self._d_module_list.keys()
        elif proto == "py":
            (ar, py) = Tools.splitPyFile(path)
            if not "zip://"+ar in self._d_archive_list.keys():
                return False
            ar = self._d_archive_list["zip://"+ar]
            return py in ar.getFileList("*.py")


    def deleteURI(self, uri):
        (proto, path) = Tools.splitURI(uri)
        if not proto in ["zip","py","mod"]:
            raise Exception("Unknonw protocol %S"%proto)

        if proto == "py":
            (ar, py) = Tools.splitPyFile(path)
            ar = self._d_archive_list["zip://"+ar]
            ar.deleteFile(py)
        elif proto == "mod":
            if not uri in self._d_module_list.keys():
                raise Exception("Module %s not known"%uri)
            os.unlink(self._d_module_list[uri].getPath())
            del self._d_module_list[uri]
        elif proto == "zip":
            if not uri in self._d_archive_list.keys():
                raise Exception("Unknown archive %s"%uri)
            os.unlink(self._d_archive_list[uri].getPath())
            del self._d_archive_list[uri]
