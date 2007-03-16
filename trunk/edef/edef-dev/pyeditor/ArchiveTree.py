import wx
import fnmatch
from edef.dev import Model, Controller
from edef.dev.NavigatorPanel import NavigatorPanel
from Tools import getArchive, getPyFile, isArchiveURI, isPyFileURI, splitPyFile
from edef.dev import Tools
from edef.dev import Dialogs
from icon_archive import getBitmap as getArchiveBitmap
from icon_python import getBitmap as getPythonBitmap



class ArchiveTreePanel(NavigatorPanel):
    def __init__(self, parent, ID):
        NavigatorPanel.__init__(self, parent, ID, "Archives")
        self._tree = ArchiveTree(self, -1)
        box = self.GetSizer()
        box.Add(self._tree,1,wx.EXPAND)

    def getArchiveTree(self): return self._tree



class ArchiveTree(wx.TreeCtrl):
    def __init__(self, parent, ID):
        wx.TreeCtrl.__init__(self, parent, ID, size=wx.Size(-1,-1),
                             style=wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT|wx.TR_NO_LINES|wx.TR_FULL_ROW_HIGHLIGHT)
        
        self._d_imgs = wx.ImageList(16,16)
        self._bmp_class = self._d_imgs.Add( getArchiveBitmap() )
        self._bmp_class_open = self._d_imgs.Add( getArchiveBitmap() )
        self._bmp_module = self._d_imgs.Add( getPythonBitmap() )
        self.SetImageList(self._d_imgs)

        self._d_model = Model()
        self._d_controller = Controller()
        self._d_mainframe = self._d_controller.getMainFrame()

        self._d_root = self.AddRoot("root")
        self.SetPyData(self._d_root, (None,None))
        self._logger = self._d_controller.getLogger()


        #Add all archives:
        archives = self._d_model.openURI("zip://")
        for archive_uri in archives:
            uri_list = self._d_model.openURI(archive_uri)
            archive_name = getArchive(archive_uri)
            arch_item = self.AppendItem(self._d_root, archive_name)
            self.SetPyData(arch_item, ("Archive", archive_uri) )
            self.SetItemImage(arch_item, self._bmp_class, wx.TreeItemIcon_Normal)
            self.SetItemImage(arch_item, self._bmp_class_open, wx.TreeItemIcon_Expanded)

            for file_uri in uri_list:
                file_name = getPyFile(file_uri)
                file_item = self.AppendItem(arch_item, file_name)
                self.SetPyData(file_item, ("File", file_uri))
                self.SetItemImage(file_item, self._bmp_module, wx.TreeItemIcon_Normal)
                self.SetItemImage(file_item, self._bmp_module, wx.TreeItemIcon_Expanded)
        
        # FIXME self._d_mainframe.bindNewArch(self.NewArchive)

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

        if isPyFileURI(uri):
            (ar, py) = splitPyFile(uri)
            item = self.getItemByURI("zip://"+ar, self._d_root)
            fitem = self.AppendItem(item, py)
            self.SetPyData(fitem, ("File", uri))
            self.SetItemImage(fitem, self._bmp_module, wx.TreeItemIcon_Normal)
            self.SetItemImage(fitem, self._bmp_module, wx.TreeItemIcon_Expanded)
        elif isArchiveURI(uri):
            path = getArchive(uri)
            item = self.AppendItem(self._d_root, path)
            self.SetPyData(item, ("Archive",uri))
            self.SetItemImage(item, self._bmp_class, wx.TreeItemIcon_Normal)
            self.SetItemImage(item, self._bmp_class_open, wx.TreeItemIcon_Expanded)
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
            self._d_mainframe.bindOpen(self.OpenFile, "&Open file")
            self._d_mainframe.bindDelete(self.DeleteFile, "&Delete file")
        elif typ is "Archive":
            self._d_mainframe.bindNew(self.NewFile, "&New file")
            self._d_mainframe.bindOpen(self.OpenArchive, "&Open archive")
            self._d_mainframe.bindDelete(self.DeleteArchive, "&Delete archive")
  

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
        if not item:
            self._logger.warning("No item selected to delete")
            return
        (typ, uri) = self.GetPyData(item)
        if not typ == "File": return
        try:
            self._d_controller.DocumentDelete(uri)
            self.removeURI(uri)
        except:
            self._logger.exception("Unable to remove file %s"%uri)


    def NewFile(self, evt=None):
        self._d_controller.DocumentOpen("zip://")
    
    def OpenArchive(self, evt=None):
        item = self.GetSelection()
        if not item: return
        (typ, uri) = self.GetPyData(item)
        if not typ=="Archive": return
        self.Expand(item)
   
    def NewArchive(self, evt=None):
        selected = False
        while not selected:
            dlg = Dialogs.eDevNewArchiveDialog(self, -1)
            if dlg.ShowModal() == wx.ID_CANCEL: return
            uri = dlg.getSelection()
            dlg.Destroy()

            if self._d_model.checkURI(uri):
                # FIXME ask for overwrite
                continue
            selected = True
        self._d_model.saveURI(uri,"")
        self.addURI(uri)

    def DeleteArchive(self, evt=None):
        item = self.GetSelection()
        (typ, uri) = self.GetPyData(item)

        py_list = self._d_model.openURI(uri)
        for py in py_list:
           self._d_controller.DocumentDelete(py)
        self._d_model.deleteURI(uri)
        self.Delete(item)
