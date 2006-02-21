import PPLT;
import unittest;

class TestSymbols(unittest.TestCase):
    def setUp(self):
        self.sys = PPLT.System(CoreLogLevel="debug", PPLTLogLevel="debug", LogFile="./PPLT.log");
    
    def tearDown(self):
        self.sys.StopAll();
        del self.sys;
        self.sys = None;

    def test01SymbolTypes(self):
        """ Test symboltypes with Random-Generator. """
        self.sys.LoadDevice("Debug.RandomGenerator", "rand", None);

        #create some symbols:
        self.sys.CreateSymbol("/bool", "rand::Generator::Bool");
        self.sys.CreateSymbol("/int", "rand::Generator::Integer");
        self.sys.CreateSymbol("/float", "rand::Generator::Float");
        self.sys.CreateSymbol("/str", "rand::Generator::String");

        self.failUnless( isinstance(self.sys.GetValue("/bool"), bool) );
        self.failUnless( isinstance(self.sys.GetValue("/int"), int) );
        self.failUnless( isinstance(self.sys.GetValue("/float"), float) );
        self.failUnless( isinstance(self.sys.GetValue("/str"), str) );

        self.sys.DeleteSymbol("/float");
        self.sys.DeleteSymbol("/str");
        self.sys.DeleteSymbol("/int");
        self.sys.DeleteSymbol("/bool");
        self.sys.UnLoadDevice("rand");

    def test02SymbolAccess(self):
        """ Test exception for wrong symbol access! """
        self.sys.LoadDevice("Debug.RandomGenerator", "rand", None);
        
        self.sys.CreateSymbol("/bool", "rand::Generator::Bool");
        
        self.failUnlessRaises(PPLT.AccessDenied, self.sys.SetValue,
                              Path="/bool", Value=True);
        
        self.sys.DeleteSymbol("/bool");
