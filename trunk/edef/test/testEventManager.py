import edef
import unittest
import logging
from utils import DummyHandler

class testEventManager(unittest.TestCase):
    
    def testScheduledEvent(self):
        logging.getLogger("edef.core").debug("Start EventManager test")
        evt = edef.EventManager()    # get ref to evt-mangr
        dummy = DummyHandler()
        cb = dummy.release
        evt.add_scheduled_event(cb, 0.1, {'value':True} )
        
        #evt.finish(10)
       
        self.assertEqual(dummy.wait(1), True)
      
        logging.getLogger("edef.core").debug("End of EventManager test")



