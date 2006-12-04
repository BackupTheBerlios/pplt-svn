""" An assembly is a simple container grouping some other assemblies and/or 
    modules to an logical entity, that behave like a single python implemented
    module. 
    
    The major difference between an assembly and a simple module is
    that an assembly can not be instanced directly (because it is only a 
    container). Instead a assembly can only be loaded and instanced by a
    CImporter instance. But there is no difference between loading a module
    and loading a assembly using the importer. 
    
    To write a assembly simply create a file named I{filename}C{.xml} into
    directory C{~/.pplt/} or C{sys.prefix+"/pplt/"}, the importer will look 
    there for modules and assemblies.

    An assembly is a small xml file that describes how several other 
    assemblies or modules have to be combined to produce a new "module".
    The grammar of the xml description language can be found in the 
    trax file I{trax/trax_assembly.xml} at the source distribution.
    Otherwise look at the projectpage at berlios: U{http://pplt.berlios.de}.
    If there is no description of the assembly-description-grammar please 
    remind me to write one.
    """

# ########################################################################## #
# Assembly.py
#
# 2006-12-03
# Copyright 2006 Hannes Matuschek
# hmatuschek@gmx.net
# ########################################################################## #
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# ########################################################################## #



from Object import CObject
import weakref


class CAssembly(CObject):
    """ The CAssembly class is a simple container for other modules. Therefore
        it is not usefull to instance this class directly. Use a L{CImporter} 
        instance instead. 

        >>> import pplt
        >>> 
        >>> imp = pplt.CImporter()
        >>> asm = imp.load("a_assambly", {'param1':'val1'})
        >>> con1 = asm.connect("namespace:address")
        >>> asm.is_busy()
        True
        >>> del con1
        >>> asm.is_busy()
        False

        As you may noticed, this looks like loading a normal module. This is 
        one of the targets of an assembly. But the address have to be in a 
        porper format. Because the assambly can contain several (even 
        identical) modules, there may be some address collisions. To prevent
        this problem each encapsulated module can get a I{namespace}. This
        namespace have to be prexiefd to the address. To seperate the 
        namespace from the address (which also may contain namespace aliases)
        a single colon is used. Therefore a namespace should never contain 
        colons!

        Once a assembly is loaded you can use it like any other module!
        """
    _d_ns_id_map  = None
    _d_id_mod_map = None
    _d_connections = None

    def __init__(self):
        CObject.__init__(self)
        self._d_ns_id_map  = {}
        self._d_id_mod_map = {}
        self._d_connections = []



    def connect(self, address, child=None):
        """ This method is a wrapper for all connect methods of the 
            encapsulated modules. The given address should contain a namespace
            prefix, so that the assembly can determ witch module the connetion
            will be established to. A namespace should be seperated to the 
            address with a colon. Therefore a namespace alias whould never 
            contain a colon. 
            
            @param address: Specifies the namespace and address of the 
                connection in a proper format. For example:
                "NAMESPACE:ADDRESS"
            @type address: string
            
            @param child: This optional parameter specifies an instance that 
                will be called to handle an event.
            @type child: Any derived from IDisposable """
        # Extract the namespace of an embeded module from address.
        # Then get this module and call connect to it using the address
        # reduced by the namespace.
        try:
            (ns,addr) = address.split(":",1)
        except:
            raise PPLTError("Invalid address-format: \"%s\" is not in form of namespace:address"%address);
        if not ns in self._d_ns_id_map.keys():
            raise PPLTError("Unable to conenct to %s: NS %s not known!"%(address, ns));

        mod = self._d_id_mod_map[self._d_ns_id_map[ns]]
        if len(addr) == 0:
            addr = None
        con = mod.connect(addr)
        self._d_connections.append(weakref.ref(con))
        return con



    def is_busy(self):
        """ This method will return True if there are any connections to an
            encapsulated module and False other wise. This method can be used
            to determ if it would be save to unload an assembly, which should
            never been done if there are any connections left. """
        for ref in self._d_connections:
            if ref() != None:
                return True
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


