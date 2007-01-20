from Model import eDevModel



class eDevController:
    _d_instance = None

    def instance():
        if eDevController._d_instance is None:
            eDevController._d_instance = eDevController()
        return eDevController._d_instance
    instance = staticmethod(instance)



    def __init__(self):
        self._d_notebook = None
        self._d_archive_tree = None
        self._d_main_frame = None
        self._d_model = eDevModel.instance()



    def getNotebook(self):
        return self._d_notebook
    def setNotebook(self, nb):
        self._d_notebook = nb

    def getArchiveTree(self):
        return self._d_archive_tree
    def setArchiveTree(self, t):
        self._d_archive_tree = t

    def getMainFrame(self):
        return self._d_main_frame
    def setMainFrame(self, frm):
        self._d_main_frame = frm


    def OnArchiveFileOpen(self, event=None):
        item = self._d_archive_tree.GetSelection()
        
        if not item: return
        if None is self._d_archive_tree.GetPyData(item): return
        
        (typ, filename) = self._d_archive_tree.GetPyData(item)
        if not typ is "File": return
        (tmp, archive_name) = self._d_archive_tree.GetPyData(self._d_archive_tree.GetItemParent(item))

        ar = self._d_model.getArchive(archive_name)
        data = ar.getFileContent(filename)
        self._d_notebook.open_page(filename, data)
        self._d_main_frame.bindClose(self.OnDocumentClose)

    def OnArchiveFileNew(self, event=None):
        pass

    def OnArchiveFileDelete(self, event=None):
        pass





    def OnArchiveFileSelected(self, event=None):
        self._d_main_frame.bindNew()
        self._d_main_frame.bindDelete(self.OnArchiveFileDelete)
        self._d_main_frame.bindOpen(self.OnArchiveFileOpen)

    def OnArchiveSelected(self, event=None):
        self._d_main_frame.bindNew(self.OnArchiveFileNew)
        self._d_main_frame.bindDelete()
        self._d_main_frame.bindOpen()

    def OnDocumentClose(self, event=None):
        #FIXME if document is modified: ask for saveing!
        self._d_notebook.close_page()

    def OnDocumentChanged(self, event=None):
        print "Document Changed!" 
