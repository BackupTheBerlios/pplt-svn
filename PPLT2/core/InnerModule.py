# ########################################################################## #
# InnerModule.py
#
# 2006-11-21
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

from Module import CModule
from Interfaces import IDisposable

class CInnerModule (CModule):
    _d_parent_connection = None


    def __init__(self, parent, address=None, parameters=None):
        # init super-class
        CModule.__init__(self, parameters)

        #FIXME Test if the connection will be closed if the module is 
        #      destroyed!
        self._d_parent_connection = parent.connect(address)



class CDisposableModule (CModule, IDisposable):
    _d_parent_connection = None;

    def __init__(self, parent, address=None, parameters=None):
        # init superclass
        CModule.__init__(self, parameters)

        self._d_parent_connection = parent.connect(address, self)


