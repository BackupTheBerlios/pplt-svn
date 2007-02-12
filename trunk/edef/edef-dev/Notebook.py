import wx
import wx.stc as stc
import keyword
from Controller import eDevController
import sys
import traceback

faces = { 'times': 'Courier',
          'mono' : 'Courier',
          'helv' : 'Courier',
          'other': 'Courier',
          'size' : 10,
          'size2': 8}




class eDevNotebook(wx.Notebook):
    _d_pages = None

    def __init__(self, parent, ID):
        wx.Notebook.__init__(self, parent, ID)
        self._d_pages = {}
        self._d_controller = eDevController.instance()
  
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)

    
    def openEditor(self, title, data, text=None):
        page = eDevEditPage(self, -1, data, text)
        self.AddPage(page, title, True)
        self._d_controller.OnDocumentChanged()


    def closePage(self, idx=None):
        if idx is None: pos = self.GetSelection()
        else: pos = idx
        
        if pos < 0: return

        if pos == self.GetSelection():
            self.DeletePage(pos)
            self._d_controller.OnDocumentChanged()
        else:
            self.DeletePage(pos)
    

    def getPageNo(self, data):
        for n in range(self.GetPageCount()):
            if self.GetPage(n).getData() == data:
                return n
        return -1

    def hasPage(self, data):
        if self.getPageNo(data) > 0:
            return True
        return False                

    def selectPage(self, data):
        self.SetSelection(self.getPageNo(data))

    def OnPageChanged(self, event):
        self._d_controller.OnDocumentChanged()
    
    def isPage(self):
        if self.GetPageCount() > 0: return True
        return False

    def isPageModified(self, idx=None):
        if idx is None: page = self.GetCurrentPage()
        else: page = self.GetPage(idx)
        if page is None: return False
        return page.isModified()

    def isPageCanCopy(self):
        return False

    def isPageCanPaste(self):
        return False

    def isPageCanRedo(self, idx=None):
        if idx is None: page = self.GetCurrentPage()
        else: page = self.GetPage(idx)
        if page is None: return False
        return page.canRedo()

    def isPageCanUndo(self, idx=None):
        if idx is None: page = self.GetCurrentPage()
        else: page = self.GetPage(idx)
        if page is None: return False
        return page.canUndo()

    def isPageCanCopy(self, idx=None):
        if idx is None: page = self.GetCurrentPage()
        else: page = self.GetPage(idx)
        if page is None: return False
        return page.canCopy()

    def isPageCanCut(self, idx=None):
        if idx is None: page = self.GetCurrentPage()
        else: page = self.GetPage(idx)
        if page is None: return False
        return page.canCut()

    def isPageCanPaste(self, idx=None):
        if idx is None: page = self.GetCurrentPage()
        else: page = self.GetPage(idx)
        if page is None: return False
        return page.canPaste()
    
    def OnPageUndo(self, evt=None):
        self.GetCurrentPage().undo()
    def OnPageRedo(self, evt=None):
        self.GetCurrentPage().redo()
    def OnPageCopy(self, evt=None):
        self.GetCurrentPage().copy()
    def OnPageCut(self, evt=None):
        self.GetCurrentPage().cut()
    def OnPagePaste(self, evt=None):
        self.GetCurrentPage().paste()
        


class eDevEditPage(stc.StyledTextCtrl):
    _d_is_modified = None
    _d_data = None

    def __init__(self, parent, ID, data, text=""):
        stc.StyledTextCtrl.__init__(self, parent, ID, style=0)
        self._d_data = data
        self._d_controller = eDevController.instance()

        self.SetLexer(stc.STC_LEX_PYTHON)
        self.SetKeyWords(0, " ".join(keyword.kwlist))
        
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT,     "face:%(helv)s,size:%(size)d" % faces)
        self.StyleClearAll()  # Reset all to be like the default
        
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT,     "face:%(helv)s,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER,  "back:#C0C0C0,face:%(helv)s,size:%(size2)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, "face:%(other)s" % faces)
        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT,  "fore:#FFFFFF,back:#0000FF,bold")
        self.StyleSetSpec(stc.STC_STYLE_BRACEBAD,    "fore:#000000,back:#FF0000,bold")

        self.StyleSetSpec(stc.STC_P_DEFAULT, "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_P_COMMENTLINE, "fore:#007F00,face:%(other)s,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_P_NUMBER, "fore:#007F7F,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_P_STRING, "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_P_CHARACTER, "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_P_WORD, "fore:#00007F,bold,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_P_TRIPLE, "fore:#7F0000,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "fore:#7F0000,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_P_CLASSNAME, "fore:#0000FF,bold,underline,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_P_DEFNAME, "fore:#007F7F,bold,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_P_OPERATOR, "bold,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_P_IDENTIFIER, "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_P_COMMENTBLOCK, "fore:#7F7F7F,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_P_STRINGEOL, "fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % faces)
        self.SetCaretForeground("BLUE")

        
        self.SetText(text)
        self.EmptyUndoBuffer()
        self.Colourise(0, -1)

        self.Bind(stc.EVT_STC_CHANGE, self.OnModified)
    
    def getData(self):
        return self._d_data
    def setData(self, data):
        self._d_data = data

    def OnModified(self, evt):
        self.setModified()

    def isModified(self):
        return self._d_is_modified

    def canRedo(self): return self.CanRedo()
    def canUndo(self): return self.CanUndo()
    def canCopy(self): return True
    def canCut(self):  return True
    def canPaste(self): return self.CanPaste()

    def redo(self, evt=None): self.Redo()
    def undo(self, evt=None): self.Undo()

    def copy(self, evt=None):
        self._d_controller.OnDocumentChanged()
        self.Copy()
    
    def cut(self, evt=None): self.Cut()
    def paste(self, evt=None): self.Paste()

    def setModified(self, mod=True):
        self._d_is_modified = mod
        if mod == True:
            self._d_controller.OnDocumentModified()


