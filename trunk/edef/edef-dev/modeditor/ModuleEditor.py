import sys
import wx
from wx.lib.scrolledpanel import ScrolledPanel
import xml.dom.minidom
import xml.xpath

from ModuleEditorBasic import eDevModuleEditorBasic
from ModuleEditorRequire import eDevModuleEditorRequire
from ModuleEditorProvide import eDevModuleEditorProvide
from edef.dev.EditorInterface import eDevEditorInterface

from edef.dev import Model, Controller, ComponentManager
from edef.dev import Events     #FIXME write own events
from edef.dev import Dialogs
from Tools import getModuleName
from edef.dev import Tools


class eDevModuleEditor(ScrolledPanel, eDevEditorInterface):
    _d_txt  = None

    def __init__(self, parent, ID, uri):
        ScrolledPanel.__init__(self, parent, ID)
        eDevEditorInterface.__init__(self, parent, False, uri)

        self._controller = Controller()
        self._model      = Model()
        self._mainframe  = self._controller.getMainFrame()
        self._component_manager = ComponentManager()
        self._moduletree = self._component_manager.getComponent("modeditor").getModuleTree()
        self._notebook   = self._controller.getNotebook()


        if uri == "mod://":
            txt = '<?xml version="1.0"?><Module version="1.0"/>'
            title = "unsaved"
        else:
            txt = self._model.openURI(uri)
            title = getModuleName(uri)
        self.setTitle(title)
        
        self._d_doc = xml.dom.minidom.parseString(txt)

        vert_box = wx.BoxSizer(wx.VERTICAL)
        self._d_basic_data = eDevModuleEditorBasic(self, -1, self._d_doc)
        self._d_require = eDevModuleEditorRequire(self, -1, self._d_doc)
        self._d_provide = eDevModuleEditorProvide(self, -1, self._d_doc)

        self.Bind(Events.EVT_MODIFIED, self.OnModified, self._d_basic_data)
        self.Bind(Events.EVT_MODIFIED, self.OnModified, self._d_require)
        self.Bind(Events.EVT_MODIFIED, self.OnModified, self._d_provide)

        vert_box.Add(self._d_basic_data, 0, wx.EXPAND|wx.ALL, 15)
        vert_box.Add(self._d_require, 0, wx.EXPAND|wx.ALL, 15)
        vert_box.Add(self._d_provide, 0, wx.EXPAND|wx.ALL, 15)

        self.SetSizer(vert_box)
        self.SetAutoLayout(1)
        self.SetupScrolling()


    def OnModified(self, evt):
        #print "Something was modified"
        self.setModified()
        event = Events.PageModifiedEvent(Events._event_modified, self.GetId())
        event.SetPage(self)
        self.GetEventHandler().ProcessEvent(event)
        evt.Skip()
        self._updateMainFrame()

    
    def OnSelected(self):
        self._updateMainFrame()

    
    def _updateMainFrame(self):
        self._mainframe.bindCopy()
        self._mainframe.bindCut()
        self._mainframe.bindPaste()
        self._mainframe.bindRedo()
        self._mainframe.bindUndo()

        self._mainframe.bindSaveAs(self.OnSaveAs)
        if self.isModified() and self.getURI() != "mod://":
            self._mainframe.bindSave(self.OnSave)
        else: self._mainframe.bindSave()


    def _toXML(self):
        impl = xml.dom.minidom.getDOMImplementation()
        dom  = impl.createDocument(None, "Module", None)
        dom.documentElement.setAttribute("version","1.0")
        
        node_list = self._d_basic_data.ToXML(dom)
        
        node_list += self._d_require.ToXML(dom)
        
        node_list += self._d_provide.ToXML(dom)
        
        for node in node_list:
            dom.documentElement.appendChild(node)

        return dom.toprettyxml("    ")


    def OnSave(self, evt=None):
        if self.getURI() == "mod://": return
        
        txt = self._toXML()
        self._controller.DocumentSave(self.getURI(),txt)
        self.setModified(False)
        self._updateMainFrame()


    def OnSaveAs(self, evt=None):
        selected = False
        while not selected:
            dlg = Dialogs.eDevSaveModuleAsDialog(self, -1)
            if dlg.ShowModal() != wx.ID_OK:
                return
            uri = "mod://%s"%dlg.getSelection()
            dlg.Destroy()
            if self._model.checkURI(uri):
                # FIXME Override?
                continue
            selected = True
        
        if not self._model.checkURI(uri):
            self._controller.DocumentSave(uri, self._toXML())
            self._moduletree.addURI(uri)
        else:
            self._controller.DocumentSave(uri, self._toXML())
        self.setURI(uri)
        self.setTitle( getModuleName(uri) )

