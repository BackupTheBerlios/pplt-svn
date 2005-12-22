import unittest;
import pyDCPU;

class TestSymbolTree(unittest.TestCase):
    """ Tests the symbol tree """

    def setUp(self):
        self.core = pyDCPU.Core("/usr/PPLT/", LogFile="./pyDCPU.log");

    def tearDown(self):
        del self.core;
        self.core = None;
    
    def testTypes(self):
        """ Test symbol types """
        # load random-module:
        ID = self.core.MasterTreeAdd(None, "Master.Debug.Random", None, None);
        self.failUnless(isinstance(ID, (str, unicode)));

        #create some symbols:
        self.core.SymbolTreeCreateSymbol("/bool", ID, Address="Bool");
        self.core.SymbolTreeCreateSymbol("/int", ID, Address="Integer");
        self.core.SymbolTreeCreateSymbol("/float", ID, Address="Float");
        self.core.SymbolTreeCreateSymbol("/string", ID, Address="String");
        self.core.SymbolTreeCreateSymbol("/a_bool", ID, Address="ArrayBool");
        self.core.SymbolTreeCreateSymbol("/a_int", ID, Address="ArrayInteger");
        self.core.SymbolTreeCreateSymbol("/a_float", ID, Address="ArrayFloat");
        
        #check returned types:
        self.failUnless( isinstance(self.core.SymbolTreeGetValue("/bool"), bool) );
        self.failUnless( isinstance(self.core.SymbolTreeGetValue("/int"), int) );
        self.failUnless( isinstance(self.core.SymbolTreeGetValue("/float"), float) );
        self.failUnless( isinstance(self.core.SymbolTreeGetValue("/string"), str) );
        self.failUnless( isinstance(self.core.SymbolTreeGetValue("/a_bool"), list) );
        self.failUnless( isinstance(self.core.SymbolTreeGetValue("/a_int"), list) );
        self.failUnless( isinstance(self.core.SymbolTreeGetValue("/a_float"), list) );
        tmp = self.core.SymbolTreeGetValue("/a_bool");
        self.failUnless( isinstance(tmp[0], bool) );
        tmp = self.core.SymbolTreeGetValue("/a_int");
        self.failUnless( isinstance(tmp[0], int) );
        tmp = self.core.SymbolTreeGetValue("/a_float");
        self.failUnless( isinstance(tmp[0], float) );

        #cleanup:
        self.core.SymbolTreeDeleteSymbol("/a_float");
        self.core.SymbolTreeDeleteSymbol("/a_int");
        self.core.SymbolTreeDeleteSymbol("/a_bool");
        self.core.SymbolTreeDeleteSymbol("/string");
        self.core.SymbolTreeDeleteSymbol("/float");
        self.core.SymbolTreeDeleteSymbol("/int");
        self.core.SymbolTreeDeleteSymbol("/bool");
        self.core.MasterTreeDel(ID);


    def testConnection(self):
        """ Test connection to objects """
        ID = self.core.MasterTreeAdd(None, "Master.Debug.Random", None, None);
        
        # create connection directly to object
        con = self.core.GetAConnection(ID, "Bool");
        self.failUnless( isinstance(con, pyDCPU.ValueConnection), "Need \"ValueConnection\" got: %s"%str(con) );
        
        # read a value:
        tmp = con.read_seq();
        self.failUnless( isinstance(tmp, bool) );
    
        # test remove busy object:
        self.failUnlessRaises( pyDCPU.Exceptions.ItemBusy, self.core.MasterTreeDel, ObjectID = ID);
        
        #close:
        con.close();
        self.core.MasterTreeDel(ID);

        
    def testMoveRename(self):
        """ Test rename and moveing symbols/folders """
        ID = self.core.MasterTreeAdd(None, "Master.Debug.Random", None, None); 
        
        #create folder:
        self.core.SymbolTreeCreateFolder("/test1");
        
        #create symbols:
        self.core.SymbolTreeCreateSymbol("/test1/bool", ID, Address="Bool");
        self.core.SymbolTreeCreateSymbol("/test1/int", ID, Address="Integer");

        #move a symbol 
        self.core.SymbolTreeMoveSymbol("/test1/bool","/test1/bool1");
        self.core.SymbolTreeMoveSymbol("/test1/bool1","/bool");
        
        #move/rename folder
        self.core.SymbolTreeMoveFolder("/test1","/test");
        
        # try to access symbols:
        tmp = self.core.SymbolTreeGetValue("/test/int");
        self.failUnless( isinstance(tmp, int) );
        tmp = self.core.SymbolTreeGetValue("/bool");
        self.failUnless( isinstance(tmp, bool) );
        
        #try to remove not empty folder:
        self.failUnlessRaises(pyDCPU.Exceptions.ItemBusy, self.core.SymbolTreeDeleteFolder, Path="/test");
        
        #remove symbols and folder
        self.core.SymbolTreeDeleteSymbol("/test/int");
        self.core.SymbolTreeDeleteFolder("/test");
        
        #try to unload used module:
        self.failUnlessRaises(pyDCPU.Exceptions.ItemBusy, self.core.MasterTreeDel, ID);

        self.core.SymbolTreeDeleteSymbol("/bool");
        self.core.MasterTreeDel(ID);

        
