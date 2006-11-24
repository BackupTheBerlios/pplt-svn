import unittest;
from core import CImporter;


class testImporter(unittest.TestCase):
    _d_importer = None;


    def setUp(self):
        self._d_importer = CImporter("../modules");



    def testModuleFinding(self):
        """ CLASS CImporter module finding """
        (path, meta) = self._d_importer.getModuleMeta("stream_reflection");

        self.assertRaises(Exception, self._d_importer.getModuleMeta, "DoNotEx");
       


    def testModuleLoading(self):
        """ CLASS CImporter module loading """
        self._d_importer.load("stream_reflection");


    def testInnerModuleLoading(self):
        """ CLASS CImporter inner-module loading """
        root = self._d_importer.load("stream_reflection")
        self._d_importer.load("stream_hexlify", None, root, "1")
