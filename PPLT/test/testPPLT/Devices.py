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
        

