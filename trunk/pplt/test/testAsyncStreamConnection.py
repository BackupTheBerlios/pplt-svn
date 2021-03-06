import unittest;
from pplt import ItemBusy, PPLTError;
from pplt import IDisposable;
from pplt import CImporter;
import logging;
import threading;
import weakref;
import sys;
from pplt import _fmtid;


class DummyDisposable(IDisposable):
    _d_lock = None;
    _d_buffer = None;
    _d_connection = None;

    def __init__(self, parent, addr):
        self._d_lock = threading.Lock();
        self._d_lock.acquire();
        self._d_buffer = "";
        self._d_connection = parent.connect(addr, self);

    def notify_data(self):
        try:
            self._d_buffer = self._d_connection.read(1024);
        finally:
            self._d_lock.release();


    def get_data(self):
        return self._d_buffer;

    def get_refcount(self): return sys.getrefcount(self._d_connection)-1;

    def read(self, length):
        return self._d_connection.read(length);
    def reserve(self):
        return self._d_connection.reserve();
    def release(self):
        return self._d_connection.release();
    def wait(self):
        self._d_lock.acquire();
        self._d_lock.release();




class testAsyncStreamConnection(unittest.TestCase):
    _d_importer = None;
    
    def setUp(self):
        self._d_importer = CImporter("../modules");



    def testTimeout(self):
        """ CLASS CAsyncStreamConnection timeout exception """
        refl = self._d_importer.load("stream_reflection", {'timeout':'0.0001'});

        con1 = refl.connect("aaa");
        con2 = refl.connect("aaa");

        self.assertRaises(ItemBusy, con1.read, 1);


    def testConnectionCount(self):
        """ CLASS CAsyncStreamConnection connection count """
        refl = self._d_importer.load("stream_reflection", {'timeout':1});

        con1 = refl.connect("aaa");
        con2 = refl.connect("aaa");

        con3 = refl.connect("bbb");
        del con3;

        self.assertRaises(ItemBusy, refl.connect, "aaa");

        del con2;
        con2 = refl.connect("aaa");

        del con2;
        self.assert_(refl.is_busy());

        del con1;
        self.assert_(not refl.is_busy());



    def testDataIntegrity(self):
        """ CLASS CAsyncStreamConnection data integrity """
        refl = self._d_importer.load("stream_reflection", {'timeout':1});
         
        con1  = refl.connect("aaa");
        con2  = refl.connect("aaa");
        
        con1.write("123");
        self.assert_( "123" == con2.read(3) );
        del con2

        dis = DummyDisposable(refl, "aaa");

        dis.reserve();
        con1.write("1234567890");
        self.assert_( dis.read(3) == "123" );
        dis.release();

        dis.wait();
        self.assert_( dis.get_data() == "4567890" );
        del con1;
        del dis;

        self.assert_( not refl.is_busy() );
