import wx
import sys
import traceback

import Events
from Controller import eDevController
from pyeditor.PythonEditor import eDevPythonEditor
from modeditor.ModuleEditor import eDevModuleEditor
from Shell import eDevShell #FIXME shell.Shell


class eDevNotebook(wx.Notebook):

    def __init__(self, parent, ID):
        wx.Notebook.__init__(self, parent, ID)
        
        self._d_controller = eDevController()
        self._d_mainframe  = self._d_controller.getMainFrame()

        #self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self._onPageChanged)
    
    def _onPageChanged(self, evt):
        page = self._getSelectedPage()
        if page: page.OnSelected()
        self._emmitChanged()
        evt.Skip()

    def _onPageModified(self, evt):
        self._emmitModified(evt.GetPage())
        evt.Skip()

    def _getSelectedPage(self):
        sel = self.GetSelection()
        if sel < 0: return None
        return self.GetPage(sel)

    def _emmitModified(self, page=None):
        if page == None: page = self._getSelectedPage()
        event = Events.PageModifiedEvent(Events._event_page_modified,
                                         self.GetId())
        event.SetPage(page)
        self.GetEventHandler().ProcessEvent(event)

    def _emmitChanged(self, page=None):
        if page == None: page = self._getSelectedPage()
        event = Events.PageChangedEvent(Events._event_page_changed,
                                        self.GetId())
        event.SetPage(page)
        self.GetEventHandler().ProcessEvent(event)
        

    def openEditor(self, title, uri, text=None):
        page = eDevPythonEditor(self, -1, uri, text)
        self.AddPage(page, title, True)
        self.Bind(Events.EVT_PAGE_MODIFIED, self._onPageModified, page)
        self._emmitChanged(page)


    def openModule(self, title, uri, text=None):
        page = eDevModuleEditor(self, -1, uri, text)
        self.AddPage(page, title, True)
        self.Bind(Events.EVT_PAGE_MODIFIED, self._onPageModified, page)
        self._emmitChanged(page)


    def openShell(self, title, uri, text=None):
        page = eDevShell(self, -1, uri, text)
        self.AddPage(page, title, True)
        self._emmitChanged(page)


    def closePage(self, idx=None):
        if idx is None: pos = self.GetSelection()
        else: pos = idx
        if pos < 0: return
        if pos == self.GetSelection():
            self.DeletePage(pos)
            self._emmitChanged()
        else:
            self.DeletePage(pos)
        
        if not self.isPage():
            self._d_mainframe.bindSave()
            self._d_mainframe.bindSaveAs()
            self._d_mainframe.bindCopy()
            self._d_mainframe.bindCut()
            self._d_mainframe.bindPaste()
            self._d_mainframe.bindRedo()
            self._d_mainframe.bindUndo()

    def getPageByURI(self, uri):
        for n in range(self.GetPageCount()):
            if self.GetPage(n).getURI() == uri:
                return n
        return -1

    def hasPageURI(self, uri):
        if self.getPageByURI(uri) >= 0: return True
        return False

    def selectPageByURI(self, uri):
        if self.hasPageURI(uri):
            self.SetSelection(self.getPageByURI(uri))
   
    def isPage(self):
        if self.GetPageCount() > 0: return True
        return False

    def setPageTitleByURI(self, uri, title):
        page = self.getPageByURI(uri)
        self.SetPageText(page, title)
