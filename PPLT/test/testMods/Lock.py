import unittest;
import pyDCPU;
import time;

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


    def test02ItemLocking(self):
        """ Test item-locking (access lock) """

        rand_id = self.core.MasterTreeAdd(None, "Master.Debug.Random", None, None);
        lock_id = self.core.MasterTreeAdd(rand_id, "Master.Debug.testLock", "Bool", None);

        self.core.SymbolTreeCreateSymbol("/test", lock_id);

        tmp = self.core.SymbolTreeGetValue("/test");
        self.failUnless( isinstance(tmp, bool) );

#        self.failUnlessRaises( pyDCPU.Exceptions.ItemBusy, self.core.SymbolTreeGetValue, Path="/test");
        self.core.SymbolTreeGetValue("/test");
        print "Wait for item-release: ";
        time.sleep(6);
        
        tmp = self.core.SymbolTreeGetValue("/test");
        self.failUnless( isinstance(tmp, bool) );
      
        self.core.SymbolTreeDeleteSymbol("/test");
        self.core.MasterTreeDel(lock_id);
        self.core.MasterTreeDel(rand_id);

 
