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
#   - extend ModuleMeta to provide all data 
#   - write some tools to check a module or assembly files
#   - find and solve all FIXMEs


import logging
import xml.xpath
import xml.dom.minidom
import os
import os.path
from zipimport import zipimporter
import re
from Exceptions import ModuleImportError
import Importer
from Assembly import Assembly


class ModuleBaseMeta:
    """ This is the base-class for the L{ModuleMeta} and L{AssemblyMeta} 
        classes. Normaly these classes are instanced by the L{Importer} and 
        you will never need to instance these classes directly. """
    _d_logger = None
    _d_dom    = None

    def __init__(self, xml_dom):
        """ Constructor. Takes only an XML-DOM tree. """
        self._d_logger = logging.getLogger("edef.core")
        # FIXME check if dom is a valid XML-DOM
        self._d_dom = xml_dom
        # FIXME check grammar-version!

    
    def getAuthor(self):
        """ This method returns the name of the author of the module/assembly,
            if defined. Otherwise it will return an empty string. """
        # FIXME test me
        node = xml.xpath.Evaluate("string(Author/text())",self._d_dom)
        if not node: return None
        return node.strip()


    def getVersion(self):
        """ Returns the version-string of the module."""
        # FIXME test me
        node = xml.xpath.Evaluate("string(Version/text())",self._d_dom)
        return node.strip()


    def getDescription(self, lang="en"):
        """ This method will return the description of the module/assembly.
            If it is not defined it will return an empty string. The optional
            attribute I{lang} specifies the language of the description 
            returned. Note: If there is no description specified in the given
            language the method will return an empty string. """
        # FIXME test me
        query = "string(Description[@lang='%s']/text())"%lang
        node = xml.xpath.Evaluate(query, self._d_dom)
        return node.strip()


    def checkAndExpandParameters(self, params):
        """ This method can be used to expand the given parameters in respect 
            to this module. This method will be used by the Importer to expand
            the given parameters before instanceing the module/assembly. So
            the module-developer doesn't need to care about if there are all
            (even optional) parameters present. 
            This method will raise a I{ModuleImportError] if a non-optional
            parameter is missing. """
        # to check if all "needed" parameters are present:
        #   - get all parameter names from the meta that have no "default" 
        #     attribute
        #   - check if all these parameters are present in the parameter dict
        nodes = xml.xpath.Evaluate("Requires/Parameter[not(@default)]", self._d_dom)
        for node in nodes:
            if not node.getAttribute("name") in params.keys():
                raise ModuleImportError("Can't import: Needed parameter \"%s\" not set!"%
                                        (node.getAttribute("name")))

        # to expand the parameters, get all parameters that have the "default"
        # attribute and remove from this list all parameters, that are presend
        # and add the rest
        nodes = xml.xpath.Evaluate("Requires/Parameter[@default]", self._d_dom)
        for node in nodes:
            name = node.getAttribute("name")
            defval = node.getAttribute("default")
            if not name in params.keys():
                params[name] = defval


    def getParameterDescription(self, name, lang="en"):
        # FIXME test me
        """ This method will return the description-string for the given 
            parameter. The language can be selected. """
        query = "string(Requires/Parameter[@name='%s']/Description[@lang=%s]/text())"%(name, lang)
        node = xml.xpath.Evaluate(query, self._d_dom)
        return node.strip()

    
    def getInputs(self, token=".*"):
        # FIXME test me
        """ This method returns a list of inputs. You can specify a regexp. 
            that should match the name of the input """
        query = "Provides/Input"
        qlst = xml.xpath.Evaluate(query, self._d_dom)
        lst = []
        for node in qlst:
            if re.match(token, node.getAttribute("name")):
                lst.append(node.getAttribute("name"))
        return lst

    def getOutputs(self, token=".*"):
        # FIXME test me
        """ This method returns (like getInputs) the list of outputs, that
            match the given regexp. If non is given all outputs are retuned. 
            """
        query = "Provides/Output"
        qlst = xml.xpath.Evaluate(query, self._d_dom)
        lst = []
        for node in qlst:
            if re.match(token, node.getAttribute("name")):
                lst.append(node.getAttribute("name"))
        return lst


    def getIODescription(self, name, lang="en"):
        # FIXME test me
        """ This method can be used to get the description of an input or
            output. In the meta-data of a module you can describe a input or
            output. This method take a complete name like C{i_input} and an 
            optional parameter I{lang}. The method will return a string if
            there is a description of the give pin in the proper language."""
        mo = re.match(name, "^o_(.*)$")
        mi = re.match(name, "^i_(.*)$")
        if mo:
            query = "string(Provides/Output[name='%s']/Description[@lang='%s'])"%(mo.group(1), lang)
            return xml.xpath.Evaluate(query, self._d_dom)
        elif m1:
            query = "string(Provides/Input[name='%s']/Description[@lang='%s'])"%(mi.group(1), lang)
            return xml.xpath.Evaluate(query, self._d_dom)
        raise Exception("Invalid name for an input or output: %s"%name)


    def getElement(self, xp_query):
        """ This method can be used to query elements of the module/assembly
            xml-description. This can be used to access elements that are not
            defined in the Module/Assembly grammar. """
        # FIXME test me
        return xml.xpath.Evaluate(xp_query, self._d_dom)


    def instance(self, paramters):
        """ This method should be overridden to implement the instanceing. """
        raise NotImplemented("This method should be implemented by Module- or AssemblyMeta!")

    def checkDependencies(self):
        """ This method should be overridden to check if all defined 
            Dependencies are satisfied """
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
        nodes = xml.xpath.Evaluate("/Module/Requires/PyModule/text()", self._d_dom)
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
            m = re.match("^(\w+).(\w+)$", full_class_name)
            file_name = m.group(1)
            class_name = m.group(2)
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
        




# FIXME test AssemblyMeta-Class!
class AssemblyMeta(ModuleBaseMeta):
    _d_importer = None

    def __init__(self, dom):
        ModuleBaseMeta.__init__(self, dom)
        self._d_importer = Importer.Importer()
        # FIXME check if dom is Assembly DOM        
        

    def instance(self, parameters):
        mod_table = dict()
        
        # load all modules defined in Assembly
        mods_to_load = self._modules_to_load()
        for (mod_name, alias) in mods_to_load:
            if alias in mod_table.keys():
                raise ModuleImportError("Alias \"%s\" defined twice"%alias)
            mod_table[alias] = self._load_module_by_alias(alias, parameters)

        # connect modules
        nodes = xml.xpath.Evaluate("/Assembly/Setup/Link",self._d_dom)
        for node in nodes:
            (frm_mod, frm_out) = node.getAttribute("from").split(".",2)
            (to_mod,  to_in)   = node.getAttribute("alias").split(".",2)
            mod = getattr(mod_table[frm_mod], frm_out)
            mod += getattr(mod_table[to_mod], to_in)

        # list IOs
        io_list = dict()
        nodes = xml.xpath.Evaluate("/Assembly/Provides/Input", self._d_dom)
        self._d_logger.debug("Found inputs: %s"%nodes)
        for node in nodes:
            name = "i_"+node.getAttribute("name")
            redir = node.getAttribute("link")
            io_list[name] = redir
        nodes = xml.xpath.Evaluate("/Assembly/Provides/Output", self._d_dom)
        self._d_logger.debug("Found outputs: %s"%nodes)
        for node in nodes:
            name = "o_"+node.getAttribute("name")
            redir = node.getAttribute("link")
            io_list[name] = redir


        # instance an Assembly 
        return Assembly(mod_table, io_list)


    def checkDependencies(self):
        # FIXME test me
        # get list of neede modules:
        nodes = xml.xpath.Evaluate("/Assembly/Require/Module/text()", self._d_dom)
        mod_list = self._d_importer.listModules()

        for node in nodes:
            mod_name = node.wholeText.strip()
            self._d_logger.debug("Check for module \"%s\""%mod_name)
            if not mod_name in mod_list:
                raise ModuleImportError("Can't load assembly: Module %s not found"%mod_name)


    def _modules_to_load(self):
        ret = list()
        
        query = "/Assembly/Setup/Module[@alias]"
        nodes = xml.xpath.Evaluate(query, self._d_dom)
        for node in nodes:
            ret.append( (node.getAttribute("name"), node.getAttribute("alias")) )
        return ret


    def _load_module_by_alias(self, alias, params):
        query = "/Assembly/Setup/Module[@alias='%s']"%alias
        mod_node = xml.xpath.Evaluate(query, self._d_dom)[0]

        mod_parameters = dict()
        # get parameters
        par_nodes = xml.xpath.Evaluate("Parameter[ValueOf]", mod_node)
        for node in par_nodes:
            ref_name = xml.xpath.Evaluate("ValueOf/text()",node).strip()
            if not ref_name in params.keys():
                raise ModuleImportError("Unable to instance Assembly: Parameter %s is not set!"%ref_name)
            ref_value = self.params[ref_name]
            name = node.getAttribute("name")
            mod_parameters[name] = ref_value

        par_nodes = xml.xpath.Evaluate("Parameter[not(child::ValueOf)]", mod_node)
        for node in par_nodes:
            ref_value = xml.xpath.Evaluate("text()",node).strip()
            name = node.getAttribute("name")
            mod_parameters[name] = ref_value

        mod_name = xml.xpath.Evaluate("string(@name)", mod_node).strip()

        return self._d_importer.load(mod_name, mod_parameters)

