from Model import eDevModel
from Dialogs import eDevSaveAsDialog
from Dialogs import eDevDiscardDialog
import wx


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

    
    def OnArchiveSelected(self, event=None):
        self._d_main_frame.bindNew(self.OnArchiveFileNew)
        self._d_main_frame.bindDelete(self.OnArchiveDelete)
        self._d_main_frame.bindOpen()

    def OnArchiveFileSelected(self, event=None):
        self._d_main_frame.bindNew()
        self._d_main_frame.bindDelete(self.OnArchiveFileDelete)
        self._d_main_frame.bindOpen(self.OnArchiveFileOpen)



    def OnArchiveDelete(self, event=None):
        pass



    def OnArchiveFileOpen(self, event=None):
        item = self._d_archive_tree.GetSelection()
        
        if not item: return
        if None is self._d_archive_tree.GetPyData(item): return
        
        (typ, filename) = self._d_archive_tree.GetPyData(item)
        if not typ is "File": return
        (tmp, archive_name) = self._d_archive_tree.GetPyData(self._d_archive_tree.GetItemParent(item))

        idx = self._d_notebook.getPageNo( (archive_name, filename) )
        if idx >= 0:
            self._d_notebook.SetSelection(idx)
            return 

        ar = self._d_model.getArchive(archive_name)
        text = ar.readFile(filename)
        self._d_notebook.openEditor(filename, (archive_name, filename), text)
        self._d_main_frame.bindClose(self.OnDocumentClose)


    def OnArchiveFileNew(self, event=None):
        item = self._d_archive_tree.GetSelection()
        
        if not item: return
        if None is self._d_archive_tree.GetPyData(item): return
        
        (typ, archive_name) = self._d_archive_tree.GetPyData(item)
        if typ is "File": return

        self._d_notebook.openEditor("Unsaved", (archive_name, None), "")
        self._d_main_frame.bindClose(self.OnDocumentClose)
        #self._d_main_frame.


    def OnArchiveFileDelete(self, event=None):
        item = self._d_archive_tree.GetSelection()
        if not item: return;
        if None is self._d_archive_tree.GetPyData(item): return

        (typ, fname) = self._d_archive_tree.GetPyData(item)
        if not typ is "File": return
        (tmp, archive_name) = self._d_archive_tree.GetPyData(self._d_archive_tree.GetItemParent(item))

        ar = self._d_model.getArchive(archive_name)
        ar.deleteFile(fname)
        self._d_notebook.closePage(self._d_notebook.getPageNo((archive_name, fname)))
        self._d_archive_tree.removeFile()
       


    def OnDocumentClose(self, event=None):
        doc = self._d_notebook.GetCurrentPage()
        if doc is None:
            raise Exception("No document selected to save")

        if doc.isModified():
            # Ask for saveing
            dlg = eDevDiscardDialog(self._d_main_frame, -1)
            ret = dlg.ShowModal()
            # if cancel was clicked -> abort
            if ret == wx.ID_CANCEL: return
            # if Yes was clicked -> close and return
            if ret == wx.ID_YES:
                self._d_notebook.closePage()
                return
            
        (archive, filename) = doc.getData()
        if filename is None:
            self._d_notebook.closePage()
        else:
            self._d_notebook.closePage()


    def OnDocumentSave(self, event=None):
        # get the current selected document-page:
        doc = self._d_notebook.GetCurrentPage()
        if doc is None:
            raise Exception("No document selected to be save!")
        
        # FIXME Switch types
        if doc.isModified():
            # get text, archive and filename
            data = doc.GetText()
            (archive, fname) = doc.getData()
            ar = self._d_model.getArchive(archive)
            # check if archive is writeable:
            if not ar.isWriteable():
                raise Exception("Archive %s is not writable!"%archive)
            # write text to archive               
            ar.writeFile(fname, data)
        
        # reset "modified" flag of document-page 
        doc.setModified(False)
        # and disable save buttons            
        self._d_main_frame.bindSave()
            
    
    def OnDocumentSaveAs(self, event=None):
        doc = self._d_notebook.GetCurrentPage()
        if doc is None:
            raise Exception("No document selected to be saved!")
        # FIXME type specific handleing
        (archive, filename) = doc.getData()
        file_selected = False
        
        while not file_selected:
            dlg = eDevSaveAsDialog(self._d_main_frame, -1, archive)
            if not dlg.ShowModal() == wx.ID_OK: return 
            (archive, filename) = dlg.getSelection()
            ar = self._d_model.getArchive(archive)
            dlg.Destroy()

            if filename in ar.getFileList():
                dlg = eDevOverwriteDialog()
                ret = dlg.ShowModal()
                if ret == wx.ID_OK: file_selced=True
                elif ret == wx.ID_CANCEL: return
                dlg.Destroy()
            else: file_selected = True               
        
        if filename in ar.getFileList():
            ar.writeFile(filename, doc.GetText())
            self._d_notebook.SetPageText(doc, filename)
            doc.setData( (archive, filename) )
            doc.setModified(False)
        else:
            ar.createFile(filename, doc.GetText())
            self._d_notebook.SetPageText(doc, filename)
            doc.setData( (archive, filename) )
            self._d_archive_tree.addFile(archive, filename)
            doc.setModified(False)


    def OnDocumentModified(self, event=None):
        print "page modified"
        pg = self._d_notebook.GetCurrentPage()
        (arc, fname) = pg.getData()
        if not fname is None:
            self._d_main_frame.bindSave(self.OnDocumentSave)
        if self._d_notebook.isPageCanUndo():
            self._d_main_frame.bindUndo(self._d_notebook.OnPageUndo)
        if self._d_notebook.isPageCanRedo():
            self._d_main_frame.bindRedo(self._d_notebook.OnPageRedo)

        if self._d_notebook.isPageCanCopy():
            self._d_main_frame.bindCopy(self._d_notebook.OnPageCopy)
        if self._d_notebook.isPageCanCut():
            self._d_main_frame.bindCut(self._d_notebook.OnPageCut)
        if self._d_notebook.isPageCanPaste():
            self._d_main_frame.bindPaste(self._d_notebook.OnPagePaste)



    def OnDocumentChanged(self, event=None):
        print "page changed"
        # disable all editor-tools:
        self._d_main_frame.bindSave()
        self._d_main_frame.bindSaveAs()
        self._d_main_frame.bindCopy()
        self._d_main_frame.bindCut()
        self._d_main_frame.bindPaste()
        self._d_main_frame.bindRedo()
        self._d_main_frame.bindUndo()
        self._d_main_frame.bindClose()

        if self._d_notebook.isPage():
            self._d_main_frame.bindClose(self.OnDocumentClose)
            self._d_main_frame.bindSaveAs(self.OnDocumentSaveAs)

        if self._d_notebook.isPageModified():
            (archive, filename) = self._d_notebook.GetCurrentPage().getData()
            if filename == None: return
            self._d_main_frame.bindSave(self.OnDocumentSave)

        if self._d_notebook.isPageCanCopy():
            self._d_main_frame.bindCopy(self._d_notebook.OnPageCopy)
        if self._d_notebook.isPageCanCut():
            self._d_main_frame.bindCut(self._d_notebook.OnPageCut)
        if self._d_notebook.isPageCanPaste():
            self._d_main_frame.bindPaste(self._d_notebook.OnPagePaste)

        if self._d_notebook.isPageCanUndo():
            self._d_main_frame.bindUndo(self._d_notebook.OnPageUndo)
        if self._d_notebook.isPageCanRedo():
            self._d_main_frame.bindRedo(self._d_notebook.OnPageRedo)
                
