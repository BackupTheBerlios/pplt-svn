import unittest;
import pyDCPU;

class TestSymbolTree(unittest.TestCase):
    """ Tests the symbol tree """

    def setUp(self):
        self.core = pyDCPU.Core(LogLevel="debug", LogFile="./pyDCPU.log");

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
        self.core.SymbolTreeCreateSymbol("/stream", ID, Address="Stream");
        self.core.SymbolTreeCreateSymbol("/sequence", ID, Address="Sequence");

        #check returned types:
        self.failUnless( isinstance(self.core.SymbolTreeGetValue("/bool"), bool) );
        self.failUnless( isinstance(self.core.SymbolTreeGetValue("/int"), int) );
        self.failUnless( isinstance(self.core.SymbolTreeGetValue("/float"), float) );
        self.failUnless( isinstance(self.core.SymbolTreeGetValue("/string"), str) );
        self.failUnless( isinstance(self.core.SymbolTreeGetValue("/a_bool"), list) );
        self.failUnless( isinstance(self.core.SymbolTreeGetValue("/a_int"), list) );
        self.failUnless( isinstance(self.core.SymbolTreeGetValue("/a_float"), list) );
        tmp = self.core.SymbolTreeRead("/stream",3);
        self.failUnless( isinstance(tmp, str));
        self.failUnless( len(tmp) <= 3);
        self.failUnless( isinstance(self.core.SymbolTreeRead("/sequence"), str) );
        tmp = self.core.SymbolTreeGetValue("/a_bool");
        self.failUnless( isinstance(tmp[0], bool) );
        tmp = self.core.SymbolTreeGetValue("/a_int");
        self.failUnless( isinstance(tmp[0], int) );
        tmp = self.core.SymbolTreeGetValue("/a_float");
        self.failUnless( isinstance(tmp[0], float) );

        #cleanup:
        self.core.SymbolTreeDeleteSymbol("/sequence");
        self.core.SymbolTreeDeleteSymbol("/stream");
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
        self.core.SymbolTreeCreateFolder("/test");
        
        #create symbols:
        self.core.SymbolTreeCreateSymbol("/test/bool", ID, Address="Bool");
        self.core.SymbolTreeCreateSymbol("/test/int", ID, Address="Integer");

        #move a symbol 
        self.core.SymbolTreeMoveSymbol("/test/bool","/test/bool1");
        self.core.SymbolTreeMoveSymbol("/test/bool1","/test/bool");
        
        #move/rename folder
        self.core.SymbolTreeMoveFolder("/test","/test1");
        
        # try to access symbols:
        tmp = self.core.SymbolTreeGetValue("/test1/int");
        self.failUnless( isinstance(tmp, int) );
        tmp = self.core.SymbolTreeGetValue("/test1/bool");
        self.failUnless( isinstance(tmp, bool) );
        
        # try to read renamed symbol:
        self.failUnlessRaises(pyDCPU.Exceptions.ItemNotFound, self.core.SymbolTreeGetValue, Path="/test1/bool1");

        #try to remove not empty folder:
        self.failUnlessRaises(pyDCPU.Exceptions.ItemBusy, self.core.SymbolTreeDeleteFolder, Path="/test1");
        
        #remove symbols and folder
        self.core.SymbolTreeDeleteSymbol("/test1/int");
        self.core.SymbolTreeMoveSymbol("/test1/bool","/bool");
        self.core.SymbolTreeDeleteFolder("/test1");
        
        #try to unload used module:
        self.failUnlessRaises(pyDCPU.Exceptions.ItemBusy, self.core.MasterTreeDel, ID);
        
        self.core.SymbolTreeDeleteSymbol("/bool");
        self.core.MasterTreeDel(ID);


    def testRefCounter(self):
        """ Test reference-counter for symbol-connections """
        ID = self.core.MasterTreeAdd(None, "Master.Debug.Random", None, None);

        self.core.SymbolTreeCreateSymbol("/bool1", ID, Address="Bool");
        self.core.SymbolTreeCreateSymbol("/bool2", ID, Address="Bool");
        self.core.SymbolTreeCreateSymbol("/bool3", ID, Address="Bool");

        self.failUnlessRaises(pyDCPU.Exceptions.ItemBusy, self.core.MasterTreeDel, ObjectID=ID);
        self.core.SymbolTreeDeleteSymbol("/bool1");
        self.failUnlessRaises(pyDCPU.Exceptions.ItemBusy, self.core.MasterTreeDel, ObjectID=ID);
        self.core.SymbolTreeDeleteSymbol("/bool2");
        self.failUnlessRaises(pyDCPU.Exceptions.ItemBusy, self.core.MasterTreeDel, ObjectID=ID);
        self.core.SymbolTreeDeleteSymbol("/bool3");
        self.core.MasterTreeDel(ID); 
