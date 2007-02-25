import wx
from copy import copy,deepcopy
import math


class CanvasCostmap:
    _map = None
    def __init__(self, target=(0,0)):
        self._map = dict()
        self._target_x, self._target_y = target
        
        self._dist_cost = 10
        self._wire_cost = 100
        self._module_cost = 1000


    def _dist(self, pos):
        x1,y1 = self.getTarget()
        x2,y2 = pos
        dx, dy = ( x1-x2, y1-y2 )
        return abs(dx)+abs(dy)
        #return math.sqrt( dx*dx +dy*dy )
    
    def setTarget( self, pos ):
        self._target_x, self._target_y = pos
    def getTarget( self ):
        return (self._target_x, self._target_y)

    def get(self, pos):
        x,y=pos
        return self.getPure(pos) + self._dist( pos ) * self._dist_cost
   
    def getPure(self, pos):
        x,y=pos
        if not self._map.has_key(x): return 0
        if not self._map[x].has_key(y): return 0
        return self._map[x][y]

    def add(self, pos, cost):
        x,y = pos
        if not self._map.has_key(x): self._map[x] = dict()
        if not self._map[x].has_key(y): self._map[x][y] = 0
        self._map[x][y] += cost

    def addWire(self, wire ):
        frm   = wire.getFromPos()
        to    = wire.getToPos()
        nodes = wire.getNodes()
        mynodes = copy(nodes)
        mynodes.append(to)
        
        (sx,sy) = frm
        for node in mynodes:
            tx,ty = node
            if tx == sx:
                if sy > ty: (sy, ty) = (ty,sy)
                for i in range(ty-sy): self.add( (sx,sy+i), self._wire_cost )
            if ty == sy:
                if sx > tx: (sy,ty) = (ty, sy)
                for i in range(tx-sx): self.add( (sx+i,sy), self._wire_cost )
            sx, sy = node

    def addModule(self, pos, size ):
        x,y=pos
        w,h=size
        for dx in range(w):
            for dy in range(h): self.add( (x+dx,y+dy), self._module_cost )

    def copy(self): return deepcopy(self)


    def draw(self, dc):
        for (x, y_list) in self._map.items():
            for (y,value) in y_list.items():
                val = int( (1- self.get( (x,y) )/400000.0)*255 )%256
                col = wx.Colour(val,val,val)
                dc.SetBrush( wx.Brush(col) )
                dc.SetPen( wx.Pen(col) )
                dc.DrawRectangle(x*5,y*5,5,5)


