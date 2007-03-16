from Module import DynamicModule, InputWrapper
from Output import ValueOutput

# FIXME: Write documentation!

# ########################################################################## #
# Assembly.py
#
# 2007-03-16
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


class Assembly(DynamicModule):
    _d_module_table = None
    _d_io_list = None

    def __init__(self, module_table, io_list):
        DynamicModule.__init__(self)
        self._d_module_table = module_table
        self._d_io_list = io_list
        self._d_logger.debug("Instance Assembly with modules (%s) and IOs (%s)"%(module_table, io_list))


    def create_input(self, name):
        if not name in self._d_io_list.keys():
            raise Exception("Unkown input %s"%name)
        return InputWrapper(self, name)


    def create_output(self, name):
        if not name in self._d_io_list.keys():
            raise Exception("Output \"%s\" not in list! %s"%(name,self._d_io_list.keys()))
        # create output            
        out = ValueOutput()
        # find redirection
        (alias, oname) = self._d_io_list[name].split(".",2)
        mod = self._d_module_table[alias]
        mout = getattr(mod, oname)
        # add my output as input to redirection
        mout += out
        return out


    def input_dispacher(self, name, value, kwargs=None):
        # find redirection
        (alias, iname) = self._d_io_list[name].split(".",2)
        mod = self._d_module_table[alias]
        mod_in = getattr(mod, iname)
        mod_in(value)
        
