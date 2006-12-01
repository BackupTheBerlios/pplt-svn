import unittest
from pplt import CAssemblyMeta, CImporter
import xml.dom.minidom

xml_doc="""<?xml version="1.0"?>
    <Assembly version="1.0">
    
        <Require>
            <Module>stream_reflection</Module>
            <Parameter name="to" default="1"/>
        </Require>


        <Setup>
            <Load module="stream_reflection" namespace="test">
                <Parameter name="timeout"><ValueOf>to</ValueOf></Parameter>
            </Load>                
        </Setup>
    </Assembly>"""

xml_doc2="""<?xml version="1.0"?>
    <Assembly version="1.0">
    
        <Require>
            <Module>stream_reflection</Module>
            <Module>stream_dump</Module>
            <Parameter name="timeout" default="1"/>
        </Require>


        <Setup>
            <Load module="stream_reflection" namespace="refl">
                <Parameter name="timeout"><ValueOf>timeout</ValueOf></Parameter>
                
                <Load module="stream_dump" namespace="dump">
                    <Address>1</Address>
                </Load>
                <Load module="stream_hexlify" namespace="hex">
                    <Address>1</Address>
                </Load>
            </Load>                
        </Setup>
    </Assembly>"""


xml_doc3="""<?xml version="1.0"?>
    <Assembly version="1.0">
    
        <Require>
            <Module>stream_hexlify</Module>
        </Require>


        <Setup>
            <Load module="stream_hexlify" namespace="hex"> </Load>                
        </Setup>
    </Assembly>"""


xml_doc4="""<?xml version="1.0"?>
    <Assembly version="1.0">
    
        <Require>
            <Module>not_existing</Module>
        </Require>


        <Setup>
            <Load module="stream_hexlify" namespace="hex"> </Load>                
        </Setup>
    </Assembly>"""



class testAssemblyMeta(unittest.TestCase):

    def testGrammarVersion(self):
        """ CLASS CAssemblyMeta grammar version """
        imp = CImporter()
        doc = xml.dom.minidom.parseString(xml_doc)
        meta = CAssemblyMeta(doc,imp)

    
    def testDependencies(self):
        """ CLASS CAssemblyMeta dependencies """
        imp = CImporter()
        doc = xml.dom.minidom.parseString(xml_doc)
        meta = CAssemblyMeta(doc,imp)
        meta.checkDependencies()

        doc = xml.dom.minidom.parseString(xml_doc4)
        meta = CAssemblyMeta(doc,imp)
        self.assertRaises(Exception, meta.checkDependencies)
    
    def testLoad(self):
        """ CLASS CAssemblyMeta load simple assembly """
        imp = CImporter()
        doc = xml.dom.minidom.parseString(xml_doc)
        meta = CAssemblyMeta(doc, imp)

        mod = meta.instance({'to':"0.1"})
        con1 = mod.connect("test:1")
        con2 = mod.connect("test:1")
        
        con1.write("abc")
        self.assertEqual(con2.read(3),"abc")


    def testCmplxLoad(self):
        """ CLASS CAssemblyMeta load complex assembly """
        imp = CImporter()
        doc = xml.dom.minidom.parseString(xml_doc2)
        meta = CAssemblyMeta(doc,imp)

        mod = meta.instance({'timeout':"0.1"})
        con1 = mod.connect("dump:")
        con2 = mod.connect("hex:")

        con1.write("abc")
        self.assertEqual(con2.read(6), "616263")


    def testInnerLoad(self):
        """ CLASS CAssembly load assembly as inner module """
        imp = CImporter()
        doc = xml.dom.minidom.parseString(xml_doc3)
        meta = CAssemblyMeta(doc, imp)

        root = imp.load("stream_reflection")
        hexl = meta.instance({}, root, "1")
        
        con1 = hexl.connect("hex:")
        con2 = root.connect("1")

        con2.write("abc")
        self.assertEqual(con1.read(6),"616263")


