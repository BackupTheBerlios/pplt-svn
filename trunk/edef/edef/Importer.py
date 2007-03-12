""" The importer can be used to import modules and assemblies. 
    An module is a python-script zipped into an archive. Additionally there 
    should be a description-file containing meta-data about the module. In 
    contrast, an assembly consists only of a xml file that describe how to
    assemble one or more module or assemblies to get a new one. 
    
    To find out how to write a module, please check U{http://pplt.berlios.de}"""



# ########################################################################## #
# Importer.py
#  
# 2007-01-24
# Copyright 2007 Hannes Matuschek
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




import xml.dom.minidom
import xml.xpath
import logging
from Exceptions import ModuleImportError
import os
import os.path
from glob import glob
import sys
from ModuleMeta import ModuleMeta, AssemblyMeta
from Singleton import Singleton



class Importer:
    """ The importer searches by default the paths C{~/.edef} and 
    C{sys.prefix+"/edef/} for the module to load. But you can define
    some new searchpaths by instanceing the Importer with a list of 
    strings containg the new search-paths. """

    _d_search_path = None
    
    __metaclass__ = Singleton
    def __init__(self, base_path=None):
        """ The constructor takes the optional parameter C{base_path} which
            can define the new searchpaths. This should be C{None}, for the
            default searchpaths or a list of strings. For example:
            C{imp = Importer( ['/path/to/modules', '/other/path'] )}. """
        self._d_search_path=[os.path.abspath(os.path.expanduser('~/.edef')),
                             os.path.abspath(os.path.join(sys.prefix, 'edef'))]

        self._d_logger = logging.getLogger("edef.core")

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
            raise ModuleImportError("Module %s can't be found in %s"%(mod_name, self._d_search_path))
        
        return file_path;

    
    def load(self, mod_name, parameters=None):
        """ This method should be used to load a specific module. The 
            parameter C{mod_name} specifies the (full) name of the module. It 
            makes no differenc if you want to load a module or an assembly!
            The parameter C{parameters} can specifiy the parameters for the 
            module. The description-file of the module will be used to check 
            if all needed parameters are specified. If not a 
            L{ModuleImportError} exception will be raised! Additionally this 
            method will expand all optional parameters for the module. So the
            module-developer will not need to check the parameters. """
        # find and load meta-data
        (file_path, mod_meta) = self.getModuleMeta(mod_name)

        #check and expand parameters:
        if not parameters:
            parameters = {}
        mod_meta.checkAndExpandParameters(parameters)

        #check dependencies:
        mod_meta.checkDependencies()

        self._d_logger.debug("Instance module %s with params %s"%(mod_name,parameters))
        return mod_meta.instance(parameters)


    def loadGrafical(self, canvas, coordinates, name, parameters=None):
        """ Loads a module as it's grafical representaion. The instance 
            behaves like a normal module. """
        # find module meta:
        (file_path, mod_meta) = self.getModuleMeta(name)

        #check and expand parameters:
        if not parameters: parameters = {}
        mod_meta.checkAndExpandParameters(parameters)

        #check dependencies:
        mod_meta.checkDependencies()

        if not mod_meta.getGraficClass():
            self._d_logger.debug("Instance default grafic")
            # if no grafic-class is specified -> load default grafic-module
            try: from edef.dev.circuit import DefaultGraficModule
            except:
                self._d_logger.exception("Unabel to load default grafic module!")
                raise ModuleImportError("Unable to load defualt grafic for %s"%name)
            return DefaultGraficModule(canvas, coordinates, name, parameters)
        # if a graficmodule is specified
        self._d_logger.debug("Instance defined graficmodule %s with params %s"%(mod_name,parameters))
        return mod_meta.instanceGrafical(canvas, coordinates, parameters)
   

    def getModuleMeta(self, mod_name):
        """ This method will return either a L{ModuleMeta} or L{AssemblyMeta} 
            instance depending on if you specified a module or an assembly 
            with C{mod_name}. 
            
            This instance contains some meta-information about the module/assembly. """
        file_path = self._find_module_meta(mod_name)
    
        try:
            xml_dom = xml.dom.minidom.parse(file_path).documentElement
        except DOMException, e:
            raise ModuleImportError("Parse error: File %s: %s"%(file_path, str(e)))

        typ = xml.xpath.Evaluate("local-name(.)", xml_dom)
        if typ == "Module":
            mod_meta = ModuleMeta(xml_dom, file_path)
        elif typ == "Assembly":
            # FIXME implement!
            raise NotImplemented("Assembly loading is not implemented yet")
            #mod_meta = AssemblyMeta(xml_dom, self)
        else:
            raise ModuleImportError("Unknown module type %s in %s"%(typ,file_path))

        return file_path, mod_meta


    def listModules(self):
        """ This method will return a list with all modules found in search-path """
        tmp_list = []
        mod_list = []
        for path in self._d_search_path:
            tmp_list += glob(os.path.join(path,"*.xml"))
        for file_name in tmp_list:
            if os.path.isfile(file_name):
                (path, file_name) = os.path.split(file_name)
                (file_name, ext)  = os.path.splitext(file_name)
                mod_list.append(file_name)
        return mod_list


