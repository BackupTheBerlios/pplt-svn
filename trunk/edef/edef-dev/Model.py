import os
import os.path
import fnmatch
from ModelArchive import eDevModelArchive
import re

class eDevModel:
    _d_model_instance = None
    
    _d_local_mod_path = None

    _d_archive_list = None
    _d_module_tree  = None


    def instance():
        if eDevModel._d_model_instance is None:
            eDevModel._d_model_instance = eDevModel()
        return eDevModel._d_model_instance
    instance = staticmethod(instance)

    def __init__(self):
        #FIXME if local path not exists -> create
        self._d_local_mod_path = os.path.abspath(os.path.expanduser("~/.pplt"))

        self._d_archive_list = {}

        # search for zip files:
        file_list = os.listdir(self._d_local_mod_path)
        zipfile_list = fnmatch.filter(file_list, "*.zip")
        for filename in zipfile_list:
            print "Found archive: %s"%filename
            path = os.path.abspath( os.path.join(self._d_local_mod_path, filename ) )
            try:
                archive = eDevModelArchive(path)
            except:
                # FIXME log it!
                continue
            self._d_archive_list[archive.getName()] = archive


    def getArchive(self, name):
        return self._d_archive_list[name]

    def getArchives(self):
        return self._d_archive_list.keys()


