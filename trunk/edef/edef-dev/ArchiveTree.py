import wx
from Model import eDevModel
import fnmatch
from Controller import eDevController
import Tools

class eDevArchiveTree(wx.TreeCtrl):
    

    def __init__(self, parent, ID):
        wx.TreeCtrl.__init__(self, parent, ID, size=wx.Size(-1,-1),
                             style=wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT|wx.TR_NO_LINES|wx.TR_FULL_ROW_HIGHLIGHT)
        
        self._d_model = eDevModel()
        self._d_controller = eDevController()
        self._d_mainframe = self._d_controller.getMainFrame()

        self._d_root = self.AddRoot("root")
        self.SetPyData(self._d_root, (None,None))

        #Add all archives:
        archives = self._d_model.openURI("zip://")
        print "Found archives: %s"%archives
        for archive_uri in archives:
            uri_list = self._d_model.openURI(archive_uri)
            archive_name = Tools.getArchive(archive_uri)
            arch_item = self.AppendItem(self._d_root, archive_name)
            self.SetPyData(arch_item, ("Archive", archive_uri) )

            for file_uri in uri_list:
                file_name = Tools.getPyFile(file_uri)
                file_item = self.AppendItem(arch_item, file_name)
                self.SetPyData(file_item, ("File", file_uri))

        # Events:
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelection)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivate)
        self.Bind(wx.EVT_SET_FOCUS, self.OnFocus)

    def removeURI(self, uri):
        item = self.getItemByURI(uri,self._d_root)
        if not item: raise Exception("Item %s not found"%uri)
        self.Delete(item)

    def addURI(self, uri):
        if self.getItemByURI(uri, self._d_root): return
        (proto, path) = Tools.splitURI(uri)
        
        if proto == "py":
            (ar, py) = Tools.splitPyFile(path)
            item = self.getItemByURI("zip://"+ar, self._d_root)
            fitem = self.AppendItem(item, py)
            self.SetPyData(fitem, ("File", uri))
        elif proto == "zip":
            item = self.AppendItem(self._d_root, path)
            self.SetPyData(item, ("Archive",uri))
        else: raise Exception("Unkonw URI %s"%uri)
        

    def getItemByURI(self, uri, item):
        (typ, iuri) = self.GetPyData(item)
        if iuri==uri: return item
        (citem, cookie) = self.GetFirstChild(item)
        
        while citem:
            ret = self.getItemByURI(uri, citem)
            if ret != None: return ret
            (citem, cookie) = self.GetNextChild(item,cookie)
 

    
    #
    # CONTROLLER PART
    #
    def OnFocus(self, evt):
       self._updateMainFrame()
       evt.Skip()


    def OnSelection(self, event):
        item = event.GetItem()
        self._updateMainFrame(item)
        event.Skip()


    def _updateMainFrame(self, item=None):
        if not item: item = self.GetSelection()
        
        self._d_mainframe.bindNew()
        self._d_mainframe.bindOpen()
        self._d_mainframe.bindDelete()
        
        if not item: return
        (typ, uri) = self.GetPyData(item)

        if typ is "File":
            self._d_mainframe.bindOpen(self.OpenFile)
            self._d_mainframe.bindDelete(self.DeleteFile)
        elif typ is "Archive":
            self._d_mainframe.bindNew(self.NewFile)
            self._d_mainframe.bindOpen(self.OpenArchive)
            #self._d_mainframe.bindDelete(self.DeleteArchive)
  

    def OnActivate(self, event):
        item = event.GetItem()
        (typ, uri) = self.GetPyData(item)
        if typ == "File":
            self._d_controller.DocumentOpen(uri)
        event.Skip()


    def OpenFile(self, evt=None):
        item = self.GetSelection()
        if not item: return
        (typ, uri) = self.GetPyData(item)
        if not typ == "File": return
        self._d_controller.DocumentOpen(uri)

    def DeleteFile(self, evt=None):
        item = self.GetSelection()
        if not item: return
        (typ, uri) = self.GetPyData(item)
        if not typ == "File": return
        try:
            self._d_controller.DocumentDelete(uri)
            self.removeURI(uri)
        except: pass            


    def NewFile(self, evt=None):
        self._d_controller.DocumentOpen("py://")
    
    def OpenArchive(self, evt=None):
        item = self.GetSelection()
        if not item: return
        (typ, uri) = self.GetPyData(item)
        if not typ=="Archive": return
        self.Expand(item)
    
