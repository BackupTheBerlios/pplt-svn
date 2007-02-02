import unittest
from edef import AssemblyMeta
import xml.dom.minidom
import time
import xml.xpath

xml1 = """<?xml version="1.0"?>
    <Assembly version="1.0">
        <Author>Hannes Matuschek</Author>
        <Version>0.1</Version>

        <Description lang="en">
            This assembly wrapps simply the AND Module!
        </Description>
        <Description lang="de">
            Dieses Assembly beinhaltet einfach nur das AND Modul.
        </Description>

        <Requires>
            <Module name="logic.AND"/>
        </Requires>
        
        <Provides>
            <Input name="a" type="bool" link="and.i_a"/>
            <Input name="b" type="bool" link="and.i_b"/>
            <Output name="out" type="bool" link="and.o_out"/>
        </Provides>
        
        <Setup>
            <Module name="logic.AND" alias="and"/>
        </Setup>
    </Assembly>"""


class testAssembly(unittest.TestCase):
    
    def testInitAssembly(self):
        dom = xml.dom.minidom.parseString(xml1)
        asmm = AssemblyMeta(dom)
       
        asm = asmm.instance({})

        def test_out(value):
            print "Value %s"%value
        
        asm.o_out += test_out
        asm.i_a(True)
        asm.i_b(True)
        time.sleep(0.01)
