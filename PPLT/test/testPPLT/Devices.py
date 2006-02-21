import PPLT;
import unittest;

class TestDevices(unittest.TestCase):
    def setUp(self):
        self.sys = PPLT.System(CoreLogLevel="debug", PPLTLogLevel="debug", LogFile="./PPLT.log");
    
    def tearDown(self):
        self.sys.StopAll();
        del self.sys;
        self.sys = None;

    def testRandom(self):
        """ Test loading and stopping of random device """
        self.sys.LoadDevice("Debug.RandomGenerator", "rand", None);
        self.sys.UnLoadDevice("rand");
        
    def testDeviceLock(self):
        """ Test device locking """
        self.sys.LoadDevice("Debug.RandomGenerator", "rand", None);
        
        self.sys.CreateSymbol("/bool", "rand::Generator::Bool");

        self.failUnlessRaises(PPLT.ItemBusy, self.sys.UnLoadDevice,
                              Alias="rand");

        self.sys.DeleteSymbol("/bool");
        self.sys.UnLoadDevice("rand");

    def testDeviceLockII(self):
        """ Test more complex device locking """
        self.sys.LoadDevice("PLC.S7-200", "s7", {'Port':'0'});

        self.sys.CreateSymbol("/smb28", "s7::Marker::SMB28");
        self.sys.CreateSymbol("/ppi-rd", "s7::PPIStatistic::read_data");

        self.failUnlessRaises(PPLT.ItemBusy, self.sys.UnLoadDevice,
                              Alias="s7");

        self.sys.DeleteSymbol("/smb28");

        self.failUnlessRaises(PPLT.ItemBusy, self.sys.UnLoadDevice,
                              Alias="s7");

        self.sys.DeleteSymbol("/ppi-rd");
        self.sys.UnLoadDevice("s7");
