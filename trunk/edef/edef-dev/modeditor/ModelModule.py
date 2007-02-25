import os.path
import xml.dom.minidom
import xml.xpath

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

