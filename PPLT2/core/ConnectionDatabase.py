""" This module holds the class CConnectionDatabase """

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


from Exceptions import CorruptInterface, ItemBusy, ItemNotFound;
import weakref;

class CConnectionDatabase: 
    """ This class should be used to managed all connection of a module. """
    _d_id_con_map = None;
    _d_id_addr_map = None;


    def __init__(self):
        self._d_id_con_map = {};
        self._d_id_addr_map = {};

    
    
    def addConnection(self, con, addr=None):
        from Connection import CConnection;
        if not isinstance(con, CConnection):
            raise CorruptInterface("The con parameter should be an instance of CConnection!");

        con_id = con.identifier();
        if(con_id in self._d_id_con_map.keys()):
            raise ItemBusy("The connection %s already exists in db!"%con_id);
        self._d_id_con_map[con_id] = weakref.proxy(con);
        self._d_id_addr_map[con_id] = addr;



    def getConnectionByID(self, con_id):
        if not con_id in self._d_id_con_map.keys():
            raise ItemNotFound("Connection ID %s not found in DB"%con_id);
        return (self._d_id_con_map[con_id], self._d_id_addr_map[con_id]);



    def getConnectionsByAddr(self, addr):
        if not addr in self._d_id_addr_map.values():
            raise ItemNotFound("No Conenctions with addr %s found in DB"%addr);

        con_list = [];
        for con_id in self._d_id_addr_map.keys():
            if self._d_id_addr_map[con_id] == addr:
                if self._d_id_con_map[con_id] == None: 
                    self.remConnection(con_id);
                else: con_list.append(self._d_id_con_map[con_id]);
        return con_list;



    def remConnection(self, con_id):
        if not con_id in self._d_id_con_map.keys():
            raise ItemNotFound("Not connection with id %s found in DB"%con_id);
        del self._d_id_con_map[con_id];
        del self._d_id_addr_map[con_id];


    
    def count(self, addr=None):
        if None == addr: return len(self._d_id_con_map);
        return self._d_id_addr_map.values().count(addr);


