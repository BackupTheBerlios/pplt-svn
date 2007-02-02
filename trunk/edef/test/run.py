#!/usr/bin/python


import logging
import unittest
import edef
import time

# import Tests:
from testValueOutput import testValueOutput
from testEventManager import testEventManager
from testSimpleModule import testSimpleModule
from testDecorators import testDecorators
from testAssembly import testAssembly
from testSingleton import testSingleton



if __name__ == '__main__':
    print ""
    # init logger
    log_file = open("test.log","w")
    edef.Logger(logging.DEBUG, log_file)

    # create suite:
    suite = unittest.TestSuite()
    
    # add tests
    suite.addTest(testSingleton("testSingle"))

    suite.addTest(testValueOutput("testEventOnConnect"))
    suite.addTest(testValueOutput("testEventOrder"))

    suite.addTest(testEventManager("testScheduledEvent"))

    suite.addTest(testSimpleModule("testSingleModule"))
    
    suite.addTest(testDecorators("testArguments"))
    suite.addTest(testDecorators("testType"))
   
    suite.addTest(testAssembly("testInitAssembly"))

    # run tests
    try:
        unittest.TextTestRunner(verbosity=2).run(suite)
    finally:
        # stop Eventhandler
        time.sleep(0.1)
        edef.EventManager().stop()
