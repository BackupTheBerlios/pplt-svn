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


class dummy_inner(core.CInnerModule, core.IStreamModule):

    def connect(self, addr, child=None):
        con = core.CStreamConnection(self,child);
        self._d_connections.addConnection(con,addr);
        return con;

    def disconnect(self, con_id):
        self._d_connections.remConnection(con_id);


    def read(self, con_id, length):
        return self._d_parent_connection.read(length);

    def write(self, con_id, data):
        self._d_parent_connection.write(data);





class dummy_disposable(core.CDisposableModule, core.IStreamModule):
    _d_child = None;

    def connect(self, addr, child=None):
        if self._d_child:
            raise Exception("Only on connection!");
        con = core.CStreamConnection(self, child)
        self._d_connections.addConnection(con, addr)
        self._d_child = con.identifier();
        return con


    def disconnect(self, con_id):
        self._d_connections.remConnection(con_id)
        self._d_child = None;


    def read(self, con_id, length):
        self._d_parent_connection.read(length);


    def write(self, con_id, data):
        self._d_parent_connection.write(data)


    def notify_data(self):
        (con,addr) = self._d_connections.getConnectionByID(self._d_child)
        con.push(self._d_parent_connection.read(1024));





class dummy_root(core.CModule, core.IStreamModule):

    def connect(self, address, child=None):
        con = core.CStreamConnection(self, child);
        self._d_connections.addConnection(con,address);
        return con

    def disconnect(self, con_id):
        self._d_connections.remConnection(con_id);

    def con_count(self):
        return self._d_connections.count();





class testInnerModule(unittest.TestCase):

    def setUp(self):
        self._d_importer = core.CImporter("../modules");

    def testConCloseAtModDestroy(self):
        """ CLASS CInnerModule parent-connection close on module destroy """
        root = dummy_root()

        ch1 = dummy_inner(root, "1")
        ch2 = dummy_inner(root, "2")

        self.assertEqual(root.con_count(), 2)

        del ch1
        self.assertEqual(root.con_count(), 1)

        del ch2
        self.assertEqual(root.con_count(), 0)

        ch1 = dummy_disposable(root, "1")
        ch2 = dummy_disposable(root, "2")

        self.assertEqual(root.con_count(), 2)

        del ch1
        self.assertEqual(root.con_count(), 1)

        del ch2
        self.assertEqual(root.con_count(), 0)

        del root


    def testSimpleInnerModule(self):
        """ CLASS CInnerModule simple inner module test """
        root = self._d_importer.load("stream_reflection", {'timeout':'0.1'})
        child = dummy_inner(root, "1");

        con1 = child.connect("aaa");
        con2 = root.connect("1");

        con1.write("abc");
        self.assertEqual(con2.read(3), "abc");

        con2.write("def");
        self.assertEqual(con1.read(3), "def");

        con1.write("abc")
        con2.write("abc")
        con1.write("def")
        con2.write("def")
        self.assertEqual(con1.read(6), "abcdef")
        self.assertEqual(con2.read(3), "abc")
        self.assertEqual(con2.read(3), "def")

        con2.write("abc");
        del con1;
        del child;
        del con2;
        self.assertEqual( root.connection_count(), 0)


    def testSimpleDisposableModule(self):
        """ CLASS CDisposableModule simple disposable module test """
        root = self._d_importer.load("stream_reflection", {"timeout":'0.1'})
        child = dummy_disposable(root,"1");

        con1 = child.connect("aaa");
        con2 = root.connect("1");

        con2.write("abc");
        self.assertEqual(con1.length(), 3)
        con2.write("def");
        self.assertEqual(con1.length(), 6)
        self.assertEqual(con1.read(6), "abcdef")

        del con1;
        del con2;
        self.assertEqual( root.connection_count(), 1 )
        del child;
        self.assertEqual( root.connection_count(), 0 )

