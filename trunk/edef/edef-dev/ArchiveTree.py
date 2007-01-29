import wx
from Model import eDevModel
import fnmatch
from Controller import eDevController

class eDevArchiveTree(wx.TreeCtrl):
    

    def __init__(self, parent, ID):
        wx.TreeCtrl.__init__(self, parent, ID, size=wx.Size(-1,-1),
                             style=wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT|wx.TR_NO_LINES|wx.TR_FULL_ROW_HIGHLIGHT)
        
        self._d_model = eDevModel.instance()
        self._d_controller = eDevController.instance()

        self._d_root = self.AddRoot("root")
        self.SetPyData(self._d_root, None)

        #Add all archives:
        archives = self._d_model.getArchives()
        for archive_name in archives:
            archive = self._d_model.getArchive(archive_name)
            arch_item = self.AppendItem(self._d_root, archive_name)
            self.SetPyData(arch_item, ("Archive",archive_name))

            for file_name in archive.getFileList("*.py"):
                file_item = self.AppendItem(arch_item, file_name)
                self.SetPyData(file_item, ("File", file_name))

        # Events:
        #self.Bind(wx.EVT_LEFT_DCLICK, self.OnOpen)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelection)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivate)



    def OnSelection(self, event):
        item = event.GetItem()
        
        if self.GetPyData(item) is None: return
        (typ, name) = self.GetPyData(item)
            
        if typ is "File":
            self._d_controller.OnArchiveFileSelected()
        elif typ is "Archive":
            self._d_controller.OnArchiveSelected()
        else:
            self._d_controller.OnArchiveDeselected()


    def OnActivate(self, event):
        self._d_controller.OnArchiveFileOpen()
    

    def removeFile(self):
        item = self.GetSelection()
        if item is None:
            raise Exception("No item selected to remove!")
        self.Delete(item)


    def addFile(self, archive_name, filename):
        item = self.getItemByData( ("Archive", archive_name), self.GetRootItem() )
        if not item:
            raise Exception("There is no archive named %s"%archive_name)
        file_item = self.AppendItem(item, filename)
        self.SetPyData(file_item, ("File", filename))


    def getItemByData(self, data, item):
        if self.GetPyData(item) == data: return item
        (citem, cookie) = self.GetFirstChild(item)
        
        while citem:
            ret = self.getItemByData(data, citem)
            if ret != None: return ret
            (citem, cookie) = self.GetNextChild(item,cookie)
                    
