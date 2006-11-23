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
from zipimport import zipimporter
import xml.dom.minidom
import sys
import imp
import xml.xpath


class CImporter:
    """ This simple class can seqrch for modules and load them."""

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
            the given address (you may need no address). 
            
            @return: An instance of the module."""

        if (parent and not address) or (address and not parent):
            raise Exception("If parent is set address have to!")

        # find and load meta-data
        (file_path, mod_meta) = self.getModuleMeta(mod_name)
        mod_archive = mod_meta.getArchive()
        
        # if no absolute path is give im mod-meta -> take it relative to the
        # meta-file
        if not os.path.isabs(mod_archive):
            mod_archive = os.path.join( os.path.dirname(file_path), mod_archive)
            
        # try to find module:
        zipimp = zipimporter(mod_archive);
        mod = zipimp.load_module(mod_meta.getClass());
        
        #load class from module
        try:
            cls = mod.__dict__[mod_meta.getClass()]
        except:
            raise ItemNotFound("Can't find class %s in %s [%s]"%
                        (mod_meta.getClass(), mod_archive, mod.__dict__.keys()))

        #instance class:
        if not parent:
            return cls(parameters)
        else:
            return cls(parent, address, parameters)



    def getModuleMeta(self, mod_name):
        file_path = self._find_module_meta(mod_name)

        mod_meta = ModuleMeta(file_path)
        return file_path, mod_meta





class ModuleMeta:
    _d_dom = None;

    def __init__(self, xml_file = None, xml_data=None):
        if xml_file:
            xml_data = open(xml_file).read()
        if xml_data:
            self._d_dom = xml.dom.minidom.parseString(xml_data)
            

    def getArchive(self):
        node = xml.xpath.Evaluate("./Module/Archive/text()",self._d_dom)
        return node[0].wholeText.strip()

    def getClass(self):
        node = xml.xpath.Evaluate("./Module/Class/text()",self._d_dom)
        return node[0].wholeText.strip()

    def getVersion(self):
        node = xml.xpath.Evaluate("./Module/Version/text()",self._d_dom)
        return node[0].wholeText.strip()

    def getDescription(self, lang="en"):
        node = xml.xpath.Evaluate("./Module/Description[@lang='%s']/text()"%lang, self._d_dom);
        return node[0].wholeText.strip();


