from Model import eDevModel
from Dialogs import eDevSaveAsDialog
from Dialogs import eDevDiscardDialog
import wx
from edef import Singleton
import Tools


class eDevController:

    __metaclass__ = Singleton
    def __init__(self):
        self._d_notebook = None
        self._d_archive_tree = None
        self._d_module_tree = None
        self._d_main_frame = None
        self._d_model = eDevModel()

    def getNotebook(self):
        return self._d_notebook
    def setNotebook(self, nb):
        self._d_notebook = nb
    def getArchiveTree(self):
        return self._d_archive_tree
    def setArchiveTree(self, t):
        self._d_archive_tree = t
    def setModuleTree(self, t):
        self._d_module_tree = t
    def getModuleTree(self):
        return self._d_module_tree
    def getMainFrame(self):
        return self._d_main_frame
    def setMainFrame(self, frm):
        self._d_main_frame = frm

   
    def DocumentOpen(self, uri):
        (proto, path) = Tools.splitURI(uri)
            
        if self._d_notebook.hasPageURI( uri ):
            self._d_notebook.selectPageByURI( uri )
            return 
        
        if path == "" and proto == "py":
            self._d_notebook.openEditor("Unsaved", uri, "")
        elif path == "" and proto == "mod":
            self._d_notebook.openModule("Unsaved", uri, "")

        elif proto == "py":
            text = self._d_model.openURI(uri)
            filename = Tools.getPyFile(uri)
            self._d_notebook.openEditor(filename, uri, text)
        elif proto == "mod":
            text = self._d_model.openURI(uri)
            mod_name = Tools.getModule(uri)
            self._d_notebook.openModule(mod_name, uri,text)
        else: return
        self._d_main_frame.bindClose(self.OnDocumentClose)


    def DocumentDelete(self, uri):
        # Ask for delete
        dlg = wx.MessageDialog(self._d_main_frame, "Do you realy wan to delete %s?"%uri,
                                "delete?", wx.YES|wx.NO)
        if dlg.ShowModal() == wx.ID_NO:
            raise Exception("Delete aborted")
        # delete
        self._d_model.deleteURI( uri )
        if self._d_notebook.hasPageURI( uri ):
            self._d_notebook.closePage( self._d_notebook.getPageByURI( uri ) )


    def DocumentClose(self):
        doc = self._d_notebook.GetCurrentPage()
        if doc is None: None

        if doc.isModified():
            # Ask for saveing
            dlg = eDevDiscardDialog(self._d_main_frame, -1)
            ret = dlg.ShowModal()
            # if cancel was clicked -> abort
            if ret == wx.ID_CANCEL: return
            # if Yes was clicked -> close and return
        self._d_notebook.closePage()
        if not self._d_notebook.GetCurrentPage():
            self._d_main_frame.bindClose()


    def DocumentSave(self, uri, txt=None):
        self._d_model.saveURI(uri, txt)



    #
    # Evt Handler:
    #
    def OnDocumentClose(self, evt): self.DocumentClose()
