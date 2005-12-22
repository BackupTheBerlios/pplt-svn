#!/usr/bin/python
import unittest;
from testDCPU import TestDCPUMasterTree;
from testDCPU import TestSymbolTree;

if __name__ == "__main__":
    suite = unittest.TestSuite();
    suite.addTest(unittest.makeSuite(TestDCPUMasterTree));
    suite.addTest(unittest.makeSuite(TestSymbolTree));
    unittest.TextTestRunner(verbosity=3).run(suite);

