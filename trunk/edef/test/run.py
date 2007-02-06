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
    log_file = open("test.log","a")
    edef.Logger(logging.DEBUG, log_file)

    # init/start EventManager:
    evt = edef.EventManager()
    evt.resume()

    # create suite:
    suite = unittest.TestSuite()
    
    # add tests
    suite.addTest(testSingleton("testSingle"))

    suite.addTest(testValueOutput("testEventOnConnect"))
    suite.addTest(testValueOutput("testEventOrder"))

    suite.addTest(testEventManager("testScheduledEvent"))
    suite.addTest(testEventManager("testFinish"))
    suite.addTest(testEventManager("testPause"))

    suite.addTest(testSimpleModule("testSingleModule"))
    
    suite.addTest(testDecorators("testArguments"))
    suite.addTest(testDecorators("testType"))
   
    suite.addTest(testAssembly("testInitAssembly"))

    # run tests
    try:
        unittest.TextTestRunner(verbosity=2).run(suite)
    finally:
        evt.finish()
        evt.shutdown()
