""" This module contains only the class L{CCoreModuleMeta}. """

# ########################################################################## #
# CoreModuleMeta.py
#
# 2006-11-25
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

import xml.xpath
import imp
import os.path
from zipimport import zipimporter
from ModuleMeta import CModuleMeta
from Exceptions import *
from InnerModule import CInnerModule, CDisposableModule

class CCoreModuleMeta (CModuleMeta):
    """ This class will be used by the L{Importer} to get meta-data about a 
        core-module (a pplt-module implemented in python) and to instance such
        a module."""

    _d_file_path = None

    def __init__(self, xml_dom, file_path):
        """ This contructor will also call the constuctor of the L{ModuleMeta}
        class. 
        
        @param xml_dom: The xml.dom.Document node containing the meta-data. 
        @type xml_dom: xml.dom.Document
        @param file_path: The filepath of the module description. This path 
            will be used to find the archive containing the module
            implentation. If the archive path specified in the module meta 
            is not absolute the archive will be searched relative to the 
            module meta file. 
        @type file_path: string """            

        CModuleMeta.__init__(self, xml_dom)
    
        self._d_file_path = file_path

        # check grammar version:
        vers_attr = xml.xpath.Evaluate("/Module/@version", self._d_dom)
        if not vers_attr[0].nodeValue == "1.0":
            raise InvalidGrammarVersion("Can't handle grammar version %s"%vers_attr[0].nodeValue)


    def getArchive(self):
        """ This method will extract the (relative) path of the archive 
            containing the module-implementation. This archive is a simple
            zip file with all modules zipped into it. Think of it like a .jar
            """
        node = xml.xpath.Evaluate("/Module/Archive/text()",self._d_dom)
        return node[0].wholeText.strip()


    def getClass(self):
        """ This method will return the class name of the module. But also the
            name of the python file containing the module-class. For example 
            if your module should be named I{SolveAllMyProblems} there B{must}
            be a file named C{SolveAllMyProblems.py} inside the zip archive 
            and this file have to contain a class definition named
            C{SolveAllMyProblems}. """
        node = xml.xpath.Evaluate("/Module/Class/text()",self._d_dom)
        return node[0].wholeText.strip()


    def checkDependencies(self):
        """ This method will check if all dependencies of the module is
            satisfied if not it will raise an exception. Dependencies are
            currently only python modules or packages needed by the module."""
        # to check all dependencies get all <PyModule> tags and try to find 
        # them using imp.find_module()
        nodes = xml.xpath.Evaluate("/Module/Require/PyModule/text()", self._d_dom)
        for node in nodes:
            mod_name = node.wholeText.strip()
            #FIXME this can't handle doted names
            (fp, path, desc) = imp.find_module(mod_name)
            if fp: fp.close()
 

    def instance(self, parameters, parent=None, address=None):
        """ This method will return an instance of the module. Therfore you 
            may have to specify the parameters needed to load the module. If 
            you want to instance an inner module, that will be attached to an
            other module, you have to specify also the parent and the address
            of the connection between the modules. The parent is the one the
            I{new} module will be connected to. """
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
        mod = zipimp.load_module(self.getClass());

        #load class from module
        try:
            cls = mod.__dict__[self.getClass()]
        except:
            raise ItemNotFound("Can't find class %s in %s [%s]"%
                        (self.getClass(), mod_archive, mod.__dict__.keys()))

        #instance class:
        if not issubclass(cls, (CInnerModule,CDisposableModule)):
            self._d_logger.debug("Module %s instance with params %s"%(self.getClass(),parameters))
            return cls(parameters)
        else:
            self._d_logger.debug("InnerModule %s instance with addr %s and params %s"%(self.getClass(), address, parameters))
            return cls(parent, address, parameters)


