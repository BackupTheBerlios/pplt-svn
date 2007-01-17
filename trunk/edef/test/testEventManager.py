import unittest


class testEventManager(unittest.TestCase):

    def setUp(self):
        self.evt = EventManager()
        self._d_state = False
        self._d_ok = False

    def tearDown(self):
        self.evt.stop()


    def testEventOrder(self):
        

    def _cb_1(self):
        
