import edef
import edef.dev
from edef.dev.circuit.SimpleCanvasObjects import gModule, gPin


class button_dummy:
    def __init(self):
        self.o_out = edef.ValueOutput(False)
        
        
class button(gModule):
    def __init__(self, canvas, coord):
        gModule.__init__(self, canvas, coord, "logic.gui.button", [])
        self._state = False
        self.o_out = edef.ValueOutput(False)
       
        self._out_pin = gPin(self, "o_out")
        
        self.setSize( (12,7) )
        self._apply_position_rules()
        

    def draw(self, dc):
        x,y = self.getPosition()
        if self._state: color="GREEN"
        else: color = "LIGHTGRAY"
        self.getCanvas().drawFilledRect(dc, (x+1,y+1), (5,5), color)
        gModule.draw(self, dc)

    def drawTitle(self, dc): pass

    def OnClick(self):
        self._state = not self._state
        self.o_out(self._state)
        dc = self.getCanvas().beginDrawing()
        self.draw(dc)
        self.getCanvas().endDrawing(dc)

    def _calcHeight(self): return 7
    def _getPinOffset(self): return 3
