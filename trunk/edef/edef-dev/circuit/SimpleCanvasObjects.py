""" This file defines the basic grafic objects that can be added to a 
    L{Simplecanvas} """

# ########################################################################## #
# SimpleCanvas.py
#
# 2007-03-05
# Copyright 2007 Hannes Matuschek
# hmatuschek@gmx.net
# ########################################################################## #
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# ########################################################################## #


import wx
import re
from copy import copy
from SimpleCanvas import SimpleCanvas, gObject, gMoveable, gConnectable
import weakref
from leftarrow import getBitmap as getLeftArrowBitmap
from rightarrow import getBitmap as getRightArrowBitmap


#
# Specialized grafic objects.
#
class gModule(gMoveable):
    """ This object represents a module. """
    _name           = None
    _rules          = None
    _pins           = None
    
    def __init__(self, can, coord, name, label, rules):
        self.setName(name)
        if not label: self.setLabel(name.split(".")[-1])
        else: self.setLabel(label)

        self._rules = rules #FIXME

        self._pins = {}

        gMoveable.__init__(self, can, coord)
        
        self._apply_position_rules()
        
        self.setSize( (20,self._calcHeight()) )
    

   
    def setName(self, name): self._name = name
    def getName(self): return self._name


    def getLabel(self): return self._label
    def setLabel(self, label, auto_redraw=False):
        self._label = label
        if auto_redraw:
            dc = self.getCanvas().beginDrawing()
            self.getCanvas().eraseRect(dc, self.getPosition(), self.getSize())
            self.draw(dc)
            self.getCanvas().endDrawing(dc)


    def setPosition(self, pos):
        gMoveable.setPosition(self, pos)
        self._apply_position_rules()


    def getPin(self, name): return self._pins[name]
    def addPin(self, pin):
        name = pin.getName()
        if name in self._pins.keys(): raise Exception("Pin allready exists")
        self._pins[name] = pin
        self._apply_position_rules()
        (w,h) = self.getSize()
        self.setSize( (w,self._calcHeight()) )

    
    def drawTitle(self, dc):
        _x,_y = self.getPosition()
        _w,_h = self.getSize()

        name = self.getLabel()
        self._canvas.drawTitle(dc, name, (_x+int(_w/2), _y+1) )
    
    
    def draw(self, dc):
        _x, _y = self.getPosition()
        _w, _h = self.getSize()
        self._canvas.drawRectangle(dc, self.getPosition(), self.getSize() )
        
        self.drawTitle(dc)

        for name in self._left_side_pins: self._pins[name].draw(dc)
        for name in self._right_side_pins: self._pins[name].draw(dc)


    def drawSelected(self, dc):
        self._canvas.drawRectangle(dc, self.getPosition(), self.getSize(), "RED")


    def hitTest(self, coord):
        mx, my = coord
        _x,_y = self.getPosition()
        _w,_h = self.getSize()
        for name in self._left_side_pins:
            pin = self._pins[name].hitTest(coord)
            if pin: return pin
        for name in self._right_side_pins:
            pin = self._pins[name].hitTest(coord)
            if pin: return pin
        if (mx >= _x and mx <= _x+_w) and (my >= _y and my <= _y+_h):
            return self


    def _apply_position_rules(self):
        """ This method applyes the defined layout-rules and fills the
            left or right side lists of pins """
        pins = self._pins.keys()
        
        self._left_side_pins = []
        self._right_side_pins = []
        
        _x,_y = self.getPosition()
        _w,_h = self.getSize()

        for pin_name in pins:
            in_m = re.match("^i_(.+)$",pin_name)
            out_m = re.match("^o_(.+)$",pin_name)
            if in_m:
                y = _y+7+len(self._left_side_pins)*3
                x = int(_x)
                self._pins[pin_name].setPosition((x,y))
                self._pins[pin_name].setOrientation(wx.LEFT)
                self._left_side_pins.append( pin_name )
            elif out_m:
                y = _y+7+len(self._right_side_pins)*3
                x = _x+_w
                self._pins[pin_name].setPosition((x,y))
                self._pins[pin_name].setOrientation(wx.RIGHT)
                self._right_side_pins.append( pin_name )


    def _calcHeight(self):
        """ Retuns the height of the module """
        max_len = len(self._left_side_pins)
        if max_len < len(self._right_side_pins):
            max_len = len(self._right_side_pins)
        return max_len*3+8

 


class gPin(gConnectable):
    def __init__(self, module, name):
        self._module_ref = weakref.ref(module)
        self._canvas = module.getCanvas()
        self._name = name
        m = re.match("^(i_|o_)(.+)$",name)
        self._display_name = m.group(2)
        self._position = wx.LEFT
        self._x, self._y = (0,0)
        self._module_ref().addPin(self)
        self._left_bmp = getLeftArrowBitmap()
        self._right_bmp = getRightArrowBitmap()


    def draw(self, dc):
        if self._position == wx.LEFT:
            if re.match("^i_", self._name): bmp = self._right_bmp
            else: bmp = self._left_bmp
            self._canvas.drawBMP(dc, bmp, (self._x+2,self._y), (-1,0))
            self._canvas.drawText(dc, self._display_name, (self._x+3,self._y), wx.LEFT)
            self._canvas.drawPin(dc, (self._x,self._y) )
        else:
            if re.match("^i_", self._name): bmp = self._left_bmp
            else: bmp = self._right_bmp
            self._canvas.drawBMP(dc, bmp, (self._x-2,self._y))
            self._canvas.drawText(dc, self._display_name, (self._x-2,self._y), wx.RIGHT)
            self._canvas.drawPin(dc, (self._x,self._y), wx.RIGHT)

    
    def hitTest(self, coord):
        mx,my = coord
        if self._position == wx.LEFT and \
           ((mx == self._x and my == self._y) or \
           ( mx in (self._x+1, self._x+2) and \
           my in (self._y-1,self._y,self._y+1))):
                return self
        elif self._position == wx.RIGHT and ((mx == self._x and my == self._y) or ( mx in (self._x-1, self._x-2) and my in (self._y-1,self._y,self._y+2))):
            return self

    
    def setPosition(self, coord): (self._x, self._y) = coord
    
    def getPosition(self): return (self._x, self._y)

    def setOrientation(self, ori=wx.LEFT):
        self._position = ori
        if self._position == wx.LEFT: self._x -=1
    
    def getOrientation(self): return self._position

    
    def getName(self): return self._name
    def getModule(self): return self._module_ref()




class gWire(gObject):
    def __init__(self, frm, to, nodes=[]):
        self._from      = frm
        self._to        = to
        self._nodes     = self._reduceNodes(nodes)

        gObject.__init__(self, frm.getCanvas() )

    def getFrom(self): return self._from
    def getTo(self): return self._to

    def getFromPos(self): return self._from.getPosition()
    def getToPos(self): return self._to.getPosition()
    
    def getNodes(self): return self._nodes
    def setNodes(self, nodes):
        nodes = self._reduceNodes(nodes)
        self._nodes = nodes

    def between(self, w, a, b):
        if a > b and w <= a and w >= b: return True
        elif a < b and w >= a and w <= b: return True
        return False

    def _reduceNodes(self, nodes):
        return nodes    # FIXME
        if len(nodes) == 0: return nodes
        reduced = [nodes[0]]
        lx,ly = reduced[-1]
        
        x,y   = self.getFromPos()
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
        sx,sy = self.getFromPos()
        for (tx,ty) in self._nodes:
            self._canvas.drawLine(dc, (sx,sy), (tx,ty))
            sx,sy = tx,ty
        tx,ty = self.getToPos()
        self._canvas.drawLine(dc, (sx,sy), (tx,ty))

    def drawSelected(self, dc):
        sx,sy = self.getFromPos()
        for (tx,ty) in self._nodes:
            self._canvas.drawLine(dc, (sx,sy), (tx,ty), "RED")
            sx,sy = tx,ty
        tx,ty = self.getToPos()
        self._canvas.drawLine(dc, (sx,sy), (tx,ty), "RED")


    def hitTest(self, coord):
        x,y = coord
        sx,sy = self.getFromPos()
        for (tx,ty) in self._nodes:
            if self.between(x, sx, tx) and sy == ty and y == sy: return self
            elif self.between(y, sy, ty) and sx == tx and x == sx: return self
            sy,sx = ty,tx
        ty,tx = self.getToPos()
        if self.between(x, sx, tx) and sy == ty: return self
        elif self.between(y, sy, ty) and sx == tx: return self
        return None            





