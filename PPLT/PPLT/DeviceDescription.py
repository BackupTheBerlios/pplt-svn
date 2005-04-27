import xml.dom.minidom;
import Setup;

def LoadSetup(FileName):
    doc = xml.dom.minidom.parse(FileName);
    setupnodes = doc.getElementsByTagName('Setup');
    return(Setup.Setup(setupnodes[0].firstChild));