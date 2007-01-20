import wx
import wx.stc as stc
import keyword
from Controller import eDevController
import sys

faces = { 'times': 'Times',
          'mono' : 'Courier',
          'helv' : 'Helvetica',
          'other': 'new century schoolbook',
          'size' : 12,
          'size2': 10}




class eDevNotebook(wx.Notebook):
    _d_pages = None

    def __init__(self, parent, ID):
        wx.Notebook.__init__(self, parent, ID)
        self._d_pages = {}
        self._d_controller = eDevController.instance()
  
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)

    
    def open_page(self, name, data=None):
        if data is None:
            new = True
            data = ""
        else:
            new = False

        if not name in self._d_pages.keys():
            page = wx.Panel(self, -1)#eDevEditPage(self, -1, data, new)
            self.AddPage(page, name, True)
            #self._d_pages[name]=page
  

    def close_page(self):
        print "try to close: %s"%self.GetSelection()
        try:
            self.DeletePage(self.GetSelection())
        except:
            print sys.print_exc()
    
    def OnPageChanged(self, event):
        self._d_controller.OnDocumentChanged()

    
    def isPage(self):
        if self.GetPageCount() > 0: return True
        return False

    def isPageModified(self):
        # returns False if the current page was saved so it is save to
        #   close this tab.
        page = self.GetCurrentPage()
        if page is None: return False
        return page.isModified()

    def isPageCanCopy(self):
        return False

    def isPageCanPaste(self):
        return False

    def isPageCanRedo(self):
        return False
    
    def isPageCanUndo(self):
        return True
            



class eDevEditPage(stc.StyledTextCtrl):
    _d_is_modified = None

    def __init__(self, parent, ID, data="", new=False):
        stc.StyledTextCtrl.__init__(self, parent, ID, style=0)

        self._d_is_modified = new

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

        
        self.SetText(data)
        self.EmptyUndoBuffer()
        self.Colourise(0, -1)

        self.Bind(stc.EVT_STC_MODIFIED, self.OnModified)
    
    
    def OnModified(self, evt):
        self._d_is_modified = True
        self._d_controller.OnDocumentModified()


    def isModified(self):
        return self._d_is_modified
    


