import wx
import edef
from edef.dev import Model
from edef.dev import Controller
from edef.dev import NavigatorPanel
from ArchiveTree import ArchiveTreePanel
from PythonEditor import PythonEditor
import ModelArchive


class PyEditComponent:

    __metaclass__ = edef.Singleton
    def __init__(self):
        self._controller = Controller()
        self._model      = Model()

        self._model.registerProtocol("zip", ModelArchive.Model())

        self._controller.registerEditorClass("zip", PythonEditor)
        self._archive_tree = self._controller.addNavigatorClass( ArchiveTreePanel ).getArchiveTree()

        # add menu item:
        self._new_archive_id = wx.NewId()
        main_frame = self._controller.getMainFrame()
        menu_bar = main_frame.GetMenuBar()
        menu = menu_bar.GetMenu(menu_bar.FindMenu("File"))
        menu.AppendSeparator()
        menu.Append(self._new_archive_id, "New Archive")
        
        main_frame.Bind(wx.EVT_MENU, self.OnNewArchive, id=self._new_archive_id)


    def getArchiveTree(self):
        return self._archive_tree

    def OnNewArchive(self, evt):
        self._archive_tree.NewArchive(evt)



component = PyEditComponent
