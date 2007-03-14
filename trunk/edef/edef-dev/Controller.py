from Model import eDevModel
from Dialogs import eDevDiscardDialog, showExceptionDialog
from NavigatorPanel import NavigatorPanel
import wx
from edef import Singleton
import Tools
import logging


class eDevController:

    __metaclass__ = Singleton
    def __init__(self):
        self._d_notebook = None
        self._d_main_frame = None
        self._d_model = eDevModel()
        self._navigator = None
        self._editors = dict()
        self._logger = logging.getLogger("edef.dev")

    def getNotebook(self):
        return self._d_notebook
    def setNotebook(self, nb):
        self._d_notebook = nb
    def getMainFrame(self):
        return self._d_main_frame
    def setMainFrame(self, frm):
        self._d_main_frame = frm
    def getNavigator(self):
        return self._navigator
    def setNavigator(self, nav):
        self._navigator = nav
    def getLogger(self):
        return self._logger


    def registerEditorClass(self, proto, edit_class):
        self._d_notebook.registerEditorClass( proto, edit_class )
    
    def addNavigatorClass(self, navic):
        navi = navic(self._navigator, -1)
        if not isinstance(navi, NavigatorPanel):
            raise Exception("Invalid navigator panel! Not an instance of 'NavigatorPanel'")
        self._navigator.addNavigatorPanel(navi)
        return navi


    def DocumentOpen(self, uri):
        (proto, path) = Tools.splitURI(uri)
            
        if self._d_notebook.hasPageURI( uri ):
            self._d_notebook.selectPageByURI( uri )
            return 
        
        try:
            self._d_notebook.openURI(uri)
            self._d_main_frame.bindClose(self.OnDocumentClose)
        except:
            showExceptionDialog(self._d_notebook, -1,
                                "Unable to open document %s"%uri)


    def DocumentDelete(self, uri):
        # Ask for delete
        dlg = wx.MessageDialog(self._d_main_frame, "Do you realy wan to delete %s?"%uri,
                                "delete?", wx.YES|wx.NO)
        if dlg.ShowModal() == wx.ID_NO:
            raise Exception("Delete aborted")
        
        # delete
        try:
            self._d_model.deleteURI( uri )
            if self._d_notebook.hasPageURI( uri ):
                self._d_notebook.closePage( self._d_notebook.getPageByURI( uri ) )
        except:
            showExceptionDialog(self._d_notbook, -1,
                                "Unable to delete document %s"%uri)
            raise Exception("Delete aborted")
        

    def DocumentClose(self):
        # FIXME this should be handled by an editor
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
