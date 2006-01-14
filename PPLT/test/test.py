#!/usr/bin/python
import unittest;
import sys;
import getopt;
from testDCPU import TestDCPUMasterTree;
from testDCPU import TestSymbolTree;
from testDCPU import TestExporter;
from testMods import TestS7;
from testPPLT import TestDevices;
from testMods import TestLockMod;

HELP_TEXT = """
usage: test.py [--help|-h] [--with-S7] [--with-SExp]
 -h --help\t Prints this help message.
 --with-S7\t Enables the Siemens SIMATIC S7-200 module test.
 --with-SExp\t Enables the SimpleExport module test.
 --with-Lock\t Enables the testLock module test.
 --without-MT\t Disables the MasterTree test.
 --without-ST\t Disables the SymbolTree test.
 """;



if __name__ == "__main__":
    # Table of Name -> SuiteObj
    SuiteTable = { "MasterTree":unittest.makeSuite(TestDCPUMasterTree),
                   "SymbolTree":unittest.makeSuite(TestSymbolTree),
                   "SimpleExport":unittest.makeSuite(TestExporter),
                   "Devices":unittest.makeSuite(TestDevices),
                   "S7":unittest.makeSuite(TestS7),
                   "testLock": unittest.makeSuite(TestLockMod)};
    # List of enabled Tests               
    Tests = ["MasterTree", "SymbolTree"];
    
    # Parse options:
    (opts, args) = getopt.getopt(sys.argv[1:], ["h"], ["with-S7","with-SExp","help","without-MT","without-ST","with-Lock"]);

    # check for --help / -h option -> print help, exit
    if (("--help","") in opts) or (("-h","") in opts):
        print HELP_TEXT;
        sys.exit();

    # create test suite:
    suite = unittest.TestSuite();
        
    # extend test list by options:
    if ("--with-S7","") in opts: Tests.append("S7");
    if ("--with-SExp","") in opts: Tests.append("SimpleExport");
    if ("--with-Lock", "") in opts: Tests.append("testLock");
    if ("--without-MT","") in opts: Tests.remove("MasterTree");
    if ("--without-ST","") in opts: Tests.remove("SymbolTree");
    
    # add selected tests to suite:
    for Item in Tests:
        print "Adding Test \"%s\"..."%Item;
        suite.addTest(SuiteTable[Item]);
        
    #RUN IT:    
    unittest.TextTestRunner(verbosity=3).run(suite);

