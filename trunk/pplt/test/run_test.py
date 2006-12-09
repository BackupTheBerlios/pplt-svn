#!/usr/bin/python
# ########################################################################## #
# run_test.py
#
# 2006-09-01
# Copyright 2006 Hannes Matuschek
# hmatuschek@gmx.net
# ########################################################################## #
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# ########################################################################## #

import logging
import unittest
from testModuleMeta import testModuleMeta
from testAssemblyMeta import testAssemblyMeta
from testStreamConnection import testStreamConnection
from testConnection import testConnection
from testSequenceConnection import testSequenceConnection
from testAsyncStreamConnection import testAsyncStreamConnection
from testImporter import testImporter
from testInnerModule import testInnerModule
from testStreamHexlifyModule import testStreamHexlifyModule
from testStreamDumpModule import testStreamDumpModule
from testSequenceReflectionModule import testSequenceReflectionModule
from testCoreModuleMeta import testCoreModuleMeta
from testRandomModule import testRandomModule



if __name__ == "__main__":
    #config logging:
    con = logging.FileHandler("test.log")
    con.setFormatter(logging.Formatter("%(levelname)-8s %(filename)s:%(lineno)d %(message)s"))
    logging.getLogger("PPLT").addHandler(con)
    logging.getLogger("PPLT").setLevel(logging.DEBUG)

    print ""
    print "-" * 70

    #create suite:
    suite = unittest.TestSuite()
   
    suite.addTest(testModuleMeta("testParameterExpand"))
    suite.addTest(testModuleMeta("testCheckParameters"))
    suite.addTest(testModuleMeta("testMetadata"))
    suite.addTest(testModuleMeta("testInterface"))

    suite.addTest(testCoreModuleMeta("testGrammarVersion"))
    suite.addTest(testCoreModuleMeta("testDependencies"))

    suite.addTest(testAssemblyMeta("testGrammarVersion"))
    suite.addTest(testAssemblyMeta("testDependencies"))
    suite.addTest(testAssemblyMeta("testLoad"))
    suite.addTest(testAssemblyMeta("testCmplxLoad"))
    suite.addTest(testAssemblyMeta("testInnerLoad"))

    suite.addTest(testImporter("testModuleFinding"))
    suite.addTest(testImporter("testModuleLoading"))
    suite.addTest(testImporter("testInnerModuleLoading"))
    suite.addTest(testImporter("testAssemblyLoading"))

    suite.addTest(testInnerModule("testConCloseAtModDestroy"))
    suite.addTest(testInnerModule("testSimpleInnerModule"))
    suite.addTest(testInnerModule("testSimpleDisposableModule"))

    suite.addTest(testConnection("testConnectionClose"))

    suite.addTest(testSequenceConnection("testEventThread"))
    suite.addTest(testSequenceConnection("testConnectionClose"))
    suite.addTest(testSequenceConnection("testStreamInterface"))

    suite.addTest(testStreamConnection("testEventStatus"))
    suite.addTest(testStreamConnection("testEventThread"))
    
    suite.addTest(testAsyncStreamConnection("testConnectionCount"))
    suite.addTest(testAsyncStreamConnection("testTimeout"))
    suite.addTest(testAsyncStreamConnection("testDataIntegrity"))

    suite.addTest(testSequenceReflectionModule("testSimpleIO"))

    suite.addTest(testStreamHexlifyModule("testHexlify"));
    suite.addTest(testStreamHexlifyModule("testUnhexlify"))
    suite.addTest(testStreamHexlifyModule("testConnectionCount"))
    
    suite.addTest(testStreamDumpModule("testConnectionCount"))
    suite.addTest(testStreamDumpModule("testRead"))
    suite.addTest(testStreamDumpModule("testWrite"))
    suite.addTest(testStreamDumpModule("testEvent"))
    
    suite.addTest(testRandomModule("testModule"))
    suite.addTest(testRandomModule("testParamConnection"))
    suite.addTest(testRandomModule("testEventGeneration"))

    unittest.TextTestRunner(verbosity=2).run(suite)



