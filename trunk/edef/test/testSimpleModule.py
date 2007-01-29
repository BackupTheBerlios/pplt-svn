import unittest
import edef

from utils import DummyHandler


class XOR:
    def __init__(self):
        self.o_out = edef.BoolOutput(False)
        self._d_in_a = False
        self._d_in_b = False
    
    @edef.BoolDecorator
    def i_a(self, value):
        self._d_in_a = value
        if self._d_in_a ^ self._d_in_b:
            self.o_out(True)
        else:
            self.o_out(False)

    @edef.BoolDecorator
    def i_b(self, value):
        self._d_in_b = value
        if self._d_in_a ^ self._d_in_b:
            self.o_out(True)
        else:
            self.o_out(False)



class testSimpleModule(unittest.TestCase):

    def testSingleModule(self):
        mod = XOR()
        dummy = DummyHandler()

        mod.o_out += dummy.release

        self.assertEqual(dummy.wait(0.1), False)

        mod.i_a(True)
        self.assertEqual(dummy.wait(0.1), True)

        mod.i_b(True)
        self.assertEqual(dummy.wait(0.1), False)

        mod.i_a(False)
        self.assertEqual(dummy.wait(0.1), True)

        mod.i_b(False)
        self.assertEqual(dummy.wait(0.1), False)


