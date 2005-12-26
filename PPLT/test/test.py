#!/usr/bin/python
import unittest;
from testDCPU import TestDCPUMasterTree;
from testDCPU import TestSymbolTree;
from testDCPU import TestExporter;
from testMods import TestS7;
from testPPLT import TestDevices;


if __name__ == "__main__":
    suite = unittest.TestSuite();

    suite.addTest(unittest.makeSuite(TestDCPUMasterTree));
    suite.addTest(unittest.makeSuite(TestSymbolTree));
#    suite.addTest(unittest.makeSuite(TestExporter));
    suite.addTest(unittest.makeSuite(TestS7));   
    suite.addTest(unittest.makeSuite(TestDevices));

    unittest.TextTestRunner(verbosity=3).run(suite);

