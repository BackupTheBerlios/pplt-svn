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

  
    def getArchiveTree(self):
        return self._archive_tree


component = PyEditComponent
