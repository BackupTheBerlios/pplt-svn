""" This module contains the L{CImporter} class. """

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
from CoreModuleMeta import CCoreModuleMeta



class CImporter:
    """ This simple class can search for modules and load them."""

    _d_search_path = None;

    def __init__(self, base_path=None):
        """ The base_path specifies the path where to search for modules. If 
            it is a string or a list of string the importer will try to find 
            the modules there. Otherwise the importer will look at 
            "sys.prefix"/pplt/ or at ~/.pplt for modules. """

        self._d_search_path=[os.path.abspath(os.path.expanduser('~/.pplt')),
                             os.path.abspath(os.path.join(sys.prefix, 'pplt'))]

        if isinstance(base_path, str):
            self._d_search_path = [base_path]
        elif isinstance(base_path, [list, tuple]):
            self._d_search_path = base_path



    def _find_module_meta(self, mod_name):
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
            
            @return: An instance of the module."""

        if (parent and not address) or (address and not parent):
            raise Exception("If parent is set address have to!")

        # find and load meta-data
        (file_path, mod_meta) = self.getModuleMeta(mod_name)

        #check if module is inner-module if parent is set:
        if parent and not mod_meta.isInnerModule():
            raise PPLTError("An root-module can't be attached to an other!")

        #check and expand parameters:
        if not parameters:
            parameters = {}
        mod_meta.checkAndExpandParams(parameters)

        #check dependencies:
        mod_meta.checkDependencies()

        return mod_meta.instance(parameters, parent, address)
        

    def getModuleMeta(self, mod_name):
        file_path = self._find_module_meta(mod_name)
    
        xml_dom = xml.dom.minidom.parse(file_path).documentElement

        typ = xml.xpath.Evaluate("local-name(.)", xml_dom)
        if typ == "Module":
            mod_meta = CCoreModuleMeta(xml_dom, file_path)
        elif typ == "Assembly":
            mod_meta = CAssamblyMeta(xml_dom, self)
        else:
            raise ModuleImportError("Unknown module type %s in %s"%(typ,file_path))

        return file_path, mod_meta



