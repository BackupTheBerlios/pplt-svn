import unittest;
import pyDCPU;

class TestLockMod(unittest.TestCase):
    """ Testes the \"testLock\" module """

    def setUp(self):
        self.core = pyDCPU.Core(LogLevel="debug", LogFile="./pyDCPU.log");

    def tearDown(self):
        del self.core;
        self.core = None;

    
    def test01LoadModule(self):
        """ Test testLock: Try to load modules """
        #load Random:
        rand_id = self.core.MasterTreeAdd(None, "Master.Debug.Random",None, None);
        self.failUnless( isinstance(rand_id, str) );

        #load lock-mod:
        lock_id = self.core.MasterTreeAdd(rand_id, "Master.Debug.testLock", "Bool", None);
        self.failUnless( isinstance(lock_id, str) );

        self.core.MasterTreeDel(lock_id);
        self.core.MasterTreeDel(rand_id);

