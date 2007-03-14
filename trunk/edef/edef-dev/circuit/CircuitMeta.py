import xml.dom.minidom
import xml.xpath
import logging


class CircuitMeta:
    def __init__(self, xml_string):
        self._dom = xml.dom.minidom.parseString(xml_string)
        self._logger = logging.getLogger("edef.dev")

    def getModules(self):
        mod_table = dict()
        mods = xml.xpath.Evaluate("/Circuit/Module",self._dom)
        for mod in mods:
            (ID, name, label, pos, param) = self._getModule(mod.getAttribute("id"))
            mod_table[ID] = (name, label, pos, param)
        self._logger.debug("Found %s"%mod_table)
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


    def _getModule(self, ID):
        node = xml.xpath.Evaluate("/Circuit/Module[@id=%s]"%ID, self._dom)[0]
        ID = node.getAttribute("id")
        name = node.getAttribute("name")
        label = node.getAttribute("label")
        pos = ( int(node.getAttribute("x")), int(node.getAttribute("y")) )
        params = self._getParameterDict(ID)
        return (ID, name, label, pos, params)

    def _getParameterDict(self, ID):
        params = dict()
        
        nodes = xml.xpath.Evaluate("/Circuit/Module[@id=%s]/Parameter"%ID, self._dom)
        self._logger.debug("Found %i params for mod (id %s)"%(len(nodes), ID))
        for node in nodes:
            name = str(node.getAttribute("name"))
            try: value = node.firstChild.wholeText.strip()
            except: raise Exception("Parameter %s has no value"%name)
            params[name] = value
        return params

