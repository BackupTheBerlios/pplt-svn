import wx
import re
import edef
from edef.dev.EditorInterface import eDevEditorInterface as EditorInterface
from ElementMap import ElementMap
from SimpleCanvasObjects import gModule
from ElementMapObjects import emModule
from edef.dev import Controller, Model, ComponentManager
from edef.dev import Tools, showExceptionDialog
from CircuitMeta import CircuitMeta
from xml.dom.minidom import getDOMImplementation
from Dialogs import SaveAsDialog


class CircuitEditor(EditorInterface, ElementMap):
    
    def __init__(self, parent, ID, uri):
        EditorInterface.__init__(self, parent, False, uri)
        ElementMap.__init__(self, parent, ID)

        self._controller = Controller()
        self._logger     = self._controller.getLogger()
        self._model      = Model()
        self._circtree   = ComponentManager().getComponent("circuit").getCircuitTree()
        self._importer   = edef.Importer()
        self._mainframe  = self._controller.getMainFrame()
        
        self.setTitle(uri)
       
        if not uri == "circ://":
            self._loadCircuit(uri)
            self.redraw()
            self.setModified(False)

        self._target = CircuitDropTarget(self)
        self.SetDropTarget( self._target )


    def _loadCircuit(self, uri):
        wire_list = []
        mod_table = {}
        self._logger.debug("Load %s"%uri)
        
        xml = self._model.openURI(uri)
        meta = CircuitMeta(xml)
        mods = meta.getModules()
        
        for (ID, (name, label, (x,y), params)) in mods.items():
            self._logger.debug("Load module %s as %s @ %s,%s"%(name, label, x,y))
            moduri = "mod://"+"/".join(name.split("."))
            mod_table[ID] = self.loadModule(moduri, x,y, params)
            mod_table[ID].setLabel(label)
            wire_list += meta.getWires(ID)
            
        for ( frm, to ) in wire_list:
            (frm_id, frm_pin) = frm
            (to_id,  to_pin)  = to
            frm = mod_table[frm_id].getPin(frm_pin)
            to  = mod_table[to_id].getPin(to_pin)
            self.connect(frm,to)
         

    def OnSelected(self, evt=None):
        self._updateMainFrame()


    def _updateMainFrame(self):
        self._mainframe.bindCopy()
        self._mainframe.bindCut()
        self._mainframe.bindPaste()
        self._mainframe.bindRedo()
        self._mainframe.bindUndo()
        
        self._mainframe.bindSaveAs(self.OnSaveAs)
        if self.isModified() and self.getURI() != "circ://":
            self._mainframe.bindSave(self.OnSave)
        else: self._mainframe.bindSave()


    def OnModified(self):
        self.setModified(True)
        self._updateMainFrame()
        

    def OnSave(self, evt):
        self._logger.debug("On save...")
        
        if self.getURI() == "circ://":
            self.OnSaveAs(evt)
            return
                    
        txt = self._to_xml().toprettyxml(" ")
        self._model.saveURI(self.getURI(), txt)
        self.setModified(False)
        self._updateMainFrame()


    def OnSaveAs(self, evt):
        dlg = SaveAsDialog(self, -1)
        if dlg.ShowModal()==wx.ID_CANCEL:
            dlg.Destroy()
            return
        uri = dlg.getSelection()
        dlg.Destroy()

        try:
            txt = self._to_xml().toprettyxml("  ")
            self._model.saveURI(uri, txt)
        except:
            showExceptionDialog(self, -1, "Unable to save file to %s"%uri)

        self.setURI(uri)
        self.setTitle(uri)
        self._circtree.addURI(uri)
        self.setModified(False)
        self._updateMainFrame()


    def _to_xml(self):
        dom_impl = getDOMImplementation()

        doc = dom_impl.createDocument(None, "Circuit", None)
        root = doc.documentElement

        mods = self.getObjects(gModule)
        for idx in range(len(mods)):
            mod = mods[idx]
            mod_node = mod._to_xml(doc, idx)
            cons = self.getConnectionsFrom(mod)
            for con in cons:
                to_pin = con.getTo().getName()
                frm_pin = con.getFrom().getName()
                to_idx = mods.index(con.getTo().getModule())
                wire = doc.createElement("Wire")
                frm = doc.createElement("From")
                frm.setAttribute("id", str(idx))
                frm.setAttribute("pin",frm_pin)
                wire.appendChild(frm)
                to = doc.createElement("To")
                to.setAttribute("id", str(to_idx))
                to.setAttribute("pin", to_pin)
                wire.appendChild(to)
                root.appendChild(wire)
            root.appendChild(mod_node)
        return doc



class CircuitDropTarget(wx.TextDropTarget):
    def __init__(self, editor):
        wx.TextDropTarget.__init__(self)
        self._editor = editor
        self._model  = Model()
    
    #FIXME use OnDragOver() to check if there can a module be placed

    def OnDropText(self, x, y, uri):
        if not self._model.checkURI(uri):
            raise Exception("Unknown module %s"%uri)
        if not re.match("^mod://",uri):
            raise Exception("Can only place modules here!")
        (x,y) = self._editor._convertCoords( (x,y) )
        self._editor.loadModule(uri, x, y)





