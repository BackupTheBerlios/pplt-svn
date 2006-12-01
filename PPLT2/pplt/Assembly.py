""" An assembly is a simple container grouping some other assemblies and/or 
    modules to an logical entity, that behave like a single python implemented
    module. The major difference between a assembly and a simple module is
    that an assembly can not be instanced directly (because it is only a 
    container). Instead a assembly can only be loaded and instanced by a
    CImporter instance. But there is no difference between loading a module
    and loading a assembly using the importer. """
from Object import CObject

class CAssembly(CObject):
    _d_ns_id_map  = None
    _d_id_mod_map = None


    def __init__(self, parameters=None):
        CObject.__init__(self)
        self._d_ns_id_map  = {}
        self._d_id_mod_map = {}
  


    #def __del__(self):
    #    # try to free all embeded modules...
    #    # done...
    #    #FIXME: I do not know how to destroy the modules in a proper way
    #    pass



    def connect(self, address, child=None):
        # Extract the namespace of an embeded module from address.
        # Then get this module and call connect to it using the address
        # reduced by the namespace.

        try:
            (ns,addr) = address.split(":",1)
        except:
            raise Exception("Invalid address-format: \"%s\" is not in form of namespace:address"%address);
        if not ns in self._d_ns_id_map.keys():
            raise Exception("Unable to conenct to %s: NS %s not known!"%(address, ns));

        mod = self._d_id_mod_map[self._d_ns_id_map[ns]]
        if len(addr) == 0:
            addr = None
        return mod.connect(addr)



    def is_busy(self):
        # while the assembly has no disconnect method (because the 
        # disconnect method of the embeded module will be called) the assembly
        # can not know if there are connections to any embeded modules. 
        # Otherwise there are connections between the embeded modules so the
        # assembly can not check if there are connections to it! 
        # FIXME This should be solved!
        return False

    
    
    def _add_module(self, mod_instance, name_space=None, to=None):
        """ This method will be used by the importer to add a module.
            If the parameter C{to} is given, the module instance will be 
            stored as a child of the module to.

            @param mod_instance: Instance of the module that will be added to
                the assembly. This have to be not a weak reference!
            @type mod_instance: Any derived from CModule or CAssambly.

            @param to: If this optional parameter is given, it have to be an 
                id of a module allready known by the assembly that will be 
                used as the parent of the module added. """

        if isinstance(name_space,(str,unicode)):
            self._d_ns_id_map[name_space]=mod_instance.identifier()
        self._d_id_mod_map[mod_instance.identifier()] = mod_instance


