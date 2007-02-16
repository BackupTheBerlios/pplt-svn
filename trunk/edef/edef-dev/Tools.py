import xml.xpath
import re


def GetXMLContent(node):
    txt = xml.xpath.Evaluate("string(text())",node)
    return txt.strip()



# ====== URI stuff ======

def splitURI(uri):
    m = re.match("^(zip|py|mod|shell)://(.*)$", uri)
    return (m.group(1), m.group(2))

def splitArchive(path):
    m = re.match("^([\w|\-]+[/[\w|\-]+]*\.zip)$", path)
    return m.group(1)

def splitPyFile(path):
    m = re.match("^([\w|\-]+[/[\w|\-]+]*\.zip)/([\w|\-]+[/[\w|\-]+]*\.py)$", path)
    return (m.group(1),m.group(2))

def splitModule(path):
    m = re.match("^(\w+[/\w+]*)$", path)
    return m.group(1)

def getArchive(uri):
    (proto, path) = splitURI(uri)
    if proto == "zip":
        return splitArchive(path)
    elif proto == "py":
        (ar, py) = splitPyFile(path)
        return ar
    return None

def getPyFile(uri):
    (proto, path) = splitURI(uri)
    if proto == "py":
        (ar, py) = splitPyFile(path)
        return py
    return None

def getModule(uri):
    (proto, path) = splitURI(uri)
    if not proto == "mod": return None
    path = splitModule(path)
    plist = path.split("/")
    return ".".join(plist)

