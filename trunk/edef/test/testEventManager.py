import edef
import unittest
import logging
from utils import DummyHandler

class testEventManager(unittest.TestCase):
    
    def testScheduledEvent(self):
        logging.getLogger("edef.test").debug("Start EventManager test")
        evt = edef.EventManager()    # get ref to evt-mangr
        dummy = DummyHandler()
        
        try:
            evt.add_scheduled_event(dummy.release, 0.1, {'value':True} )
            self.assertEqual(dummy.wait(20), True)
        finally:
            logging.getLogger("edef.test").debug("End of EventManager test")



