""" This module contains the L{CImporter} class. 
    
    There are two types of Modules that can be imported with this importer. 
    First of all the I{coremodules}. These are modules that are implemented by
    pythonscripts ziped into an archive. Additional there is a file describing
    these modules. The other type is called I{assembly} this one is an XML 
    file describing how to assamble several coremodules to a new one. Booth
    types behave identical, so you do not have to care about what type of 
    module you have loaded. 
    
    To be able to load modules you have to instance an L{CImporter} class.
    The constructor takes only one optional parameter C{base_path} which 
    specifies a list of path names where the importer should look for modules.
    If you obmit the parameter the importer will try to find the modules
    in C{sys.prefix+'/pplt'} and C{'~/.pplt'}. 
    
    To load and instance a module simply do following:
    
    >>> import pplt
    >>> # ... do something ...
    >>> importer = CImporter()
    >>> mod = importer.load("module_name", {"mod_param":"value"})
    >>> # ... now do something with the module
  
    One of the advantages of the pplt is the combineing of modules. So you can
    attach some module to other. The modules, that are attachable to other are
    called I{inner modules} (L{InnerModule}). If you want to load an inner 
    module and attach it to an other one, you should do following:

    >>> import pplt
    >>>
    >>> importer = CImporter()
    >>> root = importer.load("root_module")
    >>> inner = importer.load("inner_module", None, root, "address")

    This example loads the module "root_module" without any parameters.
    Then is loads a module called "inner_module" also without parameters
    and connect them with the root module using the addess "address".
    Now the "inner_module" is attached to the "root_module"

    """

# ########################################################################## #
# Importer.py
#
# 2006-11-20
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

from Exceptions import *
import os.path
import xml.dom.minidom
import sys
import imp
import xml.xpath
import logging
from CoreModuleMeta import CCoreModuleMeta
from AssemblyMeta   import CAssemblyMeta


class CImporter:
    """ This simple class can search for modules and load them.
        
        This is the unversal importer class for all pplt modules. This 
        includes coremodule and assemblies. The load() method for loading
        and instancing a module is the same for booth types of modules. Also
        booth types behave indentical, so you do not know what kind of module
        you are loading. """

    _d_search_path = None;

    def __init__(self, base_path=None):
        """ The base_path specifies the path where to search for modules. If 
            it is a string or a list of string the importer will try to find 
            the modules there. Otherwise the importer will look at 
            "sys.prefix"/pplt/ or at ~/.pplt for modules.
            
            @param base_path: A string or a list of strings specifieing where
            to search for modules. """

        self._d_search_path=[os.path.abspath(os.path.expanduser('~/.pplt')),
                             os.path.abspath(os.path.join(sys.prefix, 'pplt'))]

        self._d_logger = logging.getLogger("PPLT.core")

        if isinstance(base_path, str):
            self._d_search_path = [base_path]
        elif isinstance(base_path, (list, tuple)):
            self._d_search_path = base_path



    def _find_module_meta(self, mod_name):
        """ Internal used method to find module-metadata files. This method
            searches for a file named mod_name+".xml" in all paths given to
            the constructor. """
        file_path  = None;
        for path in self._d_search_path:
            if os.path.isfile( os.path.join(path, mod_name+".xml") ):
                file_path = os.path.abspath( os.path.join(path, mod_name+".xml") )
        
        if not file_path:
            raise ItemNotFound("Module %s can't be found in %s"%(mod_name, self._d_search_path))
        
        return file_path;



    def load(self, mod_name, parameters=None, parent=None, address=None):
        """ This method will try to load the given module from the base
            path(s) and to connect it (if given) to the parent with
            the given address (you may need no address). If the module or its
            meta-data can't be found a ItemNotFound will be raised. 
           
            @param mod_name: The parameter specifies the name of the module
                to load.
            @param parameters: This argument specifies the parameter-dict used
                to setup the module. This dict will be checked and extended by
                the importer. Look at L{ModuleMeta} for more details.
            @param parent: If you want to load an "inner"-module, you need to
                specifiy the parent module instance the new module will be 
                attached to.
            @param address: Specifies the address of the connection to the
                parent.
            @return: An instance of the module."""

        if (parent and not address) or (address and not parent):
            raise Exception("If parent is set address have to!")

        # find and load meta-data
        (file_path, mod_meta) = self.getModuleMeta(mod_name)

        #check and expand parameters:
        if not parameters:
            parameters = {}
        mod_meta.checkAndExpandParams(parameters)

        #check dependencies:
        mod_meta.checkDependencies()
        
        self._d_logger.debug("Instance module %s with addr %s and params %s"%(mod_name,address,parameters))
        return mod_meta.instance(parameters, parent, address)
        

    def getModuleMeta(self, mod_name):
        """ Returns the module meta-data object for the given module.
            
            This method is used internal to get the meta-data of an module.
            The meta-data is specified in the description file of the module.
            The meta-data contains information about the module version, 
            author, dependencies, parameters and maybe a translated 
            description of the module and its parameters. In case of an 
            assembly the meta-data also contains the information about how to
            load the assembly. """
        file_path = self._find_module_meta(mod_name)
    
        try:
            xml_dom = xml.dom.minidom.parse(file_path).documentElement
        except DOMException, e:
            raise ModuleImportError("Parse error: File %s: %s"%(file_path, str(e)))

        typ = xml.xpath.Evaluate("local-name(.)", xml_dom)
        if typ == "Module":
            mod_meta = CCoreModuleMeta(xml_dom, file_path)
        elif typ == "Assembly":
            mod_meta = CAssemblyMeta(xml_dom, self)
        else:
            raise ModuleImportError("Unknown module type %s in %s"%(typ,file_path))

        return file_path, mod_meta



