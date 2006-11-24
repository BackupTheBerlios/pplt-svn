import unittest;
from core import CImporter, ItemBusy;


class testStreamDumpModule( unittest.TestCase ):

    def setUp(self):
        self._d_importer = CImporter("../modules");
        self._d_root     = self._d_importer.load("stream_reflection",{'timeout':'1'})



    def testConnectionCount(self):
        """ MODULE stream_dump connection count """
        dump = self._d_importer.load("stream_dump", None, self._d_root, "1")

        con1 = dump.connect()
        self.assertRaises(ItemBusy, dump.connect)

        r_con = dump.connect("read")
        self.assertRaises(ItemBusy, dump.connect, "read")

        w_con = dump.connect("write")
        self.assertRaises(ItemBusy, dump.connect, "write")

        e_con = dump.connect("event")
        self.assertRaises(ItemBusy, dump.connect, "event")

        del e_con
        e_con = dump.connect("event")

        del e_con
        del w_con
        del r_con

        self.assertEqual(dump.is_busy(), True)

        del dump


    def testRead(self):
        """ MODULE stream_dump test read-channel """
        dump = self._d_importer.load("stream_dump", None, self._d_root, "1")

        con1 = self._d_root.connect("1")
        rcon = dump.connect("read")

        con1.write("abc")
        
        con2 = dump.connect()
        
        self.assertEqual(con2.read(3), "abc")
        self.assertEqual(rcon.read(3), "abc")


    def testEvent(self):
        """ MODULE stream_dump test event-channel """
        dump = self._d_importer.load("stream_dump", None, self._d_root, "1")

        con1 = self._d_root.connect("1")
        con2 = dump.connect()
        econ = dump.connect("event")

        con1.write("abc")
        self.assertEqual(con2.read(3), "abc")
        self.assertEqual(econ.read(3), "abc")


    def testWrite(self):
        """ MODULE stream_dump test write-channel """
        dump = self._d_importer.load("stream_dump", None, self._d_root, "1")

        con1 = self._d_root.connect("1")
        con2 = dump.connect()
        wcon = dump.connect("write")

        con2.write("abc")
        self.assertEqual(con1.read(3), "abc")
        self.assertEqual(wcon.read(3), "abc")
