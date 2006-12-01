import unittest
from pplt import CModuleMeta, ModuleImportError
import xml.dom.minidom

class testModuleMeta(unittest.TestCase):
    _d_test_doc1 = """<?xml version="1.0"?>

        <Module version="1.0">
            <Version>0.0.1a</Version>
            <Author>Hannes Matuschek &lt;hmatuschek@gmx.net&gt;</Author>

            <Require>
                <Parameter name="param1" default="abc"/>
                <Parameter name="param2"/>
            </Require>
        </Module>"""

    _s_meta = None

    
    def setUp(self):
        self._d_meta = CModuleMeta(xml.dom.minidom.parseString(self._d_test_doc1).documentElement)

    
    def testParameterExpand(self):
        """ CLASS CModuleMeta parameter expansion """
        
        params = {"param2":"..."};
        
        self._d_meta.checkAndExpandParams(params)

        self.assert_("param1" in params.keys())

        params = {"param2":"...", "param1":"..."}
        self._d_meta.checkAndExpandParams(params)
        self.assertEqual(params['param1'], "...")

    
    def testCheckParameters(self):
        """ CLASS CModuleMeta check parameters """
        params = { }

        self.assertRaises(
            ModuleImportError,
            self._d_meta.checkAndExpandParams,
            params)


    def testMetadata(self):
        """ CLASS CModuleMeta additional data """

        self.assertEqual(self._d_meta.getAuthor(), "Hannes Matuschek <hmatuschek@gmx.net>")
        self.assertEqual(self._d_meta.getVersion(), "0.0.1a")


    def testInterface(self):
        """ CLASS CModuleMeta abstract methods """
        self.assertRaises( Exception, self._d_meta.checkDependencies)

        self.assertRaises( Exception, self._d_meta.isInnerModule)

