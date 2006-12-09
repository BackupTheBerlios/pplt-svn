""" This module contains only the L{CModuleMeta} class that will be used by 
    the L{Importer} to get some (common) meta data about a module or assembly.

    This class will never instanced directly by the importer. Instead it will 
    use the L{CoreModuleMeta} or L{AssemblyMeta} classes which provide some 
    more detailed information about the module and also they provide a method
    called C{instance()} to intance the module.
"""

# ########################################################################## #
# ModuleMeta.py
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


import logging
import xml.dom.minidom
import xml.xpath
from Exceptions import ModuleImportError


class CModuleMeta:
    """ This class will be used by the L{Importer} to get some information 
        about how to load a module. The main target of this class is to check
        and expand parameter dicts to valid ones. Therefore a module hacker
        have not to care about if all parameters needed are given. """
    _d_dom              = None
    _d_logger           = None

    def __init__(self, xml_dom):
        """ The argument should hold a xml.dom.Document node, that contains 
            the module meta-data. """
        self._d_dom = xml_dom
        self._d_logger = logging.getLogger("PPLT.core")


    def getVersion(self):
        """ This method extracts the version-string from the module-meta. """
        node = xml.xpath.Evaluate("string(Version/text())",self._d_dom)
        return node.strip()


    def getAuthor(self):
        """ This method extracts the author-string from the meta-data. """
        node = xml.xpath.Evaluate("string(Author/text())",self._d_dom)
        return node.strip()


    def instance(self, parameters, parent=None, address=None):
        """ This method will be implemented by the L{CoreModuleMeta} or 
            L{AssemblyMeta} classes and provides a method to load and instance
            the module. """
        raise NotImplemented("This method have should load and instance a module")


    def checkDependencies(self):
        """ This method will be implemented by the L{CoreModuleMeta} or 
            L{AssemblyMeta} classes and provides the check if all needed 
            dependencies for the module or assembly are satisfied. This may
            be needed python-modules or other pplt-modules! """
        raise NotImplemented("This method should check all dependcies")


    def getDescription(self, lang="en"):
        """ This method will return the desciption of the module by language. 
            """
        query = "string(Description[@lang='%s']/text())"%lang
        node = xml.xpath.Evaluate(query, self._d_dom)
        return node.strip()


    def checkAndExpandParams(self, params):
        """ This method check if all needed parameters are present. That means
            that all parameters decribed in the module meta-file that have no
            "default" attribute have to be present in the given parameter 
            dict. If there is a parameter missing a ModuleImportError will be
            raised indicating that the module can't be seted up.

            In a second step the method will expand the given module dict with
            all missing parameters, that have a default value specified in the
            module meta-file. So a module developer don't need to check in 
            optional parameters are present. """
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








