import unittest;
import pyDCPU;

class TestS7(unittest.TestCase):
    """ Testes the modules for the SIMATIC S7 """

    def setUp(self):
        self.core = pyDCPU.Core(LogLevel="debug", LogFile="./pyDCPU.log");

    def tearDown(self):
        del self.core;
        self.core = None;
        
    
    def testLoadModules(self):
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

        
