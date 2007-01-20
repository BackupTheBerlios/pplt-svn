import os.path
import os
import zipfile
import fnmatch

class eDevModelArchive:
    _d_path = None
    _d_name = None
    _d_zipfile = None

    def __init__(self, path):
        if not zipfile.is_zipfile(path):
            raise Exception("File %s is not a zip-file!"%path)
        
        self._d_path = path
        (folder, filename) = os.path.split(self._d_path)
        (self._d_name ,ext) = os.path.splitext(filename)
        



    def getName(self):
        return self._d_name
    
    def getPath(self):
        return self._d_path

    def getFileList(self, pattern="*"):
        filelist = zipfile.ZipFile(self._d_path, "r").namelist()
        return fnmatch.filter(filelist, pattern)

    def getFileContent(self, fname):
        return zipfile.ZipFile(self._d_path, "r").read(fname)

