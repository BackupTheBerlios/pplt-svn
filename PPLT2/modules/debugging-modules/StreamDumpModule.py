# ########################################################################## #
# StreamDumpModule.py
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


from core import IStreamModule, CDisposableModule
from core import ItemBusy
from core import CStreamConnection




class StreamDumpModule (CDisposableModule, IStreamModule):

    def connect(self, address = None, child = None):
        """ Connects to this module. Address should be None, "read", "write" 
            or "event" """
        if address == None: address = "None";

        if not address in ["None", "read", "write", "event"]:
            raise Exception("Unknown address %s!"%address)
        
        if not self._d_connections.count(address) == 0:
            raise ItemBusy("Address %s allready in use!"%address)

        con = CStreamConnection(self, child)
        self._d_connections.addConnection(con,address)
        return con



    def disconnect(self, con_id):
        """ Closes the connection with the given connection id. """
        self._d_connections.remConnection(con_id);



    def read(self, con_id, length):
        (con, addr) = self._d_connections.getConnectionByID(con_id)

        if addr in ['read', 'write', 'event']:
            return ""
        
        data = self._d_parent_connection.read(length)
        
        if self._d_connections.count("read") == 1:
            con = self._d_connections.getConnectionsByAddr("read")[0]
            con.push(data)

        return data



    def write(self, con_id, data):
        (con, addr) = self._d_connections.getConnectionByID(con_id)

        if addr in ['read', 'write', 'event']: return

        if self._d_connections.count("write") == 1:
            con = self._d_connections.getConnectionsByAddr("write")[0]
            con.push(data)

        self._d_parent_connection.write(data)



    def notify_data(self):
        if not self._d_connections.count("None")==1:
            return
        
        data = self._d_parent_connection.read(self._d_parent_connection.length())
        
        if self._d_connections.count("event")==1:
            con = self._d_connections.getConnectionsByAddr("event")[0]
            con.push(data);

        con = self._d_connections.getConnectionsByAddr("None")[0]
        con.push(data)



