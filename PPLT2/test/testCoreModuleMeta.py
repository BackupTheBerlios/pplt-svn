import xml.dom.minidom
import unittest
from core import CCoreModuleMeta

class testCoreModuleMeta (unittest.TestCase):
    _d_doc1 = """<?xml version="1.0"?>
        <Module version="1.0">
            <Class>Test</Class>
            <Archive>...</Archive>
    
            <Type>root</Type>

            <Require>
                <PyModule>xml</PyModule>
            </Require>
        </Module>"""

    _d_doc2 = """<?xml version="1.0"?>
        <Module version="1.0">
            <Class>Test</Class>
            <Archive>...</Archive>

            <Type>root</Type>

            <Require>
                <PyModule>not-existing</PyModule>
            </Require>
        </Module>"""

    _d_doc3 = """<?xml version="1.0"?>
        <Module version="1.1">
            <Class>Test</Class>
            <Archive>...</Archive>
    
            <Type>root</Type>

            <Require>
                <PyModule>xml</PyModule>
            </Require>
        </Module>"""



    def testDependencies(self):
        """ CLASS CCoreModuleMeta dependencies """
        dom = xml.dom.minidom.parseString(self._d_doc1).documentElement
        
        meta = CCoreModuleMeta(dom, ".")
        meta.checkDependencies()

        dom = xml.dom.minidom.parseString(self._d_doc2).documentElement
        
        meta = CCoreModuleMeta(dom, ".")
        self.assertRaises(
            Exception,
            meta.checkDependencies)


    def testGrammarVersion(self):
        """ CLASS CCoreModuleMeta grammar version check """
        dom = xml.dom.minidom.parseString(self._d_doc3).documentElement

        self.assertRaises(
            Exception,
            CCoreModuleMeta,
            dom, "..")


