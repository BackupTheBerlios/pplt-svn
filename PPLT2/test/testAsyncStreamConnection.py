import unittest;
from core import CModule, IStreamModule;
from core import ItemBusy, PPLTError;
from core import CAsyncStreamConnection;
from core import IDisposable;
import logging;
import threading;
import weakref;
import sys;
from core import _fmtid;


class ReflectionModule(CModule, IStreamModule):
    _d_timeout  = None;
    _d_logger   = None;

    def __init__(self, timeout=1):
        CModule.__init__(self);

        self._d_timeout = timeout;
        self._d_logger = logging.getLogger("PPLT.core");


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
        if cons[0].Identifier() == con_id: con = cons[1];
        else: con = cons[0];

        con.push(data);


    def list_connection(self):
        self._d_logger.debug("There are %i connections left:"%self._d_connections.count());
        for (cid, addr) in self._d_connections._d_id_addr_map.items():
            self._d_logger.debug("\t -> %s (%s)"%(addr, cid));





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

    def testTimeout(self):
        refl = ReflectionModule(0.1);

        con1 = refl.connect("aaa");
        con2 = refl.connect("aaa");

        self.assertRaises(ItemBusy, con1.read,1);


    def testConnectionCount(self):
        refl = ReflectionModule(1);

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
        refl = ReflectionModule(1);
         
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
