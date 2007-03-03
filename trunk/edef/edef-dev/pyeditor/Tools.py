import re


def getArchive(uri):
    m = re.match("^zip://([\w|\-]+[/[\w|\-]+]*\.zip)$", uri)
    if not m: raise Exception("Invalid URI for proto zip: %s"%uri)
    return m.group(1)


def getPyFile(uri):
    m = re.match("^zip://[\w|\-]+[/[\w|\-]+]*\.zip/([\w|\-]+[/[\w|\-]+]*\.py)$", uri)
    if not m: raise Exception("Invalid URI for proto zip: %s"%uri)
    return m.group(1)


def splitPyFile(uri):
    m = re.match("^zip://([\w|\-]+[/[\w|\-]+]*\.zip)/([\w|\-]+[/[\w|\-]+]*\.py)$", uri)
    if not m: raise Exception("Invalid URI for proto zip: %s"%uri)
    return (m.group(1), m.group(2))


def isArchiveURI(uri):
    try:
        getArchive(uri)
        return True
    except:
        return False


def isPyFileURI(uri):
    try:
        getPyFile(uri)
        return True
    except:
        return False


