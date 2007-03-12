import xml.dom.minidom
import xml.xpath

class CircuitMeta:
    def __init__(self, xml_string):
        self._dom = xml.dom.minidom.parseString(xml_string)

    def getModules(self):
        mod_table = dict()
        mods = xml.xpath.Evaluate("/Circuit/Module",self._dom)
        for mod in mods:
            (ID, name, pos, param) = self._getModule(mod)
            mod_table[ID] = (name, pos, param)

        return mod_table


    def getWires(self, ID):
        wire_list = []
        wires = xml.xpath.Evaluate("/Circuit/Wire[From/@id=%s]"%ID, self._dom)
        for wire in wires:
            frm_id  = xml.xpath.Evaluate("string(From/@id)",wire)
            frm_pin = xml.xpath.Evaluate("string(From/@pin)",wire)
            to_id   = xml.xpath.Evaluate("string(To/@id)",wire)
            to_pin  = xml.xpath.Evaluate("string(To/@pin)",wire)
            wire_list.append( ((frm_id, frm_pin), (to_id,to_pin)) )
        return wire_list


    def _getModule(self, node):
        ID = node.getAttribute("id")
        name = node.getAttribute("name")
        pos = ( int(node.getAttribute("x")), int(node.getAttribute("y")) )
        params = self._getParameterDict(node)
        return (ID, name, pos, params)

    def _getParameterDict(self, node):
        params = dict()
        
        nodes = xml.xpath.Evaluate("Module/Parameter", node)
        for node in nodes:
            name = node.getAttribute("name")
            try: value = node.firstChild.wholeText.strip()
            except: raise Exception("Parameter %s has no value"%name)
            params[name] = value
        return params

