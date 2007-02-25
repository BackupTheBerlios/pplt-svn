from CanvasObjects import coConnection
from SimpleCanvasObjects import gModule, gPin
import edef
import Events
import wx

class emConnection( coConnection ):

    def __init__(self, frm, to, nodes=[]):
        coConnection.__init__(self, frm, to, nodes)
       
        self._id_remove = wx.NewId()
        
        self._ctx_menu = wx.Menu()
        self._ctx_menu.Append(self._id_remove, "remove connection")

        self.getCanvas().Bind(Events.EVT_CAN_RCLICK, self.OnRClick)
        self.getCanvas().Bind(wx.EVT_MENU, self.OnRemove, id=self._id_remove)


    def OnRClick(self, evt):
        if not evt.GetObject() == self:
            evt.Skip()
            return
        cv = self.getCanvas()
        cv.PopupMenu(self._ctx_menu)

    def OnRemove(self, evt):
        self.getCanvas().disconnect(self)
        self.getCanvas().redraw()



class emModule( gModule ):
    _module = None

    def __init__(self, canvas, pos, name, parameters=None):
        if not parameters: parameters={}
        imp = edef.Importer()

        (path, meta) = imp.getModuleMeta(name)
        inps = meta.getInputs()
        outs = meta.getOutputs()

        #FIXME: layout_rules = meta.getLayoutRules()
        layout_rules = None
        gModule.__init__(self, canvas, pos, name, layout_rules)

        for inp in inps: gPin(self, "i_"+inp)
        for out in outs: gPin(self, "o_"+out)

        self._module = imp.load(name, parameters)
        
        self._id_delete = wx.NewId()
        self._ctx_menu = wx.Menu()
        self._ctx_menu.Append(self._id_delete, "Delete Module")

        canvas.Bind(Events.EVT_CAN_RCLICK, self.OnRightClick)
        canvas.Bind(wx.EVT_MENU, self.OnDelete, id=self._id_delete)

    def OnRightClick(self, evt):
        if not evt.GetObject() == self:
            evt.Skip()
            return
        self.getCanvas().PopupMenu(self._ctx_menu)
        evt.Skip()

    def OnDelete(self, evt):
        self.getCanvas().removeModule(self)
        self.getCanvas().redraw()
