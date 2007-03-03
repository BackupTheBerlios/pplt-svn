import xml.xpath
import re


def GetXMLContent(node):
    txt = xml.xpath.Evaluate("string(text())",node)
    return txt.strip()



# ====== URI stuff ======

def splitURI(uri):
    m = re.match("^(zip|py|mod|shell)://(.*)$", uri)
    return (m.group(1), m.group(2))

