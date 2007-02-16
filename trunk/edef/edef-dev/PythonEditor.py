import wx
import wx.stc as stc
import keyword
import Events
from EditorInterface import eDevEditorInterface
from Controller import eDevController
from Model import eDevModel
import Dialogs
import Tools

faces = { 'times': 'Courier',
          'mono' : 'Courier',
          'helv' : 'Courier',
          'other': 'Courier',
          'size' : 10,
          'size2': 8}



class eDevPythonEditor(stc.StyledTextCtrl, eDevEditorInterface):
    def __init__(self, parent, ID, uri, text=""):
        stc.StyledTextCtrl.__init__(self, parent, ID, style=0)
        eDevEditorInterface.__init__(self, False, uri)

        self._d_controller = eDevController()
        self._d_mainframe  = self._d_controller.getMainFrame()
        self._d_model      = eDevModel()
        self._d_archive_tree = self._d_controller.getArchiveTree()
        self._d_notebook    = self._d_controller.getNotebook()

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
   

    def OnModified(self, evt):
        self.setModified()
        event = Events.PageModifiedEvent(Events._event_page_modified, self.GetId())
        event.SetPage(self)
        self.GetEventHandler().ProcessEvent(event)
        self._updateMainFrame()
        #evt.Skip()

    
    def OnSelected(self, evt=None):
        self._updateMainFrame()
        

    def _updateMainFrame(self):
        self._d_mainframe.bindRedo()
        self._d_mainframe.bindUndo()
        self._d_mainframe.bindSave()
        self._d_mainframe.bindSaveAs()
        self._d_mainframe.bindCopy()
        self._d_mainframe.bindCut()
        self._d_mainframe.bindPaste()
        
        if self.CanRedo(): self._d_mainframe.bindRedo(self.OnRedo)
        if self.CanUndo(): self._d_mainframe.bindUndo(self.OnUndo)
        self._d_mainframe.bindCopy(self.OnCopy)
        self._d_mainframe.bindCut(self.OnCut)
        if self.CanPaste(): self._d_mainframe.bindPaste(self.OnPaste)

        self._d_mainframe.bindSaveAs(self.OnSaveAs)
        if self.isModified() and self.getURI()!="py://":
            self._d_mainframe.bindSave(self.OnSave)


    def OnSaveAs(self, evt=None):
        selected = False
        while not selected:
            dlg = Dialogs.eDevSaveAsDialog(self, -1)
            if dlg.ShowModal() != wx.ID_OK:
                return
            uri = "py://%s/%s"%dlg.getSelection()
            dlg.Destroy()
            if self._d_model.checkURI(uri):
                # FIXME Override?
                continue
            selected = True
        
        if not self._d_model.checkURI(uri):
            self._d_controller.DocumentSave(uri, self.GetText())
            self._d_archive_tree.addURI(uri)
        else:
            self._d_controller.DocumentSave(uri, self.GetText())
        self.setURI(uri)
        print "rename to "+uri
        self._d_notebook.setPageTitleByURI(uri,Tools.getPyFile(uri))


    def OnSave(self, evt=None):
        txt = self.GetText()
        try:
            self._d_controller.DocumentSave(self.getURI(),txt)
            self.setModified(False)
        finally:
            self._updateMainFrame()

    def OnCopy(self, evt=None):
        self.Copy()
        self._updateMainFrame()

    def OnCut(self, evt=None): self.Cut()
    def OnPaste(self, evt=None): self.Paste()
    def OnRedo(self, evt=None): self.Redo()
    def OnUndo(self, evt=None): self.Undo()
