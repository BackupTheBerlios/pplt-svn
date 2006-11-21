# ########################################################################## #
# testStreamConnection.py
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
from core import *;
import threading;

class DummyModule(CModule, IStreamModule):
    def connect(self, addr="", child=None):
        return CStreamConnection(self, child);

    def disconnect(self, con_id): pass;


class DummyDisposable(IDisposable):
    _d_data = None;
    _d_lock = None;
    _d_connection = None;

    def __init__(self, parent):
        self._d_data = "";
        self._d_lock = threading.Lock();
        self._d_lock.acquire();
        self._d_connection = parent.connect(None,self);
    
    def get_connection(self): return self._d_connection;

    def notify_data(self):
        self._d_data = self._d_connection.read(1024);
        self._d_lock.release();

    def reset(self):
        self._d_data = "";
        self._d_lock.acquire();

    def wait(self):
        self._d_lock.acquire();
        self._d_lock.release();

    def data(self): return self._d_data;



class testStreamConnection(unittest.TestCase):
    
    def setUp(self):
        pass;

    def tearDown(self):
        pass;

    
    def testPushParameterConstance(self):
        data = "1234567890";
        dummy = DummyModule({});
        con = dummy.connect();
        con.reserve();
        con.push(data, 3);
        self.assert_(data == "1234567890");
        self.assert_(con.read(3) == "123");
        self.assert_(con.length() == 0);



    def testEventStatus(self):
        dummy = DummyModule({});
        con = dummy.connect();
        
        status = con._d_events_enabled;
        self.assert_(not status);

        con.reserve()
        self.assert_(not con._d_events_enabled );
        con.release();
        self.assert_(status == con._d_events_enabled);



    def testEventThread(self):
        data    = "1234567890";
        dummy   = DummyModule({});
        dis     = DummyDisposable(dummy);
        con     = dis.get_connection();

        con.reserve();
        con.push(data,3);
        con.release();

        dis.wait();
        self.assert_(dis.data() == "123");
        dis.reset();

        con.reserve();
        con.push(data,3);
        con.release();

        dis.wait();
        self.assert_(dis.data() == "123");
        dis.reset();

