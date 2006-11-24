import xml.dom.minidom
import xml.xpath
from Exceptions import ModuleImportError

class CModuleMeta:
    _d_dom              = None

    def __init__(self, xml_dom):
        self._d_dom = xml_dom


    def getVersion(self):
        node = xml.xpath.Evaluate("Version/text()",self._d_dom)
        return node[0].wholeText.strip()


    def getAuthor(self):
        node = xml.xpath.Evaluate("Author/text()",self._d_dom)
        return node[0].wholeText.strip()


    def isInnerModule(self):
        raise NotImplemented("This method have to be implemented by CCoreModule and CAssembly")

    def instance(self, parameters, parent=None, address=None):
        raise NotImplemented("This method have should load and instance a module")

    def checkDependencies(self):
        raise NotImplemented("This method should check all dependcies")


    def getDescription(self, lang="en"):
        node = xml.xpath.Evaluate("Description[@lang='%s']/text()"%lang, self._d_dom)
        return node[0].wholeText.strip()


    def checkAndExpandParams(self, params):
        """ This method check if all needed parameters are present. That means
            that all parameters decribed in the module meta-file that have no
            "default" attribute have to be present in the given parameter 
            dict. If there is a parameter missing a ModuleImportError will be
            raised indicating that the module can't be seted up.

            In a second step the method will expand the given module dict with
            all missing parameters, that have a default value specified in the
            module meta-file. So a module developer don't need to check in 
            optional parameters are present. """
        # to check if all "needed" parameters are present:
        #   - get all parameter names from the meta that have no "default" 
        #     attribute
        #   - check if all these parameters are present in the parameter dict
        nodes = xml.xpath.Evaluate("Require/Parameter[not(@default)]", self._d_dom)
        for node in nodes:
            if not node.getAttribute("name") in params.keys():
                raise ModuleImportError("Can't import: Needed parameter \"%s\" not set!"%
                                        (node.getAttribute("name")))

        # to expand the parameters, get all parameters that have the "default"
        # attribute and remove from this list all parameters, that are presend
        # and add the rest
        nodes = xml.xpath.Evaluate("Require/Parameter[@default]", self._d_dom)
        for node in nodes:
            name = node.getAttribute("name")
            defval = node.getAttribute("default")
            if not name in params.keys():
                params[name] = defval








