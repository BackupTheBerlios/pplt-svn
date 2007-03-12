from Canvas import coConnection
from SimpleCanvasObjects import gModule, gPin
import edef
import Events
import wx
import logging


class emConnection( coConnection ):

    def __init__(self, frm, to):
        self._logger = logging.getLogger("edef.dev")
        
        coConnection.__init__(self, frm, to)
      
        # connect input of "to" with output of "from"
        (frm_mod, frm_name) = frm.getModule(), frm.getName()
        (to_mod, to_name)   = to.getModule(), to.getName()
        frm_out = getattr(frm_mod, frm_name)
        frm_out += getattr(to_mod, to_name)


    def __del__(self):
        self._logger.debug("Disconnect %s from %s"%(self.getFrom(), self.getTo()))
        (frm_mod, frm_name) = self.getFrom().getModule(), self.getFrom().getName()
        (to_mod, to_name)   = self.getTo().getModule(), self.getTo().getName()
        outp = getattr(frm_mod, frm_name)
        inp  = getattr(to_mod, to_name)
        outp -= inp



class emModule( gModule ):

    def __init__(self, canvas, pos, name, parameters):
        #self._logger = logging.getLogger("edef.dev")

        imp = edef.Importer()
        (path, module_meta) = imp.getModuleMeta(name)

        #FIXME: layout_rules = meta.getLayoutRules()
        layout_rules = None
        gModule.__init__(self, canvas, pos, name, layout_rules)

        for pin in module_meta.getInputs(): gPin(self, "i_"+pin)
        for pin in module_meta.getOutputs(): gPin(self, "o_"+pin)
        
        # contextmenu
        self._id_delete = wx.NewId()
        self._ctx_menu = wx.Menu()
        self._ctx_menu.Append(self._id_delete, "Delete Module")



class DefaultGraficModule(emModule):
    """ This class will be used as a std. grafical representation of a module.
        It behaves like a module so all overloaded operators are present. """
    _module = None
    _name   = None
    _parameters = None

    def __init__(self, canvas, pos, name, parameters):
        emModule.__init__(self, canvas, pos, name, parameters)
        # instance the edef-module to be wrapped
        imp = edef.Importer()
        self._module = imp.load(name, parameters)
        self._parameters = parameters
        self._name = name

    def getParameters(self): return self._parameters
    def getName(self): return self._name

    def _to_xml(self, dom, ID):
        (x,y) = self.getPosition()
        params = self.getParameters()
        mod_node = dom.createElement("Module")

        mod_node.setAttribute("id", str(ID))
        mod_node.setAttribute("name", self.getName())
        mod_node.setAttribute("x", str(x))
        mod_node.setAttribute("y", str(y))

        for (param, value) in params:
            pnode = dom.createElement("Parameter")
            pnode.setAttribute("name", param)
            val_node = dom.createTextNode(value)
            pnode.appendChild(val_node)
            mod_node.appendChild(pnode)
    
        return mod_node


    def __getattr__(self, attr):
        return getattr(self._module, attr)

