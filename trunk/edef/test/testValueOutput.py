import unittest
import edef
import threading

from utils import DummyHandler


class testValueOutput(unittest.TestCase):

    def testEventOnConnect(self):
        out = edef.ValueOutput(True)
        dummy = DummyHandler()
        
        out += dummy.release

        self.assertEqual(dummy.wait(), True)


    def testEventOrder(self):
        out = edef.ValueOutput(False)
        
        dummy = DummyHandler()
        out += dummy.release

        self.assertEqual(dummy.wait(), False)
        out(True)
        out(False)
        self.assertEqual(dummy.wait(), True)
        self.assertEqual(dummy.wait(), False)

            
