# ########################################################################## #
# StreamHexlifyModule.py
#
# 2006-11-22
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


from pplt import CDisposableModule, IStreamModule
from pplt import CStreamConnection
from pplt import ItemBusy
import weakref
import binascii




class StreamHexlifyModule(CDisposableModule, IStreamModule):
    _d_child = None 
    _d_child_id = None


    def connect(self, address=None, child=None):
        if self._d_child: raise ItemBusy("Only one child allowed.")

        con = CStreamConnection(self, child)
        self._d_child = weakref.proxy(con)
        self._d_child_id = con.identifier()
        return con
    
    
    
    def disconnect(self, con_id):
        if not self._d_child_id == con_id:
            raise Exception("Unkown connection ...")
        del self._d_child
        del self._d_child_id



    def write(self, con_id, data):
        if not self._d_child_id == con_id:
            raise Exception("Unkown connection ...")
        self._d_parent_connection.write(binascii.unhexlify(data))



    def read(self, con_id, length):
        if not self._d_child_id == con_id:
            raise Exception("Unkown connection ...")
        return binascii.hexlify(self._d_parent_connection.read(length))



    def notify_data(self):
        data = self._d_parent_connection.read(self._d_parent_connection.length())
        self._d_child.push(binascii.hexlify(data))


