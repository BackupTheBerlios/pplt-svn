import xml.xpath
from ModuleMeta import CModuleMeta
from Assembly import CAssembly
from Exceptions import ModuleImportError



class CAssemblyMeta(CModuleMeta):
    _d_importer = None


    def __init__(self, dom, importer):
        CModuleMeta.__init__(self, dom)

        self._d_importer = importer
        
        # check grammar version:
        vers_attr = xml.xpath.Evaluate("string(/Assembly/@version)", self._d_dom)
        if not vers_attr == "1.0":
            raise InvalidGrammarVersion("Can't handle grammar version %s"%vers_attr)



    def checkDependencies(self):
        nodes = xml.xpath.Evaluate("/Assembly/Require/Module/text()", self._d_dom)

        self._d_logger.debug("Checking %i dependencies"%len(nodes))
        for node in nodes:
            mod_name = node.wholeText.strip()
            try:
                self._d_importer._find_module_meta(mod_name)
            except Exception, e:
                raise ModuleImportError("Unresolved dependencies: Module %s not found"%mod_name)



    def instance(self, parameters, parent=None, address=None):
        # instance an empty assembly:
        asm = CAssembly()

        # get all "root" modules from assembly:
        nodes = xml.xpath.Evaluate("/Assembly/Setup/Load",self._d_dom)
        for node in nodes:
            mod_name = node.getAttribute("module")
                
            namespace = None
            if node.hasAttribute("namespace"):
                namespace= node.getAttribute("namespace")

            mod_param = self._module_parameters(node,parameters)
                
            if not parent:
                mod = self._d_importer.load(mod_name, mod_param)
            else:
                mod = self._d_importer.load(mod_name, mod_param, parent, address)
            asm._add_module(mod, namespace)
                
            cnodes = xml.xpath.Evaluate("./Load",node)
            for cnode in cnodes:
                self._instance_module(cnode, parameters, mod, asm)

        return asm
        


    def _instance_module(self, node, parameters, parent, asm):
        namespace = None
        address   = None

        mod_name = node.getAttribute("module")
        
        if node.hasAttribute("namespace"):
            namespace = node.getAttribute("namespace")

        if xml.xpath.Evaluate("count(./Address)>0",node):
            address = self._module_address(node, parameters)

        mod_para = self._module_parameters(node, parameters)
        self._d_logger.debug("Try to load %s with addr %s and params %s"%(mod_name, address, mod_para))
        mod = self._d_importer.load(mod_name, mod_para, parent, address)
        asm._add_module(mod, namespace, parent.identifier())

        cnodes = xml.xpath.Evaluate("./Load",node)
        for cnode in cnodes:
            self._d_instance_module(cnode, parameters, mod, asm)



    def _module_parameters(self, node, parameters):
        mod_params = {}

        # select all module-parameters that value is defined by a 
        # asm-parameter:
        pnodes = xml.xpath.Evaluate("./Parameter[child::ValueOf]", node);
        for pnode in pnodes:
            name = pnode.getAttribute("name")
            var_name = xml.xpath.Evaluate("string(./ValueOf/text())",pnode).strip()
            mod_params[name] = parameters[var_name]

        # select all static parameters:
        pnodes = xml.xpath.Evaluate("./Parameter[not(child::ValueOf)]", node);
        for pnode in pnodes:
            name = pnode.getAttribute("name")
            value = xml.xpath.Evaluate("string(./text())",pnode).strip()
            mod_params[name]=value

        return mod_params



    def _module_address(self, node, parameters):
        if xml.xpath.Evaluate("count(./Address)>1",node):
            raise Exception("More that one address specified!")
        
        if xml.xpath.Evaluate("count(./Address/ValueOf)>1",node):
            raise Exception("There can only be on <ValueOf> inside a <Address>")

        if xml.xpath.Evaluate("count(./Address/ValueOf)=1",node):
            var_name = xml.xpath.Evaluate("string(./Address/ValueOf/text())",node).strip()
            return parameters[var_name]

        return xml.xpath.Evaluate("string(./Address/text())",node).strip()


