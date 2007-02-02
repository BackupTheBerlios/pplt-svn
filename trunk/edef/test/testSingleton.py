import unittest
from edef import Singleton


class A:
    __metaclass__ = Singleton
class B:
    __metaclass__ = Singleton
    

class testSingleton(unittest.TestCase):

    def testSingle(self):
       ia1 = A()
       ia2 = A()
       self.assertEqual(id(ia1), id(ia2))
