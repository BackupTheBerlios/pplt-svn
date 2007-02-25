import wx
import re
from copy import copy


#
# Some interfaces. These interface should be used to implement grafical 
# objects.

class gObject:
    """ Interface for alle objects, that wants to be displayed. """

    def draw(self, dc):
        """ This method have to be overridden to implement darwing of the 
            object """
        raise Exception("Not inplemented yet")
    
    def hitTest(self, coordinates):
        """ This method have to be overridden. It should return self if it is
            hited by the given coordinates. """
        raise Exception("Not implemented yet")


class gMoveable(gObject):
    def setPosition(self, coordinates):
        """ This method should be overridden! It should reset all internal 
            used coordinates. So if the module's draw() method is called, it
            will be drawn at the new position! """
        raise Exception("Not inplemented yet")
    def getSize(self):
        """ This method should return the size (width, height) of the 
            object. """
        raise Exception("Not implmeneted yet")


class gConnectable(gObject):
    """ This psoydo class identifies the object als a grafical and connectable
        one. """
    pass





class gWire(gObject):
    def __init__(self, frm, to, nodes=[]):
        self._canvas    = frm.getCanvas()
        self._from      = frm
        self._to        = to
        self._nodes     = self._reduceNodes(nodes)

        self._canvas.addObject(self)

    def getCanvas(self): return self._canvas
    def getFrom(self): return self._from
    def getTo(self): return self._to

    def getFromPos(self): return (self._from._x, self._from._y)
    def getToPos(self): return (self._to._x, self._to._y)
    
    def getNodes(self): return self._nodes
    def setNodes(self, nodes):
        nodes = self._reduceNodes(nodes)
        self._nodes = nodes

    def between(self, w, a, b):
        if a > b and w <= a and w >= b: return True
        elif w >= a and w <= b: return True
        return False

    def _reduceNodes(self, nodes):
        return nodes    # FIXME
        if len(nodes) == 0: return nodes
        reduced = [nodes[0]]
        lx,ly = reduced[-1]
        
        x,y   = self._from._x, self._from._y
        if lx == x: dir_updown = False
        else: dir_updown = True

        for (cx,cy) in nodes:
            if dir_updown and lx != cx:
                dir_updown = False
                reduced.append( (cx,cy) )
            elif not dir_updown and ly != cy:
                dir_updown = True
                reduced.append( (cx,cy) )
            lx,ly = cx,cy
        return reduced


    def draw(self, dc):
        sx,sy = self._from._x, self._from._y
        for (tx,ty) in self._nodes:
            self._canvas.drawLine(dc, (sx,sy), (tx,ty))
            sx,sy = tx,ty
        tx,ty = self._to._x,self._to._y
        self._canvas.drawLine(dc, (sx,sy), (tx,ty))

    def hitTest(self, coord):
        x,y = coord
        sx,sy = self._from._x, self._from._y
        for (tx,ty) in self._nodes:
            if self.between(x, sx, tx) and sy == ty: return self
            elif self.between(y, sy, ty) and sx == tx: return self
            sy,sx = ty,tx
        ty,tx = self._to._x, self._to._y
        if self.between(x, sx, tx) and sy == ty: return self
        elif self.between(y, sy, ty) and sx == tx: return self
        return None            



class gPin(gConnectable):
    def __init__(self, module, name):
        self._module = module
        self._canvas = module.getCanvas()
        self._name = name
        m = re.match("^(i_|o_)(.+)$",name)
        self._display_name = m.group(2)
        self._position = wx.LEFT
        self._x, self._y = (0,0)
        self._module.addPin(self)

    def draw(self, dc):
        if self._position == wx.LEFT:
            self._canvas.drawText(dc, self._display_name, (self._x+2,self._y), wx.LEFT)
            #self._canvas.drawFilledRect(dc, (self._x-1,self._y), (1,1) )
            self._canvas.drawPin(dc, (self._x,self._y) )
        else:
            self._canvas.drawText(dc, self._display_name, (self._x-1,self._y), wx.RIGHT)
            #self._canvas.drawFilledRect(dc, (self._x,self._y),(1,1))
            self._canvas.drawPin(dc, (self._x,self._y), wx.RIGHT)

    
    def hitTest(self, coord):
        mx,my = coord
        if self._position == wx.LEFT and ((mx == self._x and my == self._y) or ( mx in (self._x+1, self._x+2) and my in (self._y-1,self._y,self._y+1))):
            return self
        elif self._position == wx.RIGHT and ((mx == self._x and my == self._y) or ( mx in (self._x-1, self._x-2) and my in (self._y-1,self._y,self._y+2))):
            return self

    
    def setPosition(self, coord, pos=wx.LEFT):
        self._position = pos
        (self._x, self._y) = coord
        if self._position == wx.LEFT: self._x -= 1

    def getPosition(self): return ( (self._x, self._y), self._position )
    def getName(self): return self._name
    def getModule(self): return self._module
    def getCanvas(self): return self._canvas



class gModule(gMoveable):
    def __init__(self, can, coord, name, rules):
        self._canvas = can
        self._name = name
        self._rules = rules #FIXME

        self._pins = {}

        self._width = 20
        (self._x, self._y) = coord
        self._calcPinPositions()

        self._canvas.addObject(self)


    def getPosition( self ): return (self._x, self._y)
    def getSize( self ): return (self._width, self._height)

    def _apply_pos_rules(self, pins):
        """ This method applyes the defined layout-rules and fills the
            left or right side lists of pins """
        self._left_side_pins = []
        self._right_side_pins = []
        
        for pin_name in pins:
            in_m = re.match("^i_(.+)$",pin_name)
            out_m = re.match("^o_(.+)$",pin_name)
            if in_m:
                y = self._y+7+len(self._left_side_pins)*3
                x = int(self._x)
                self._pins[pin_name].setPosition((x,y), wx.LEFT)
                self._left_side_pins.append( pin_name )
            elif out_m:
                y = self._y+7+len(self._right_side_pins)*3
                x = self._x+self._width
                self._pins[pin_name].setPosition((x,y), wx.RIGHT)
                self._right_side_pins.append( pin_name )


    def _calcPinPositions(self):
        pins = self._pins.keys()
        self._apply_pos_rules(pins)
        
        max_len = len(self._left_side_pins)
        if max_len < len(self._right_side_pins):
            max_len = len(self._right_side_pins)
        self._height = max_len*3+8

    def addPin(self, pin):
        name = pin.getName()
        if name in self._pins.keys(): raise Exception("Pin allready exists")
        self._pins[name] = pin
        self._calcPinPositions()
    
    def getPin(self, name): return self._pins[name]
    def getCanvas(self): return self._canvas

    def draw(self, dc):
        #print "Draw Module @ %s,%s"%(self._x, self._y)
        #self._canvas.drawFilledRect(dc, (self._x, self._y), (self._width, self._height) )
        self._canvas.drawRectangle(dc, (self._x, self._y), (self._width, self._height) )
        self._canvas.drawTitle(dc, self._name, (self._x+int(self._width/2), self._y+1) )
        
        for name in self._left_side_pins: self._pins[name].draw(dc)
        for name in self._right_side_pins: self._pins[name].draw(dc)


    def hitTest(self, coord):
        mx, my = coord
        for name in self._left_side_pins:
            pin = self._pins[name].hitTest(coord)
            if pin: return pin
        for name in self._right_side_pins:
            pin = self._pins[name].hitTest(coord)
            if pin: return pin
        if (mx >= self._x and mx <= self._x+self._width) and (my >= self._y and my <= self._y+self._height):
            return self


    def setPosition(self, pos):
        self._x, self._y = pos
        self._calcPinPositions()


