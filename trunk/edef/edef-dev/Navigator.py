import wx
import wx.lib.foldpanelbar as fpb
from ArchiveTree import eDevArchiveTree
from Controller import eDevController


class eDevNavigator(wx.SplitterWindow):
     
    def __init__(self, parent, ID):
        wx.SplitterWindow.__init__(self, parent, ID)

        self._d_controller = eDevController.instance()
        
        # Create Archive-panel
        self._d_archive_panel = wx.Panel(self, -1)
        self._d_archive_panel.SetBackgroundColour(wx.Colour(0xef,0xef,0xff))
        box = wx.BoxSizer(wx.VERTICAL)
        self._d_archive_label = wx.StaticText(self._d_archive_panel, -1,"Archives")
        self._d_archive_tree  = eDevArchiveTree(self._d_archive_panel, -1)
        box.Add(self._d_archive_label, 0, wx.ALL|wx.EXPAND, 2)
        box.Add(self._d_archive_tree, 1, wx.GROW|wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 2)
        self._d_archive_panel.SetSizer(box)
        box.Fit(self._d_archive_panel)

        # Create Module-Panel
        self._d_module_panel = wx.Panel(self, -1)
        self._d_module_panel.SetBackgroundColour(wx.Colour(0xef,0xef,0xff))
        box = wx.BoxSizer(wx.VERTICAL)
        self._d_module_label = wx.StaticText(self._d_module_panel, -1, "Modules")
        box.Add(self._d_module_label, 0, wx.ALL|wx.EXPAND, 2)
        self._d_module_panel.SetSizer(box)
        box.Fit(self._d_module_panel)

        self.SplitHorizontally(self._d_archive_panel, self._d_module_panel)

        (tmp, size) = self._d_archive_label.GetSize()
        self.SetMinimumPaneSize(size+4)
        self.max_archive()

        self._d_controller.setArchiveTree(self._d_archive_tree)

        self._d_archive_label.Bind(wx.EVT_LEFT_DCLICK, self.OnToggleArchive)
        self._d_module_label.Bind(wx.EVT_LEFT_DCLICK, self.OnToggleArchive)


    def OnToggleArchive(self, evt):
        size = self.GetSashPosition()
        (tmp, lsize) = self._d_archive_label.GetSize()
        if size > lsize+4:
            self.max_modules()
        else:
            self.max_archive()


    def max_archive(self):
        (tmp, size) = self.GetSize()
        (tmp, lsize) = self._d_module_label.GetSize()
        size -= lsize
        self.SetSashPosition(size)

    
    def max_modules(self):
        (tmp, size) = self._d_archive_label.GetSize()
        self.SetSashPosition(size)
