# ########################################################################## #
# ReflectionModule.py
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



from core import CModule, IStreamModule
from core import CAsyncStreamConnection
from core import PPLTError, ItemBusy
from core import _fmtid;
import logging



class ReflectionModule(CModule, IStreamModule):
    _d_timeout  = None;
    _d_logger   = None;

    def __init__(self, parameters = None):
        CModule.__init__(self);

        try: self._d_timeout = float(parameters['timeout']);
        except: self._d_timeout = 0.1;

        self._d_logger = logging.getLogger("PPLT.core");
        self._d_logger.debug("Setup ReflectionModule with timeout %s"%self._d_timeout);

    def connect(self, addr, child=None):
        if not isinstance(addr,str):
            raise PPLTError("This module need addresses to connect.");

        self._d_logger.debug("connect with addr %s"%addr);
        
        if self._d_connections.count(addr)>=2:
            raise ItemBusy("There are allready 2 connection with addr %s"%addr);

        con = CAsyncStreamConnection(self, child, self._d_timeout);
        self._d_connections.addConnection(con,addr);
        return con;


    def disconnect(self, con_id):
        self._d_logger.debug("Close connection \"%s\" ..."%_fmtid(con_id));
        self._d_connections.remConnection(con_id);

    
    def write(self, con_id, data):
        (con,addr) = self._d_connections.getConnectionByID(con_id);
        if self._d_connections.count(addr) != 2:
            self._d_logger.warn("The other connection to %s is missing!", addr);

        cons = self._d_connections.getConnectionsByAddr(addr);
        if cons[0].identifier() == con_id: con = cons[1];
        else: con = cons[0];

        con.push(data);


    def connection_list(self):
        self._d_logger.debug("There are %i connections left:"%self._d_connections.count());
        for (cid, addr) in self._d_connections._d_id_addr_map.items():
            self._d_logger.debug("\t -> %s (%s)"%(addr, cid));

    def connection_count(self):
        return self._d_connections.count();
