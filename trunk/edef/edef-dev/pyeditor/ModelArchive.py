import os
import os.path
import fnmatch
from zipfile import ZipFile, is_zipfile
from tempfile import TemporaryFile
import logging
import fnmatch
from edef.dev.Config import eDevConfig as Config
from Tools import splitPyFile, getPyFile, isPyFileURI
from Tools import getArchive, isArchiveURI



class Model:
    def __init__(self):
        self._logger = logging.getLogger("edef.dev")
        self._base_path = Config().getBasePath()
        self._archive_list = dict()

        # search for zip files:
        file_list = os.listdir(self._base_path)
        zipfile_list = fnmatch.filter(file_list, "*.zip")
        for filename in zipfile_list:
            self._logger.debug("Found archive: %s"%filename)
            path = os.path.abspath( os.path.join(self._base_path, filename ) )
            try:
                archive = eDevModelArchive(path)
            except:
                self._d_logger.exception("Exception while load zip %s"%path)
                continue
            self._archive_list["zip://"+filename] = archive


    def openURI(self, uri):
        # open "zip://" retunrs a list of all known zip files
        if uri == "zip://":
            return self._archive_list.keys()
        # open "zip://archive_name.zip" returns a list of pythonfiles of the 
        # given archive
        elif uri in self._archive_list.keys():
            archive = self._archive_list[uri]
            lst = archive.getFileList("*.py")
            for i in range(len(lst)):
                lst[i] = uri+"/"+lst[i]
            return lst
        # open "zip://archive-name.zip/path/to/python-file.py" returns the 
        # content of the given python file.
        (aname, fname) = splitPyFile(uri)
        try: archive = self._archive_list["zip://"+aname]
        except: raise Exception("Archive zip://%s not known"%aname)
        return archive.readFile(fname)


    def saveURI(self, uri, data=""):
        # save "zip://archive-name.zip" will creat a new archive
        if isArchiveURI(uri):
            if uri in self._archive_list.keys():
                return
            archive = getArchive(uri)
            path = os.path.join(self._base_path, archive)
            ZipFile(path,"w")
            self._archive_list[uri] = eDevModelArchive(path)
        # save "zip://archive-name.zip/path/to/python-file.py creates a new 
        # python file with given content or overrides existing ones
        elif isPyFileURI(uri):
            self._logger.debug("save pyfile %s"%uri)
            (aname, fname) = splitPyFile(uri)
            try: archive = self._archive_list["zip://"+aname]
            except: raise Exception("Archive zip://&s not found"%aname)
            if not fname in archive.getFileList("*.py"):
                archive.createFile(fname, data)
            else:
                archive.writeFile(fname, data)
        else: raise Exception("Unable to write %s: Invalid URI?"%uri)


    def deleteURI(self, uri):
        if isArchiveURI(uri):
            if not uri in self._archive_list.keys():
                raise Exception("Unknown archive %s"%uri)
            aname = getArchive(uri)
            path = os.path.join(self._base_path, aname)
            os.unlink(path)
            del self._archive_list[uri]
        elif isPyFileURI(uri):
            (aname, fname) = splitPyFile(uri)
            if not "zip://"+aname in self._archive_list.keys():
                raise Exception("Unknown archive zip://%s"%aname)
            archive = self._archive_list["zip://"+aname]
            if not fname in archive.getFileList("*.py"):
                raise Exception("Unknown file %s in zip://%s"%(fname, aname))
            archive.deleteFile(fname)
        else:
            raise Exception("Invalid URI %s?"%uri)


    def checkURI(self, uri):
        if isArchiveURI(uri): return uri in self._archive_list.keys()
        elif isPyFileURI(uri):
            (aname, fname) = splitPyFile(uri)
            try: archive = self._archive_list["zip://"+aname]
            except: return False
            return fname in archive.getFileList("*.py")
                

    def isURIEditable(self, uri):
        if not isPyFileURI(uri): return False
        return True

    def isURIWriteable(self, uri):
        # FIXME if archive is writeable -> return True
        return True



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
