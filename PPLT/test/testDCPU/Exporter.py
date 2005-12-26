import pyDCPU;
import unittest;
import xmlrpclib;

class TestExporter(unittest.TestCase):
    """ Tests the exporters """

    def setUp(self):
        self.core = pyDCPU.Core(LogLevel="debug", LogFile="./pyDCPU.log");
        self.ExpID = self.core.ExporterAdd("Export.SimpleExport", {"Address":"127.0.0.1", "Port":"4711"}, "admin");

    def tearDown(self):
        self.core.ExporterDel(self.ExpID);
        del self.core;
        self.core = None;

        

    def testExpAccessAndDataTypes(self):
        """ Test the access to exporter and the returned data-types """
        # load modules
        MID = self.core.MasterTreeAdd(None, "Master.Debug.Random", None, None);

        # create symbols:
        self.core.SymbolTreeCreateSymbol("/bool", MID, Address="Bool");
        self.core.SymbolTreeCreateSymbol("/int", MID, Address="Integer");
        self.core.SymbolTreeCreateSymbol("/float", MID, Address="Float");
        self.core.SymbolTreeCreateSymbol("/str", MID, Address="String");
        self.core.SymbolTreeCreateSymbol("/a_bool", MID, Address="ArrayBool");
        self.core.SymbolTreeCreateSymbol("/a_int", MID, Address="ArrayInteger");
        self.core.SymbolTreeCreateSymbol("/a_float", MID, Address="ArrayFloat");

        # create connection to server:
        srv = xmlrpclib.ServerProxy("http://127.0.0.1:4711");
        self.failUnless( isinstance(srv.get("/bool"), bool) );
        self.failUnless( isinstance(srv.get("/int"), int) );
        self.failUnless( isinstance(srv.get("/float"), float) );
        tmp = srv.get("/a_bool");
        self.failUnless( isinstance(tmp, list) );
        self.failUnless( isinstance(tmp[0], bool) );
        tmp = srv.get("/a_int");
        self.failUnless( isinstance(tmp, list) );
        self.failUnless( isinstance(tmp[0], int) );
        tmp = srv.get("/a_float");
        self.failUnless( isinstance(tmp, list) );
        self.failUnless( isinstance(tmp[0], float) );
        
        
