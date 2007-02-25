import wx
from ElementMapObjects import emModule, emConnection
from Canvas import Canvas
import Events
import edef



class ElementMap( Canvas ):
    _importer = None

    def __init__(self, parent, ID):
        Canvas.__init__(self, parent, ID)
        self._importer = edef.Importer()
       
        self.Bind( Events.EVT_CAN_RCLICK, self.OnRightClick)


    def loadModule(self, name, pos, parameters=None):
        if not parameters: parameters = {}
        return emModule(self, pos, name)
        

    def removeModule(self, mod):
        cons  = self.getConnectionsFrom(mod)
        cons += self.getConnectionsTo(mod)
        for con in cons: self.delObject( con )
        self.delObject( mod )


    def disconnect(self, wire):
        self.delObject( wire )

    
    def addConnection(self, frm, to, auto_redraw=False):
        if self.isConnection(frm, to): return
        con = emConnection(frm,to)
        if auto_redraw: self.redraw()
        return con
   

    def OnRightClick(self, evt):
        #print "Evt object %s"%evt.GetObject()
        evt.Skip()




