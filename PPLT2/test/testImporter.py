import unittest;
from core import CImporter;


class testImporter(unittest.TestCase):
    _d_importer = None;

    def setUp(self):
        self._d_importer = CImporter("test_modules");


    def testModuleFinding(self):
        (path, meta) = self._d_importer.getModuleMeta("reflection");

        self.assertRaises(Exception, self._d_importer.getModuleMeta, "DoNotEx");
        
    def testModuleLoading(self):
        self._d_importer.load("reflection");

