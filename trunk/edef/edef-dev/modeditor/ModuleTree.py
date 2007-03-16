import wx
from edef.dev import Model, Controller, NavigatorPanel
import os.path
import re
from edef.dev import Tools
from icon_module import getBitmap as getModuleBitmap


class ModuleTreePanel(NavigatorPanel):
    def __init__(self, parent, ID):
        NavigatorPanel.__init__(self, parent, ID, "Modules")
        self._tree = eDevModuleTree(self, -1)
        box = self.GetSizer()
        box.Add(self._tree, 1, wx.EXPAND)

    def getModuleTree(self): return self._tree




class eDevModuleTree(wx.TreeCtrl):
    
    def __init__(self, parent, ID):
        wx.TreeCtrl.__init__(self, parent, ID, size=wx.Size(-1,-1),
                             style=wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT|wx.TR_NO_LINES|wx.TR_FULL_ROW_HIGHLIGHT)
        
        self._d_imgs = wx.ImageList(16,16)
        self._bmp_class = self._d_imgs.Add( wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16,16)) )
        self._bmp_class_open = self._d_imgs.Add( wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16,16)) )
        self._bmp_module = self._d_imgs.Add( getModuleBitmap() )
        self.SetImageList(self._d_imgs)

        self._d_model = Model()
        self._d_controller = Controller()
        self._d_mainframe  = self._d_controller.getMainFrame()
        self._logger = self._d_controller.getLogger()

        self._d_root = self.AddRoot("root")
        self.SetPyData(self._d_root, ("Class","mod:/") )

        mods = self._d_model.openURI("mod://")
        self.popClasses(mods)

        self._left_down_uri = None

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelection)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivate)
        self.Bind(wx.EVT_SET_FOCUS, self.OnFocus)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMove)


    def popClasses(self, mods, item=None):
        if item == None:
            item = self._d_root
        (typ, prefix) = self.GetPyData(item)
        
        def class_filter(uri): return re.match("^%s/\w+/.+$"%prefix, uri)
        modules = filter(class_filter, mods)
        for mod_uri in modules:
            m = re.match("^%s/(\w+)/.+$"%prefix, mod_uri)
            class_name = m.group(1)
            uri = "%s/%s"%(prefix,class_name)
            
            if self.hasClassURI(uri, self._d_root):
                citem = self.getItemByURI(uri, self._d_root)
                self.popModules(mods,citem)
                continue
            
            citem = self.AppendItem(item, class_name)
            self.SetPyData(citem, ("Class", uri) )
            self.SetItemImage(citem, self._bmp_class, wx.TreeItemIcon_Normal)
            self.SetItemImage(citem, self._bmp_class_open, wx.TreeItemIcon_Expanded)
            self.popClasses(mods, citem)

        self.popModules(mods, item)


    def popModules(self, mods, item=None):
        if item == None:
            item = self._d_root

        (typ, prefix) = self.GetPyData(item)
        def module_filter(uri): return re.match("^%s/(\w+)$"%prefix, uri)
        modules = filter(module_filter, mods)
        for module in modules:
            if self.hasURI(module, self._d_root): continue
            m = re.match("^%s/(\w+)"%prefix, module)
            mod_name = m.group(1)
            citem = self.AppendItem(item, mod_name)
            self.SetPyData(citem, ("Module", module) )
            self.SetItemImage(citem, self._bmp_module, wx.TreeItemIcon_Normal)
            self.SetItemImage(citem, self._bmp_module, wx.TreeItemIcon_Expanded)
   

    def addURI(self, uri):
        if self.hasURI(uri,self._d_root): return
        (proto, path) = Tools.splitURI(uri)
        if not proto == "mod": return
        self.popClasses([uri])


    def deleteURI(self, uri):
        if not self.hasURI(uri, self._d_root): return
        
        item = self.getItemByURI(uri, self._d_root)
        if self.ItemHasChildren(item): return
        
        (typ, iuri) = self.GetPyData(item)
        if iuri == "mod:/": return
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


    def OnLeftDown(self, evt):
        (item,flag) = self.HitTest(evt.GetPosition())
        if item and flag&(wx.TREE_HITTEST_ONITEMLABEL|wx.TREE_HITTEST_ONITEMICON):
            (typ, uri) = self.GetPyData(item)
            if typ == "Module": self._left_down_uri = uri
        evt.Skip()

    def OnLeftUp(self, evt):
        self._left_down_uri = None

    def OnMove(self, evt):
        if self._left_down_uri:
            self._logger.debug("begin dragging module: %s"%self._left_down_uri)
            drag_uri = wx.TextDataObject(self._left_down_uri)
            dragSrc = wx.DropSource(self)
            dragSrc.SetData(drag_uri)
            dragSrc.DoDragDrop( True )
            self._left_down_uri = None
        evt.Skip()


    def _updateMainFrame(self, item=None):
        if not item: item = self.GetSelection()
        self._d_mainframe.bindNew()
        self._d_mainframe.bindOpen()
        self._d_mainframe.bindDelete()
        
        if not item: return
        (typ, uri) = self.GetPyData(item)
        if typ == "Module":
            self._d_mainframe.bindOpen(self.OnModuleOpen, "&Open module")
            self._d_mainframe.bindDelete(self.OnModuleDelete, "&Delete module")
        elif typ == "Class":
            self._d_mainframe.bindOpen(self.OnClassOpen, "&Open class")
        self._d_mainframe.bindNew(self.OnNewModule, "&New module")


    def OnActivate(self, evt):
        item = evt.GetItem()
        (typ, uri) = self.GetPyData(item)
        if typ == "Class":
            self.Toggle(item)
            return
        self._d_controller.DocumentOpen(uri)

    def OnModuleOpen(self, evt=None):
        item = self.GetSelection()
        if not item: return
        (typ, uri) = self.GetPyData(item)
        if typ=="Module":
            self._d_controller.DocumentOpen(uri)

    def OnClassOpen(self, evt=None):
        item = self.GetSelection()
        if not item: return
        (typ, uri) = self.GetPyData(item)
        if typ == "Class":
            self.Expand(item)

    def OnNewModule(self, evt=None):
        self._d_controller.DocumentOpen("mod://")

    def OnModuleDelete(self, evt=None):
        item = self.GetSelection()
        if not item: return
        (typ, uri) = self.GetPyData(item)
        if typ == "Class": return

        self._d_controller.DocumentDelete(uri)
        self.deleteURI(uri)
        
