import edef
from edef.dev import Model
from edef.dev import Controller
from edef.dev import NavigatorPanel
from ModuleTree import ModuleTreePanel
from ModelModule import Model as ModModel
from ModuleEditor import eDevModuleEditor as ModuleEditor

class ModEditComponent:

    __metaclass__ = edef.Singleton
    def __init__(self):
        self._controller = Controller()
        self._model      = Model()

        self._model.registerProtocol("mod", ModModel())
        self._controller.registerEditorClass("mod", ModuleEditor)
        self._module_tree = self._controller.addNavigatorClass( ModuleTreePanel ).getModuleTree()

    def getModuleTree(self): return self._module_tree

component = ModEditComponent
