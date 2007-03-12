import wx
from edef.dev import Model, Controller, NavigatorPanel
import os.path
import re
from edef.dev import Tools

class CircuitTreePanel(NavigatorPanel):
    def __init__(self, parent, ID):
        NavigatorPanel.__init__(self, parent, ID, "Circuits")
        self._tree = CircuitTree(self, -1)
        box = self.GetSizer()
        box.Add(self._tree, 1, wx.EXPAND)

    def getCircuitTree(self): return self._tree




class CircuitTree(wx.TreeCtrl):
    
    def __init__(self, parent, ID):
        wx.TreeCtrl.__init__(self, parent, ID, size=wx.Size(-1,-1),
                             style=wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT|wx.TR_NO_LINES|wx.TR_FULL_ROW_HIGHLIGHT)
        
        self._d_imgs = wx.ImageList(16,16)
        self._bmp_class = self._d_imgs.Add( wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16,16)) )
        self._bmp_class_open = self._d_imgs.Add( wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16,16)) )
        self._bmp_module = self._d_imgs.Add( wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, (16,16)) )
        self.SetImageList(self._d_imgs)

        self._d_model = Model()
        self._d_controller = Controller()
        self._d_mainframe  = self._d_controller.getMainFrame()
        self._logger = self._d_controller.getLogger()

        self._d_root = self.AddRoot("root")
        self.SetPyData(self._d_root, ("Class","circ:/") )

        circs = self._d_model.openURI("circ://")
        self.popClasses(circs)

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelection)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivate)
        self.Bind(wx.EVT_SET_FOCUS, self.OnFocus)


    def popClasses(self, circs, item=None):
        if item == None:
            item = self._d_root
        (typ, prefix) = self.GetPyData(item)
        
        def class_filter(uri): return re.match("^%s/\w+/.+$"%prefix, uri)
        circuits = filter(class_filter, circs)
        for circ_uri in circuits:
            m = re.match("^%s/(\w+)/.+$"%prefix, circ_uri)
            class_name = m.group(1)
            uri = "%s/%s"%(prefix,class_name)
            
            if self.hasClassURI(uri, self._d_root):
                citem = self.getItemByURI(uri, self._d_root)
                self.popCircuits(circs,citem)
                continue
            
            citem = self.AppendItem(item, class_name)
            self.SetPyData(citem, ("Class", uri) )
            self.SetItemImage(citem, self._bmp_class, wx.TreeItemIcon_Normal)
            self.SetItemImage(citem, self._bmp_class_open, wx.TreeItemIcon_Expanded)
            self.popClasses(circs, citem)

        self.popCircuits(circs, item)


    def popCircuits(self, circs, item=None):
        if item == None:
            item = self._d_root

        (typ, prefix) = self.GetPyData(item)
        def circuit_filter(uri): return re.match("^%s/(\w+)$"%prefix, uri)
        circuits = filter(circuit_filter, circs)
        for circuit in circuits:
            if self.hasURI(circuit, self._d_root): continue
            m = re.match("^%s/(\w+)"%prefix, circuit)
            circ_name = m.group(1)
            citem = self.AppendItem(item, circ_name)
            self.SetPyData(citem, ("Circuit", circuit) )
            self.SetItemImage(citem, self._bmp_module, wx.TreeItemIcon_Normal)
            self.SetItemImage(citem, self._bmp_module, wx.TreeItemIcon_Expanded)
   

    def addURI(self, uri):
        if self.hasURI(uri,self._d_root): return
        (proto, path) = Tools.splitURI(uri)
        if not proto == "circ": return
        self.popClasses([uri])


    def deleteURI(self, uri):
        if not self.hasURI(uri, self._d_root): return
        
        item = self.getItemByURI(uri, self._d_root)
        if self.ItemHasChildren(item): return
        
        (typ, iuri) = self.GetPyData(item)
        if iuri == "circ:/": return
        self.Delete(item)
        
        pitem = self.GetItemParent(item)
        (typ, uri) = self.GetPyData(pitem)
        self.deleteURI(uri)
   

    def hasURI(self, uri, item):
        if self.getItemByURI(uri, item): return True
        return False

    def getItemByURI(self, uri, item, cookie=None):
        if not item: return None
        (typ, iuri) = self.GetPyData(item)
        if iuri == uri: return item
        
        citem = self.GetFirstChild(item)
        if citem: (citem, ncookie) = citem
        ret = self.getItemByURI(uri, citem, ncookie)
        if ret: return ret

        item = self.GetNextSibling(item)
        return self.getItemByURI(uri, item, cookie)


    def hasClassURI(self, uri, item, cookie=None):
        if not item: return False
        (typ, iuri) = self.GetPyData(item)
        if iuri == uri and typ=="Class": return True
        
        citem = self.GetFirstChild(item)
        if citem: (citem, ncookie) = citem
        if self.hasClassURI(uri, citem, ncookie): return True

        item = self.GetNextSibling(item)
        if self.hasClassURI(uri, item): return True
        return False
    

    #
    # CONTROLLER PART:
    #
    def OnFocus(self, evt):
        self._updateMainFrame()
        evt.Skip()


    def OnSelection(self, evt):
        item = evt.GetItem()
        self._updateMainFrame(item)
        evt.Skip()


    def _updateMainFrame(self, item=None):
        if not item: item = self.GetSelection()
        self._d_mainframe.bindNew()
        self._d_mainframe.bindOpen()
        self._d_mainframe.bindDelete()
        
        if not item: return
        (typ, uri) = self.GetPyData(item)
        if typ == "Circuit":
            self._d_mainframe.bindOpen(self.OnCircuitOpen)
            self._d_mainframe.bindDelete(self.OnCircuitDelete)
        elif typ == "Class":
            self._d_mainframe.bindOpen(self.OnClassOpen)
        self._d_mainframe.bindNew(self.OnNewCircuit)

    def OnActivate(self, evt):
        item = evt.GetItem()
        (typ, uri) = self.GetPyData(item)
        if typ == "Class":
            self.Toggle(item)
            return
        self._d_controller.DocumentOpen(uri)

    def OnCircuitOpen(self, evt=None):
        item = self.GetSelection()
        if not item: return
        (typ, uri) = self.GetPyData(item)
        if typ=="Circuit":
            self._d_controller.DocumentOpen(uri)

    def OnClassOpen(self, evt=None):
        item = self.GetSelection()
        if not item: return
        (typ, uri) = self.GetPyData(item)
        if typ == "Class":
            self.Expand(item)

    def OnNewCircuit(self, evt=None):
        self._d_controller.DocumentOpen("circ://")

    def OnCircuitDelete(self, evt=None):
        item = self.GetSelection()
        if not item: return
        (typ, uri) = self.GetPyData(item)
        if typ == "Class": return

        self._d_controller.DocumentDelete(uri)
        self.deleteURI(uri)
        
