import os.path
import os
import fnmatch
from zipfile import ZipFile, is_zipfile
from tempfile import TemporaryFile


class eDevModelArchive:
    _d_path = None
    _d_name = None
    _d_zipfile = None

    def __init__(self, path):
        if not is_zipfile(path):
            raise Exception("File %s is not a zip-file!"%path)
        
        self._d_path = path
        self._d_readable = os.access(self._d_path, os.R_OK)
        self._d_writeable = os.access(self._d_path, os.W_OK)

        (folder, filename) = os.path.split(self._d_path)
        (self._d_name ,ext) = os.path.splitext(filename)
        



    def getName(self):
        return self._d_name
    
    def getPath(self):
        return self._d_path

    def isReadable(self):
        return self._d_readable
    def isWriteable(self):
        return self._d_writeable

    def getFileList(self, pattern="*"):
        filelist = ZipFile(self._d_path, "r").namelist()
        return fnmatch.filter(filelist, pattern)

    def readFile(self, fname):
        return ZipFile(self._d_path, "r").read(fname)

    def createFile(self, fname, data):
        zf = ZipFile(self._d_path, "a")
        if fname in zf.namelist():
            zf.close()
            raise Exception("File allready exists!")
        zf.writestr(str(fname), data)
        zf.close()
        

    def writeFile(self, fname, data):
        f_b_table = {}
        zf = ZipFile(self._d_path, "r")
        cont = zf.namelist()

        if not fname in cont:
            raise Exception("File %s not found in archive %s"%(fname, self._d_path))
            
        for name in cont:
            if name == fname: continue
            f_b_table[name] = TemporaryFile()
            f_b_table[name].write(zf.read(name))
            f_b_table[name].seek(0)
        zf.close()

        # FIXME restore rights!
        zf = ZipFile(self._d_path, "w")
        for name in cont:
            if name == fname:
                zf.writestr(name, data)
            else:
                zf.writestr(name, f_b_table[name].read())
        zf.close()


    def deleteFile(self, fname):
        f_b_table = { }
        zipf = ZipFile(self._d_path, "r")
        acont = zipf.namelist()

        if not fname in acont:
            raise Exception("File %s not found in archive %s"%(fname, self._d_path))
        
        for name in acont:
            if name == fname: continue
            f_b_table[name] = TemporaryFile()
            f_b_table[name].write(zipf.read(name))
            f_b_table[name].seek(0)
        zipf.close()

        # FIXME restore rights!
        zipf = ZipFile(self._d_path, "w")
        for name in f_b_table.keys():
            zipf.writestr(name, f_b_table[name].read())
        zipf.close()
