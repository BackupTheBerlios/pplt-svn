""" This module holds the class CConnectionDatabase.

    All modules have an instance of this class as the attribute 
    C{_d_connections}. You can use it to manage all connections to your module
    by adding new connections you have created in the C{connect()} method to 
    it. To do this simply call C{self._d_connections.addConnection()}. So a 
    sample C{connect()} method of a module could look like:
    
    >>> def connect(self, address=None, child=None):
    >>>     # do something you may want to do
    >>>     con = CStreamConnection(self,child)
    >>>     self._d_connections.addConnection(con, address)
    >>>     return con 
    
    B{Note:} If you don't use the _d_connections connection table, you need to
    rewrite the C{is_busy()} method of the module to provide information about
    if there are connections to the module!
    
    Each connection you have created owns an identifier you can obtain the 
    identifier by calling C{con.identifier()}. The methods C{read()}, 
    C{rcve()}, C{write()}, C{send()}, C{disconnect()} get this identifier as 
    a parameter to identify the connection that calling. So you can get back 
    the connection instance from the connection table by calling 
    C{getConnectionByID()}. So a sample C{read()} method could look like:

    >>> def read(self, con_id, length):
    >>>     (con, addr) = self._d_connections.getConnectionByID(con_id)
    >>>     # do something

    Do remove (close) a connection from the table simple call the 
    C{remConnection()} method. So a simple C{disconnect()} method of a 
    module may look like:
    
    >>> def disconnect(self, con_id):
    >>>     self._d_connections.remConnection(con_id)
    """

# ########################################################################## #
# ConnectionDatabase.py
#
# 2006-09-01
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


from Exceptions import CorruptInterface, ItemBusy, ItemNotFound
import weakref

class CConnectionDatabase:
    """ This class should be used to managed all connection of a module. All 
        modules have an instance of this class as the _d_connections 
        attribute. Look at the L{core.ConnectionDatabase} module doc for more
        details."""
    _d_id_con_map = None
    _d_id_addr_map = None


    def __init__(self):
        """ """
        self._d_id_con_map = {}
        self._d_id_addr_map = {}

    
    
    def addConnection(self, con, addr=None):
        """ This method adds the given connection with the (optional) address 
            to the connection table. It is imposible to add a connection 
            twice. In this case an ItemBusy exception will be raised. 
            
            Example connect() method of a module:
            
            >>> def connect(self, address, child=None):
            >>>     con = CStreamConnection(self, child)
            >>>     self._d_connections.addConnection(con, address)
            
            @param con: Instance of the connection.
            @type con:  CConnection (or inherit)
            @param addr: Optional address of the connection.
            @type addr:  String"""
        from Connection import CConnection
        if not isinstance(con, CConnection):
            raise CorruptInterface("con param is not an inst of CConnection!")

        con_id = con.identifier()
        if(con_id in self._d_id_con_map.keys()):
            raise ItemBusy("The connection %s already exists in db!"%con_id)
        self._d_id_con_map[con_id] = weakref.proxy(con)
        self._d_id_addr_map[con_id] = addr



    def getConnectionByID(self, con_id):
        """ This method return a (connection, address-string) tuple of the 
            connection with the given id. If there is no connection with this 
            id an ItemNotFound exception will be raised. """
        if not con_id in self._d_id_con_map.keys():
            raise ItemNotFound("Connection ID %s not found in DB"%con_id)
        return self._d_id_con_map[con_id], self._d_id_addr_map[con_id]



    def getConnectionsByAddr(self, addr):
        """ This method will return a list of all connections with the given
            address. """
        if not addr in self._d_id_addr_map.values():
            raise ItemNotFound("No Conenctions with addr %s found in DB"%addr)

        con_list = []
        for con_id in self._d_id_addr_map.keys():
            if self._d_id_addr_map[con_id] == addr:
                if self._d_id_con_map[con_id] == None:
                    self.remConnection(con_id)
                else:
                    con_list.append(self._d_id_con_map[con_id])
        return con_list



    def remConnection(self, con_id):
        """ This method will delete the connection with the given id from the 
            connection table. If there is no connction with this id an 
            ItemNotFound exception will be raised. """
        if not con_id in self._d_id_con_map.keys():
            raise ItemNotFound("Not connection with id %s found in DB"%con_id)
        del self._d_id_con_map[con_id]
        del self._d_id_addr_map[con_id]


    
    def count(self, addr=None):
        """ This method will return the nummber of connections with the given 
            address. If the address is obmitted the count of all connections
            will be returned. """
        if None == addr:
            return len(self._d_id_con_map)
        return self._d_id_addr_map.values().count(addr)


