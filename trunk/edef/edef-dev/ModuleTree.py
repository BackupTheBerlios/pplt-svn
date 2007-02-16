import wx
from Model import eDevModel
from Controller import eDevController
import os.path
import re
import Tools

class eDevModuleTree(wx.TreeCtrl):
    
    def __init__(self, parent, ID):
        wx.TreeCtrl.__init__(self, parent, ID, size=wx.Size(-1,-1),
                             style=wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT|wx.TR_NO_LINES|wx.TR_FULL_ROW_HIGHLIGHT)
        
        self._d_model = eDevModel()
        self._d_controller = eDevController()
        self._d_mainframe  = self._d_controller.getMainFrame()

        self._d_root = self.AddRoot("root")
        self.SetPyData(self._d_root, ("Class","mod:/") )

        mods = self._d_model.openURI("mod://")
        self.popClasses(mods)

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelection)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivate)
        self.Bind(wx.EVT_SET_FOCUS, self.OnFocus)



    def popClasses(self, mods, item=None):
        if item == None:
            item = self._d_root
        (typ, prefix) = self.GetPyData(item)
        
        def class_filter(uri): return re.match("^%s/\w+/.+$"%prefix, uri)
        modules = filter(class_filter, mods)
        print "classes in %s: %s of %s"%(prefix, modules, mods)
        for mod_uri in modules:
            m = re.match("^%s/(\w+)/.+$"%prefix, mod_uri)
            class_name = m.group(1)
            uri = "%s/%s"%(prefix,class_name)
            
            if self.hasClassURI(uri, self._d_root):
                citem = self.getItemByURI(uri, self._d_root)
                self.popModules(mods,citem)
                continue
            
            citem = self.AppendItem(item, "c "+class_name)
            self.SetPyData(citem, ("Class", uri) )
            self.popClasses(mods, citem)

        self.popModules(mods, item)


    def popModules(self, mods, item=None):
        if item == None:
            item = self._d_root

        (typ, prefix) = self.GetPyData(item)
        def module_filter(uri): return re.match("^%s/(\w+)$"%prefix, uri)
        modules = filter(module_filter, mods)
        print "Modules in %s: %s"%(prefix, modules)
        for module in modules:
            if self.hasURI(module, self._d_root): continue
            m = re.match("^%s/(\w+)"%prefix, module)
            mod_name = m.group(1)
            citem = self.AppendItem(item, "m "+mod_name)
            self.SetPyData(citem, ("Module", module) )
   

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

    def _updateMainFrame(self, item=None):
        if not item: item = self.GetSelection()
        self._d_mainframe.bindNew()
        self._d_mainframe.bindOpen()
        self._d_mainframe.bindDelete()
        
        if not item: return
        (typ, uri) = self.GetPyData(item)
        if typ == "Module":
            self._d_mainframe.bindOpen(self.OnModuleOpen)
            self._d_mainframe.bindDelete(self.OnModuleDelete)
        elif typ == "Class":
            self._d_mainframe.bindOpen(self.OnClassOpen)
        self._d_mainframe.bindNew(self.OnNewModule)

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
        
