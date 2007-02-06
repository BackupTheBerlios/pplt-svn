import edef
import unittest
import logging
from utils import DummyHandler
import time



class testEventManager(unittest.TestCase):
    
    def testScheduledEvent(self):
        logging.getLogger("edef.core").debug("Start EventManager test")
        evt = edef.EventManager()    # get ref to evt-mangr
        dummy = DummyHandler()

        #FIXME this should not be needed!
        cb = dummy.release
        evt.add_scheduled_event(cb, 0.1, {'value':True} )
        
        self.assertEqual(dummy.wait(1), True)
        evt.clear()
        logging.getLogger("edef.core").debug("End of EventManager test")
        

    def testFinish(self):
        evt = edef.EventManager()
        dummy = DummyHandler()

        #FIXME this should not be needed!
        cb = dummy.release
        evt.add_event(cb, True)

        
        try:
            self.assertEqual(evt.finish(1.0), True)
            self.assertEqual(dummy.wait(0), True)
        finally:
            evt.resume()

    def testPause(self):
        evt = edef.EventManager()
        dummy = DummyHandler()

        #FIXME this should not be needed!
        cb = dummy.release
        
        evt.pause()
        evt.add_event(cb, True)
        try: self.assertEqual(dummy.wait(0.1), None)
        finally: evt.resume()
        
        try:
            self.assertEqual(evt.finish(4.0), True)
            self.assertEqual(dummy.wait(0), True)
        finally:
            evt.resume()
            evt.clear()
