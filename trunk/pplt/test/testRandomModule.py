

import unittest
from pplt import CImporter

class testRandomModule (unittest.TestCase):
    def setUp(self):
        self.imp = CImporter("../modules")


    def testModule(self):
        rand = self.imp.load("random_module")

        con1 = rand.connect("integer")
        con2 = rand.connect("bool")
        con3 = rand.connect("float")

        con1.get()
        con2.get()
        con3.get()



    def testParamConnection(self):
        rand = self.imp.load("random_module")

        con1 = rand.connect("period")
        con2 = rand.connect("variance")

        self.assertEqual(con1.get(), 0)
        self.assertEqual(con2.get(), 0)

        con1.set(2.0)
        con2.set(0.5)
        self.assertEqual(con1.get(), 2)
        self.assertEqual(con2.get(), 0.5)


    def testEventGeneration(self):
        raise NotImplemented  #("This test have to be written...")
