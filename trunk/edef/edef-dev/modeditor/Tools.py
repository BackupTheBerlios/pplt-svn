import re


def getModuleName(uri):
    m = re.match("^mod://([\w|\-]+[/[\w|\-]+]*)$",uri)
    if not m: raise Exception("Invalid module uri: %s"%uri)
    
    ret=list()
    lst = m.group(1).split("/")
    for n in lst:
        if n != "": ret.append(n)
    return ".".join(ret)
        
