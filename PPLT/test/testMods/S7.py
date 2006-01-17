import unittest;
import pyDCPU;

class TestS7(unittest.TestCase):
    """ Testes the modules for the SIMATIC S7 """

    def setUp(self):
        self.core = pyDCPU.Core(LogLevel="debug", LogFile="./pyDCPU.log");

    def tearDown(self):
        del self.core;
        self.core = None;
        
    
    def test01LoadModules(self):
        """ Test S7: Try to load all needed modules """
        #load serial
        ser_id = self.core.MasterTreeAdd(None, "Master.Interface.UniSerial", None, {"Port":"0", "Speed":"9600", "TimeOut":"0.5", "Parity":"Even"});
        self.failUnless( isinstance(ser_id, str) );

        #load ppi-module:
        ppi_id = self.core.MasterTreeAdd(ser_id, "Master.Transport.PPI", None, {"Address":"0"});
        self.failUnless( isinstance(ppi_id, str) );

        #load S7-module:
        s7_id = self.core.MasterTreeAdd(ppi_id, "Master.Device.S7", "2", None);
        self.failUnless( isinstance(s7_id, str) );

        #unload all:
        self.core.MasterTreeDel(s7_id);
        self.core.MasterTreeDel(ppi_id);
        self.core.MasterTreeDel(ser_id);

    
    def test02AccessSM05(self):
        """ Test S7: Try to access Marker AB0 """
        ser_id = self.core.MasterTreeAdd(None, "Master.Interface.UniSerial", None, {"Port":"0", "Speed":"9600", "TimeOut":"1", "Parity":"Even"});
        self.failUnless( isinstance(ser_id, str) );

        #load ppi-module:
        ppi_id = self.core.MasterTreeAdd(ser_id, "Master.Transport.PPI", None, {"Address":"0"});
        self.failUnless( isinstance(ppi_id, str) );

        #load S7-module:
        s7_id = self.core.MasterTreeAdd(ppi_id, "Master.Device.S7", "2", None);
        self.failUnless( isinstance(s7_id, str) );

        #create symbol:
        self.core.SymbolTreeCreateSymbol("/AB0", s7_id, Address="AB0"); 

        #read symbol and test type
        tmp = self.core.SymbolTreeGetValue("/AB0");
        self.failUnless( isinstance(tmp, int) );
        
        # rewrite value+1
        self.core.SymbolTreeSetValue("/AB0", tmp+1);
        #delete symbol:
        self.core.SymbolTreeDeleteSymbol("/AB0");

        #unload all:
        self.core.MasterTreeDel(s7_id);
        self.core.MasterTreeDel(ppi_id);
        self.core.MasterTreeDel(ser_id);

    def test03TestTypes(self):
        """ Test S7: Try to get diff types A0.0, AB0, SMW0, SMD0 """
        ser_id = self.core.MasterTreeAdd(None, "Master.Interface.UniSerial", None, {"Port":"0", "Speed":"9600", "TimeOut":"1", "Parity":"Even"});
        self.failUnless( isinstance(ser_id, str) );

        #load ppi-module:
        ppi_id = self.core.MasterTreeAdd(ser_id, "Master.Transport.PPI", None, {"Address":"0"});
        self.failUnless( isinstance(ppi_id, str) );

        #load S7-module:
        s7_id = self.core.MasterTreeAdd(ppi_id, "Master.Device.S7", "2", None);
        self.failUnless( isinstance(s7_id, str) );
 
        self.core.SymbolTreeCreateSymbol("/bit", s7_id, Address="A0.0");
        self.core.SymbolTreeCreateSymbol("/byte", s7_id, Address="AB0");
        self.core.SymbolTreeCreateSymbol("/word", s7_id, Address="SMW0");
        self.core.SymbolTreeCreateSymbol("/dword", s7_id, Address="SMD0");

        tmp = self.core.SymbolTreeGetValue("/bit");
        self.failUnless( isinstance(tmp, bool) );
        tmp = self.core.SymbolTreeGetValue("/byte");
        self.failUnless( isinstance(tmp, int) );
        tmp = self.core.SymbolTreeGetValue("/word");
        self.failUnless( isinstance(tmp, int) );
        tmp = self.core.SymbolTreeGetValue("/dword");
        self.failUnless( isinstance(tmp, int) );

        self.SymbolTreeDeleteSymbol("/bit");
        self.SymbolTreeDeleteSymbol("/byte");
        self.SymbolTreeDeleteSymbol("/word");
        self.SymbolTreeDeleteSymbol("/dword");

        self.core.MasterTreeDel(s7_id);
        self.core.MasterTreeDel(ppi_id);
        self.core.MasterTreeDel(ser_id);
      

