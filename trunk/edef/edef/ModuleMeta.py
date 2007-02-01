""" This file defines classes that represent metadata of Modules and 
    Assemblies.

    Normaly this classes are used by the L{Importer} class to load and
    instance a module/assembly. So you do not need to know a lot about this  
    classes.

    Additionally they provide some methods that useses this metadata for 
    example the C{checkAndExpandParamters()} method, that checks the given
    parameters if all needed parameters for this module are defined and expand
    the parameter list with undefined default values. So the module-developer 
    does not need to check the parameters in his module code. There are two 
    classes, one for the meta-data of modules and one for assemblies. 

    Booth types implement methods to load (or assemble) the module described.
    """

#TODO
#   - first of all; implement the AssemblyMeta
#   - extend ModuleMeta to provide all data 
#   - write some tools to check a module or assembly files
#   - find and solve all FIXMEs


import logging
import xml.xpath
import xml.dom.minidom
from Exceptions import ModuleImportError
import os
import os.path
from zipimport import zipimporter
import re


class ModuleBaseMeta:
    _d_logger = None
    _d_dom    = None

    def __init__(self, xml_dom):
        self._d_logger = logging.getLogger("edef.core")
        # FIXME check if dom is a valid XML-DOM
        self._d_dom = xml_dom
        # FIXME check grammar-version!

    
    def getAuthor(self):
        node = xml.xpath.Evaluate("string(Author/text())",self._d_dom)
        if not node: return None
        return node.strip()


    def getVersion(self):
        node = xml.xpath.Evaluate("string(Version/text())",self._d_dom)
        return node.strip()


    def getDescription(self, lang="en"):
        query = "string(Description[@lang='%s']/text())"%lang
        node = xml.xpath.Evaluate(query, self._d_dom)
        return node.strip()


    def checkAndExpandParameters(self, params):
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


    def getElement(self, xp_query):
        return xml.xpath.Evaluate(xp_query, self._d_dom)


    def instance(self, paramters):
        raise NotImplemented("This method should be implemented by Module- or AssemblyMeta!")

    def checkDependencies(self):
        raise NotImplemented("This method should be implemented by Module- or AssemblyMeta!")





class ModuleMeta(ModuleBaseMeta):
    _d_file_path = None

    def __init__(self, dom, file_path):
        ModuleBaseMeta.__init__(self, dom)
        self._d_file_path = file_path


    def getArchive(self):
        node = xml.xpath.Evaluate("string(Archive/text())",self._d_dom)
        return node.strip()
       

    def getClass(self):
        node = xml.xpath.Evaluate("string(Class/text())",self._d_dom)
        return node.strip()
        

    def checkDependencies(self):
        # to check all dependencies get all <PyModule> tags and try to find 
        # them using imp.find_module()
        nodes = xml.xpath.Evaluate("/Module/Require/PyModule/text()", self._d_dom)
        for node in nodes:
            mod_name = node.wholeText.strip()
            #FIXME this can't handle doted names
            (fp, path, desc) = imp.find_module(mod_name)
            if fp: fp.close()
 
    
    def instance(self, parameters):
        # if no absolute path is given im mod-meta -> take it relative to the
        # meta-file
        mod_archive = self.getArchive()
        if not os.path.isabs(mod_archive):
            mod_archive = os.path.join( os.path.dirname(self._d_file_path), mod_archive)
         
        # try to find module-archive:
        try:
            zipimp = zipimporter(mod_archive)
        except Exception, e:
            raise ModuleImportError("Unable to open module-archive %s: %s"
                    %(mod_archive, str(e)))
        # try to find module in module-archive
        full_class_name = self.getClass()
        if re.match("^\w+\.\w+$", full_class_name):
            (file_name, class_name) = re.split("^(\w+).(\w+)$", full_class_name,2)
        elif re.match("^\w+$", full_class_name):
            file_name = full_class_name
            class_name = full_class_name
        else:
            raise ModuleImportError("Invalid %s class-name in %s!"%(full_class_name, self._d_file_path) )
        mod = zipimp.load_module(file_name);

        #load class from module
        try:
            cls = mod.__dict__[class_name]
        except:
            raise ModuleImportError("Can't find class %s in %s [%s]"%
                        (self.getClass(), mod_archive, mod.__dict__.keys()))
        # instance:
        return cls(**parameters)
        




# FIXME Implement AssemblyMeta-Class!
class AssemblyMeta(ModuleBaseMeta): pass
