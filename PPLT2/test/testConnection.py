# ########################################################################## #
# testConnection.py
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


import unittest;
import core;

class DummyModule(core.CModule):
    _d_con_count = 0;

    def __init__(self):
        core.CModule.__init__(self);
        self._d_con_count = 0;
    
    def connect(self, addr=None, child=None):
        if(addr == None):
            raise PPLTError("Need Address!");
        con = core.CConnection(self);
        self._d_connections.addConnection(con, addr);
        self._d_con_count += 1;
        return(con);

    def disconnect(self, con_id):
        self._d_connections.remConnection(con_id);
        self._d_con_count -=1;

    def count(self): return self._d_con_count;



class testConnection(unittest.TestCase):

    def testConnectionClose(self):
        # This module checks if the close() method of the module will be
        # called if the connection will be destroyed!
        dummy = DummyModule();
        con = dummy.connect("test");
        del con;
        self.assert_( dummy.count() == 0 );
