
import unittest
from pplt import CImporter
from pplt import IDisposable
from pplt import ItemBusy
import threading

class Dummy(IDisposable):
    _d_connection = None
    _d_mutex      = None
    _d_data       = None

    def __init__(self, parent, addr):
        self._d_connection = parent.connect(addr, self);
        self._d_mutex = threading.Event()
        self._d_mutex.clear()


    def wait(self):
        data = None
        self._d_mutex.wait(1)
        if self._d_mutex.isSet(): data = self._d_data;
        self._d_mutex.clear()
        return data

    def notify_data(self):
        self._d_data = self._d_connection.recv();
        self._d_mutex.set()

    def reserve(self):
        self._d_connection.reserve()
    def release(self):
        self._d_connection.release()

    def recv(self): return self._d_connection.recv()




class testSequenceConnection (unittest.TestCase):

    def setUp(self):
        self._d_importer = CImporter("../modules")

    def testEventThread(self):
        """ CLASS CSequenceConnection events """
        root = self._d_importer.load("sequence_reflection", {'timeout':'0.001'})

        con1 = root.connect("1")
        con2 = Dummy(root,"1")

        con1.send("abc")
        self.assertEqual(con2.wait(), "abc")


        con2.reserve()
        con1.send("abc")
        con1.send("def")
        self.assertEqual(con2.recv(), "abc")
        con2.release()
        self.assertEqual(con2.wait(), "def")


    def testConnectionClose(self):
        """ CLASS CSequenceConnection close/count """
        root = self._d_importer.load("sequence_reflection", {'timeout':'0.001'})

        con1 = root.connect("1")
        con2 = root.connect("1")

        del con2

        con2 = root.connect("1")

        self.assertRaises(ItemBusy, root.connect, "1")

    
    def testStreamInterface(self):
        """ CLASS CSequenceConnection stream interface """
        root = self._d_importer.load("sequence_reflection", {'timeout':'0.001'})

        con1 = root.connect("1")
        con2 = root.connect("1")

        con2.write("abc")
        self.assertEqual(con1.read(2), "ab")
        con2.write("def")
        self.assertEqual(con1.recv(), "c")
        self.assertEqual(con1.read(3), "def")
        con2.write("ghi")
        self.assertEqual(con1.recv(), "ghi")

