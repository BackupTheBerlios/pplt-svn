import edef
import edef.dev
from edef.dev.circuit.SimpleCanvasObjects import gModule, gPin
import wx

class lamp(gModule):
    def __init__(self, canvas, coord):
        gModule.__init__(self, canvas, coord, "logic.gui.lamp", [])
        self._state = False
        
        self._in_pin = gPin(self, "i_in")
        
        self.setSize( (12,7) )
        self._apply_position_rules()
        
    def i_in(self, value):
        if value: self._state = True
        else: self._state = False
        dc = self.getCanvas().beginDrawing()
        self.draw(dc)
        self.getCanvas().endDrawing(dc)
        del dc
        wx.WakeUpIdle()

    def draw(self, dc):
        x,y = self.getPosition()
        if self._state: color="GREEN"
        else: color = "LIGHTGRAY"
        self.getCanvas().drawFilledRect(dc, (x+6,y+1), (5,5), color)
        gModule.draw(self, dc)

    def drawTitle(self, dc): pass

    def _calcHeight(self): return 7
    def _getPinOffset(self): return 3
