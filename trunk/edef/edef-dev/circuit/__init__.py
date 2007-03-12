from ElementMapObjects import DefaultGraficModule
import edef
import edef.dev

from CircuitModel import Model
from CircuitTree import CircuitTreePanel
from CircuitEditor import CircuitEditor

class CircuitComponent:
    __metaclass__ = edef.Singleton
    
    def __init__(self):
        self._ctrl = edef.dev.Controller()
        self._model = edef.dev.Model()


        self._model.registerProtocol("circ", Model())
        self._ctrl.registerEditorClass("circ", CircuitEditor)
        self._circ_tree = self._ctrl.addNavigatorClass( CircuitTreePanel )


    def getCircuitTree(self): return self._circ_tree.getCircuitTree()

component = CircuitComponent
