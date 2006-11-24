import unittest
import core
from core import ItemBusy

class testStreamHexlifyModule( unittest.TestCase ):

    def setUp(self):
        self._d_importer = core.CImporter("../modules");
        

    def testHexlify(self):
        """ MODULE stream_hexlify (hexlify) """
        root = self._d_importer.load("stream_reflection",{'timeout':'0.1'})
        hexly= self._d_importer.load("stream_hexlify",None, root, "1");

        con1 = hexly.connect("aaa");
        con2 = root.connect("1");

        con2.write("abc");
        self.assertEqual(con1.read(6), "616263");
        
        
    def testUnhexlify(self):
        """ MODULE stream_hexlify (unhexlify) """
        root = self._d_importer.load("stream_reflection",{'timeout':'0.1'})
        hexl = self._d_importer.load("stream_hexlify", None, root, "1")

        con1 = hexl.connect("...");
        con2 = root.connect("1");

        con1.write("616263");
        self.assertEqual(con2.read(3), "abc");

        self.assertRaises(Exception, con1.write, "61626")


    def testConnectionCount(self):
        """ MODULE stream_hexlify allows only one child """
        root = self._d_importer.load("stream_reflection",{'timeout':'0.1'})
        hexl = self._d_importer.load("stream_hexlify", None, root, "1")

        con1 = hexl.connect("...");
        self.assertRaises(ItemBusy, hexl.connect, "....")

        del con1;
        con1 = hexl.connect("...");



