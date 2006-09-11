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

import logging;
import unittest;
from testStreamConnection import testStreamConnection;
from testConnection import testConnection;
from testAsyncStreamConnection import testAsyncStreamConnection;

if __name__ == "__main__":
    #config logging:
    con = logging.FileHandler("test.log");
    con.setFormatter(logging.Formatter("%(levelname)-8s %(message)s"));
    logging.getLogger("PPLT").addHandler(con);
    logging.getLogger("PPLT").setLevel(logging.DEBUG);

    print "";
    print "-"*70;

    #create suite:
    suite = unittest.TestSuite();
    
    suite.addTest(testConnection("testConnectionClose"));
    
    suite.addTest(testStreamConnection("testPushParameterConstance"));
    suite.addTest(testStreamConnection("testEventStatus"));
    suite.addTest(testStreamConnection("testEventThread"));
    
    suite.addTest(testAsyncStreamConnection("testConnectionCount"));
    suite.addTest(testAsyncStreamConnection("testTimeout"));
    suite.addTest(testAsyncStreamConnection("testDataIntegrity"));

    unittest.TextTestRunner(verbosity=2).run(suite);



