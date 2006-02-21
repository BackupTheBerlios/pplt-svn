import pyDCPU;
import unittest;

class TestDCPUMasterTree(unittest.TestCase):
    """ Test the mastertree of the pyDCPU-Core class """

    def setUp(self):
        self.core = pyDCPU.Core(LogLevel="debug", LogFile="./pyDCPU.log");

    def tearDown(self):
        del self.core;
        self.core = None;

    def test01LoadAndRemoveModule(self):
        """ Test the basic master-tree functionality """
        # Try to load an existing module:
        ID1 = self.core.MasterTreeAdd(None, "Master.Debug.Random", None, None);
        self.failUnless(isinstance(ID1, (str, unicode) ), "Wrong type of return code");
        
        # try to load a not existing module and check type of raised exception:
        self.failUnlessRaises(pyDCPU.Exceptions.ItemNotFound, self.core.MasterTreeAdd,
                              ParentID=None, ModName="Master.NotKnown", Address=None, Parameter=None);

        # try to remove a not existing object and check type of raised exception:
        self.failUnlessRaises(pyDCPU.Exceptions.ItemNotFound, self.core.MasterTreeDel, ObjectID="");

        # try to create a symbol:
        self.core.SymbolTreeCreateSymbol("/test",ID1, Address="Bool");

        # try to remove busy object;
        self.failUnlessRaises(pyDCPU.Exceptions.ItemBusy, self.core.MasterTreeDel, ObjectID=ID1);
        
        # try to remove symbol:
        self.core.SymbolTreeDeleteSymbol("/test");

        #try to remove loaded module:
        self.core.MasterTreeDel(ID1);


    def test01ReferenceCounter(self):
        """ Test reference-counters """

        # Try to load one module often:
        ID1 = self.core.MasterTreeAdd(None, "Master.Debug.Random", None, None);
        ID  = self.core.MasterTreeAdd(None, "Master.Debug.Random", None, None);
        self.assertEqual(ID1,ID);
        ID  = self.core.MasterTreeAdd(None, "Master.Debug.Random", None, None);
        self.assertEqual(ID1,ID);
        ID  = self.core.MasterTreeAdd(None, "Master.Debug.Random", None, None);
        self.assertEqual(ID1,ID);
        ID  = self.core.MasterTreeAdd(None, "Master.Debug.Random", None, None);
        self.assertEqual(ID1,ID);
       
        self.core.MasterTreeDel(ID);
        self.core.MasterTreeDel(ID);
        self.core.MasterTreeDel(ID);
        self.core.MasterTreeDel(ID);
        self.core.MasterTreeDel(ID);

        self.failUnlessRaises(pyDCPU.Exceptions.ItemNotFound, self.core.MasterTreeDel,ObjectID = ID);


    def test03ItemLocking(self):
        """ Test item-locking (remove lock)"""

        ID = self.core.MasterTreeAdd(None, "Master.Debug.Random", None, None);
        self.core.SymbolTreeCreateSymbol("/test01", ID, Address="Bool");
        self.core.SymbolTreeCreateSymbol("/test02", ID, Address="Bool");
        
        # try to overwrite an existing symbol
        self.failUnlessRaises(pyDCPU.Exceptions.Error, self.core.SymbolTreeCreateSymbol, Path="/test01", ObjectID=ID, Address="Bool");
       
        # check if used module is removeable.
        self.failUnlessRaises(pyDCPU.Exceptions.ItemBusy, self.core.MasterTreeDel, ObjectID=ID);
        self.core.SymbolTreeDeleteSymbol("/test02");
        self.failUnlessRaises(pyDCPU.Exceptions.ItemBusy, self.core.MasterTreeDel, ObjectID=ID);
        self.core.SymbolTreeDeleteSymbol("/test01");
        self.core.MasterTreeDel(ID);


    def test04ItemLockOnFail(self):
        """ Test usagecounter on faild loading """
        ID1 = self.core.MasterTreeAdd(None, "Master.Interface.UniSerial", None,
                                      {'Port':'0', 'Speed':'9600'});
        
        # this now will fail:
        self.failUnlessRaises(pyDCPU.ModuleRequirement, self.core.MasterTreeAdd,
                              ParentID=ID1, ModName="Master.Transport.PPI",
                              Address=None, Parameter={});

        #unload serial-interface:
        self.core.MasterTreeDel(ID1);

