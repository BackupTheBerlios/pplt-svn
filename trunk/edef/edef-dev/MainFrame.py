import wx
from MainSplitter import eDevMainSplitter
from Navigator import eDevNavigator
from Notebook import eDevNotebook
from Controller import eDevController



class eDevMainFrame(wx.Frame):
    
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title,
                          size=(640,480))
        
        new_bmp = wx.ArtProvider_GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, (16,16))
        open_bmp = wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, (16,16))
        del_bmp = wx.ArtProvider_GetBitmap(wx.ART_DELETE, wx.ART_TOOLBAR, (16,16))
        save_bmp = wx.ArtProvider_GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, (16,16))
        save_as_bmp = wx.ArtProvider_GetBitmap(wx.ART_FILE_SAVE_AS, wx.ART_TOOLBAR, (16,16))
        close_bmp = wx.ArtProvider_GetBitmap(wx.ART_CROSS_MARK, wx.ART_TOOLBAR, (16,16))
        copy_bmp = wx.ArtProvider_GetBitmap(wx.ART_COPY, wx.ART_TOOLBAR, (16,16))
        cut_bmp = wx.ArtProvider_GetBitmap(wx.ART_CUT, wx.ART_TOOLBAR, (16,16))
        paste_bmp = wx.ArtProvider_GetBitmap(wx.ART_PASTE, wx.ART_TOOLBAR, (16,16))
        redo_bmp = wx.ArtProvider_GetBitmap(wx.ART_REDO, wx.ART_TOOLBAR, (16,16))
        undo_bmp = wx.ArtProvider_GetBitmap(wx.ART_UNDO, wx.ART_TOOLBAR, (16,16))
        quit_bmp = wx.ArtProvider_GetBitmap(wx.ART_QUIT, wx.ART_TOOLBAR, (16,16))
        about_bmp = wx.ArtProvider_GetBitmap(wx.ART_INFORMATION, wx.ART_TOOLBAR, (16,16))
        conf_bmp = wx.ArtProvider_GetBitmap(wx.ART_HELP_SETTINGS, wx.ART_TOOLBAR, (16,16))

        # Assemble Menu
        self._d_menubar = wx.MenuBar()
        self._d_file_menu    = wx.Menu()
        self._d_edit_menu    = wx.Menu()
        self._d_settings_menu= wx.Menu()
        self._d_help_menu    = wx.Menu()
        
        # create items:
        self._d_menu_new     = wx.MenuItem(self._d_file_menu, wx.ID_NEW, "&New", "???")
        self._d_menu_open    = wx.MenuItem(self._d_file_menu, wx.ID_OPEN, "&Open", "???")
        self._d_menu_save    = wx.MenuItem(self._d_file_menu, wx.ID_SAVE, "&Save", "???")
        self._d_menu_save_as = wx.MenuItem(self._d_file_menu, wx.ID_SAVEAS, "Save &as...", "???")
        self._d_menu_delete  = wx.MenuItem(self._d_file_menu, wx.ID_DELETE, "&Delete", "???")
        self._d_menu_quit    = wx.MenuItem(self._d_file_menu, wx.ID_EXIT, "&Quit", "???")
       
        self._d_menu_copy    = wx.MenuItem(self._d_edit_menu, wx.ID_COPY, "&Copy", "???")
        self._d_menu_cut     = wx.MenuItem(self._d_edit_menu, wx.ID_CUT, "Cut", "???")
        self._d_menu_paste   = wx.MenuItem(self._d_edit_menu, wx.ID_PASTE, "&Paste", "???")
        self._d_edit_menu.AppendSeparator()
        self._d_menu_redo    = wx.MenuItem(self._d_edit_menu, wx.ID_REDO, "&Redo", "???")
        self._d_menu_undo    = wx.MenuItem(self._d_edit_menu, wx.ID_UNDO, "&Undo", "???")

        self._d_menu_conf_editor = wx.MenuItem(self._d_settings_menu, wx.ID_PREFERENCES, "&Editor", "???")
        self._d_menu_about   = wx.MenuItem(self._d_help_menu, wx.ID_HELP, "&About", "About edef Developer")

        # Set Menuicons:
        self._d_menu_new.SetBitmap(new_bmp)
        self._d_menu_open.SetBitmap(open_bmp)
        self._d_menu_save.SetBitmap(save_bmp)
        self._d_menu_save_as.SetBitmap(save_as_bmp)
        self._d_menu_delete.SetBitmap(del_bmp)
        self._d_menu_quit.SetBitmap(quit_bmp)
        self._d_menu_copy.SetBitmap(copy_bmp)
        self._d_menu_cut.SetBitmap(cut_bmp)
        self._d_menu_paste.SetBitmap(paste_bmp)
        self._d_menu_redo.SetBitmap(redo_bmp)
        self._d_menu_undo.SetBitmap(undo_bmp)
        self._d_menu_about.SetBitmap(about_bmp)

        # Add Items:
        self._d_file_menu.AppendItem(self._d_menu_new)
        self._d_file_menu.AppendItem(self._d_menu_open)
        self._d_file_menu.AppendItem(self._d_menu_save)
        self._d_file_menu.AppendItem(self._d_menu_save_as)
        self._d_file_menu.AppendItem(self._d_menu_delete)
        self._d_file_menu.AppendSeparator()
        self._d_file_menu.AppendItem(self._d_menu_quit)
        self._d_edit_menu.AppendItem(self._d_menu_copy)
        self._d_edit_menu.AppendItem(self._d_menu_cut)
        self._d_edit_menu.AppendItem(self._d_menu_paste)
        self._d_edit_menu.AppendSeparator()
        self._d_edit_menu.AppendItem(self._d_menu_redo)
        self._d_edit_menu.AppendItem(self._d_menu_undo)
        self._d_settings_menu.AppendItem(self._d_menu_conf_editor)
        self._d_help_menu.AppendItem(self._d_menu_about)

        #assemble menu-bar
        self._d_menubar.Append(self._d_file_menu, "&File")
        self._d_menubar.Append(self._d_edit_menu, "&Edit")
        self._d_menubar.Append(self._d_settings_menu, "&Settings")
        self._d_menubar.Append(self._d_help_menu, "&Help")
        self.SetMenuBar(self._d_menubar)

 
        # Assemble Toolbar:
        self._d_toolbar = self.CreateToolBar()
        self._d_toolbar.SetToolBitmapSize((16,16))
        self._d_toolbar.AddSimpleTool(wx.ID_NEW, new_bmp, "New")
        self._d_toolbar.AddSimpleTool(wx.ID_OPEN, open_bmp, "Open")
        self._d_toolbar.AddSimpleTool(wx.ID_DELETE, del_bmp, "Delete")
        self._d_toolbar.AddSeparator()
        self._d_toolbar.AddSimpleTool(wx.ID_SAVE, save_bmp, "Save")
        self._d_toolbar.AddSimpleTool(wx.ID_SAVEAS, save_as_bmp, "Save as...")
        self._d_toolbar.AddSimpleTool(wx.ID_CLOSE, close_bmp, "Close")
        self._d_toolbar.AddSeparator()
        self._d_toolbar.AddSimpleTool(wx.ID_COPY, copy_bmp, "Copy")
        self._d_toolbar.AddSimpleTool(wx.ID_CUT, cut_bmp, "Cut")
        self._d_toolbar.AddSimpleTool(wx.ID_PASTE, paste_bmp, "Paste")
        self._d_toolbar.AddSeparator()
        self._d_toolbar.AddSimpleTool(wx.ID_REDO, redo_bmp, "Redo")
        self._d_toolbar.AddSimpleTool(wx.ID_UNDO, undo_bmp, "Undo")
        

        self._d_controller = eDevController.instance()
        self._d_controller.setMainFrame(self)

        # status-bar:
        self.CreateStatusBar()

        # add splitter window:
        self._d_splitter = eDevMainSplitter(self, -1)
        self._d_navigator = eDevNavigator(self._d_splitter, -1)
        self._d_notebook = eDevNotebook(self._d_splitter, -1)
        self._d_controller.setNotebook(self._d_notebook)

        self._d_splitter.SplitVertically(self._d_navigator, self._d_notebook)
        self._d_splitter.SetSashPosition(180, True)
        self._d_splitter.SizeWindows()

        # connect events:
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        self.bindNew()
        self.bindOpen()
        self.bindDelete()
        self.bindSave()
        self.bindSaveAs()
        self.bindClose()


    def OnExit(self, evt):
        self.Close()


    def bindNew(self, cb=None):
        if cb is None:
            self._d_toolbar.EnableTool(wx.ID_NEW, False)
            self._d_menu_new.Enable(False)
        else:
            self.Bind(wx.EVT_MENU, cb, id=wx.ID_NEW)
            self.Bind(wx.EVT_TOOL, cb, id=wx.ID_NEW)
            self._d_toolbar.EnableTool(wx.ID_NEW, True)
            self._d_menu_new.Enable(True)

    def bindOpen(self, cb=None):
        if cb is None:
            self._d_toolbar.EnableTool(wx.ID_OPEN, False)
            self._d_menu_open.Enable(False)
        else:
            self.Bind(wx.EVT_MENU, cb, id=wx.ID_OPEN)
            self.Bind(wx.EVT_TOOL, cb, id=wx.ID_OPEN)
            self._d_toolbar.EnableTool(wx.ID_OPEN, True)
            self._d_menu_open.Enable(True)

    def bindDelete(self, cb=None):
        if cb is None:
            self._d_toolbar.EnableTool(wx.ID_DELETE, False)
            self._d_menu_delete.Enable(False)
        else:
            self.Bind(wx.EVT_MENU, cb, id=wx.ID_DELETE)
            self.Bind(wx.EVT_TOOL, cb, id=wx.ID_DELETE)
            self._d_toolbar.EnableTool(wx.ID_DELETE, True)
            self._d_menu_delete.Enable(True)

    def bindSave(self, cb=None):
        if cb is None:
            self._d_toolbar.EnableTool(wx.ID_SAVE, False)
            self._d_menu_save.Enable(False)
        else:
            self.Bind(wx.EVT_MENU, cb, id=wx.ID_SAVE)
            self.Bind(wx.EVT_TOOL, cb, id=wx.ID_SAVE)
            self._d_toolbar.EnableTool(wx.ID_SAVE, True)
            self._d_menu_save.Enable(True)

    def bindSaveAs(self, cb=None):
        if cb is None:
            self._d_toolbar.EnableTool(wx.ID_SAVEAS, False)
            self._d_menu_save_as.Enable(False)
        else:
            self.Bind(wx.EVT_MENU, cb, id=wx.ID_SAVEAS)
            self.Bind(wx.EVT_TOOL, cb, id=wx.ID_SAVEAS)
            self._d_toolbar.EnableTool(wx.ID_SAVEAS, True)
            self._d_menu_save_as.Enable(True)

    def bindClose(self, cb=None):
        if cb is None:
            self._d_toolbar.EnableTool(wx.ID_CLOSE, False)
        else:
            self.Bind(wx.EVT_TOOL, cb, id=wx.ID_CLOSE)
            self._d_toolbar.EnableTool(wx.ID_CLOSE, True)

    

