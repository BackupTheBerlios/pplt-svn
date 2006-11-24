

import unittest
from core import CImporter


class testSequenceReflectionModule(unittest.TestCase):

    def setUp(self):
        self._d_importer = CImporter("../modules")


    def testSimpleIO(self):
        """ MODULE sequence_reflection simple io """
        ref = self._d_importer.load("sequence_reflection",{'timeout':'0.1'})

        con1 = ref.connect("1")
        con2 = ref.connect("1")

        con1.send("abc")
        self.assertEqual(con2.recv(), "abc")

        con2.send("abc")
        self.assertEqual(con1.recv(), "abc")

        con1.send("abc")
        con1.send("def")
        self.assertEqual(con2.recv(), "abc")
        con2.send("abc")
        self.assertEqual(con1.recv(), "abc")
        self.assertEqual(con2.recv(), "def")

