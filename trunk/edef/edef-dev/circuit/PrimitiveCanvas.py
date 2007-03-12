""" This file defines the L{PrimitiveCanvas} class. This class provides method
    to do simple drawing in a defined 5x5 pixel raster. """

# ########################################################################## #
# PrimitiveCanvas.py
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
import logging


class PrimitiveCanvas(wx.ScrolledWindow):
    """ Canvas with very basic drawing features. It is subclassed from 
        C{wx.ScrolledWindow}, so it may emmit all events of it. """
    
    _logger = None  # This attribute will hold the logger for the edef-gui.
    
    def __init__(self, parent, ID=-1, virtSize=(200,200)):
        """ Constuctor. This method takes the parent window C{wx.Window} and 
            an optional ID. ID is by default -1, which means to be 
            autogenerated.  Additionally the contructor takes the optional 
            argument C{virtSize} which specifies the size of the canvas in the
            raster. By default it is 200x200. Note: The size of the canvas is
            currently fixed to 200x200!
            
            @param parent: Parent wx.Window.
            @param ID: wx Identifier. By default -1.
            @param virtSize: Size of the canvas. """
        
        wx.ScrolledWindow.__init__(self, parent, ID, (0,0), style=wx.SUNKEN_BORDER)
        
        self._logger = logging.getLogger("edef.dev")
        
        #vx,vy = virtSize FIXME make virtualsize more flexible
        vx = 1000 # 200*5
        vy = 1000 # 200*5
        self.virtualSize = vx,vy

        # init window
        self.SetBackgroundColour("WHITE")
        self.SetVirtualSize(self.virtualSize)
        self.SetScrollRate(20,20)

        # create buffer
        self.buffer = wx.EmptyBitmap(vx, vy)
        
        # prepare DC
        dc = wx.BufferedDC(None, self.buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()

        self.Bind(wx.EVT_PAINT, self._pc_OnPaint)


    def _convertEventCoords(self, evt):
        """ Takes an mouse-event or something that has GetX(), GetY() methods 
            and returns the raster-coordinates of the event. 
            @param evt: A wx.MouseEvent.
            @return: A (x,y) tuple  holding the converted coordinates."""
        return self._convertCoords( (evt.GetX(),evt.GetY()) )


    def _convertCoords(self, pos):
        """ Takes a (x,y) tuple and returns the raster coordinates. 
            @param pos: A (x,y) tuple specifiing the coordinates to convert.
            @return: A (x,y) tuple  holding the converted coordinates. """
        x,y = pos
        vx,vy = self.GetViewStart()
        dx,dy = self.GetScrollPixelsPerUnit()
        x,y = (x+(vx*dx), y+(vy*dy))
        return (int(x/5),int(y/5))

    
    def _pc_OnPaint(self, evt):
        """ Internal used evt-handler to create a buffered drawingcontext on 
            OnPaint events. """
        dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)

    
    #
    # basic Drawing methods
    #
    def redraw(self):
        """ Can be called to redraw the canvas. The method will call the 
            C{self.draw()} method. If you inherit from this class you should 
            override the draw() method to get something drawn """
        dc = self.beginDrawing()
        dc.Clear()
        self._logger.debug("Call (maybe overridden) self.draw()")
        self.draw(dc)
        self.endDrawing(dc)


    def draw(self, dc):
        """ This method can be overridden to draw something on the canvas. 
            This method will also be called by the C{redraw()} method. 
            
            The parameter C{dc} will be the drawingcontext to draw on. If you
            like to invoke the draw() method by your self, please use the 
            C{beginDrawing()} and C{endDrawing()} methods to get and finish 
            the drawingcontext. """
        pass


    def beginDrawing(self):
        """ This method will create an empty drawingcontext to be used to
            draw on. Please use the C{endDrawing()} method to finalize the
            DC."""
        cdc = wx.ClientDC(self)
        self.PrepareDC(cdc)
        dc = wx.BufferedDC(cdc, self.buffer)
        dc.BeginDrawing()
        return dc


    def endDrawing(self, dc):
        """ This method will finalize the given drawingcontext. """
        dc.EndDrawing()


    def drawRectangle(self, dc, where, size, color="BLACK"):
        """ This method draws a simple rectangle at the given coordinates and 
            with the given size. 

            @param dc: The drawing context to draw on. You can get it from 
                beginDrawing() method.
            @param where: A (x,y) tuple holding the coordinates of the 
                upper-left corner of the rectangle.
            @param size: A (w,h) tuple holding the width and the height of the
                rectnagle. """
        # convert coordinates from raster to real
        (x, y) = where
        x=x*5+2
        y=y*5+2
        # convert size from rater to real
        (w, h) = size
        assert w >= 1
        assert h >= 1
        w = w*5-3
        h = h*5-3
        # draw
        dc.SetBrush( wx.TRANSPARENT_BRUSH )
        dc.SetPen(wx.Pen(color,2))
        dc.DrawRectangle(x,y, w,h)
        

    def drawLine(self, dc, frm, to):
        """ This method will draw a line.
            
            @param dc: The drawing context to draw on. You can get it from 
                beginDrawing() method.
            @param frm: A (x,y) tuple holding the coordinates where the line 
                starts.
            @param frm: A (x,y) tuple holding the coordinates where the line 
                ends. """
        # convert coordinates from raster to real:
        x1,y1 = frm
        x2,y2 = to
        x1 = x1*5+2
        y1 = y1*5+2
        x2 = x2*5+2
        y2 = y2*5+2
        # draw
        dc.SetPen( wx.Pen("YELLOW",1) )
        dc.DrawLine( x1,y1, x2,y2 )


    def drawPin(self, dc, coord, pos=wx.LEFT):
        """ This method will draw a short line at the given coordinates. This 
            method will be used to draw pins.
            
            @param dc: The drawing context to draw on. You can get it from 
                beginDrawing() method.
            @param coord: A (x,y) tuple holding the coordinates the to put the
                pin.
            @param pos: The optional parameter specifies if the pin is on the
                left (wx.LEFT) or on the right (wx.RIGHT) side of the module.
            """                
        (x,y) = coord
        y = y*5+2
        if pos == wx.LEFT: x = x*5+2
        else: x = x*5-2
        
        dc.SetPen( wx.Pen("BLACK",1) )
        dc.DrawLine(x,y,x+5,y)
         

    def drawTitle(self, dc, txt, where):
        """ Draws an fat centered text at the given position. 
            
            @param dc: The drawing context to draw on. You can get it from 
                beginDrawing() method.
            @param txt: The string to draw.
            @param where: A (x,y) tuple where to put the text. """
        dc.SetFont( wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD) )
        dc.SetTextForeground( wx.Colour(0x00,0x00,0x00) )
       
        (w,h) = dc.GetTextExtent(txt)
        (x,y) = where
        x = x*5-int(w/2)
        y = y*5
        
        dc.DrawText(txt, x, y)


    def drawText(self, dc, txt, where, ori=wx.LEFT):
        """ Draws a small text.
            
            @param dc: The drawing context to draw on. You can get it from 
                beginDrawing() method.
            @param txt: The string to draw.
            @param where: A (x,y) tuple specifies the coordinates where to put 
                the string.
            @param ori: This optional parameter specifies the orientation of 
                the text. By default it is wx.LEFT. wx.RIGHT is also allowed. 
            """
        dc.SetFont( wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL) )
        dc.SetTextForeground( wx.Colour(0x00,0x00,0xff) )
        (w,h) = dc.GetTextExtent(txt)
        
        (x,y) = where
        x *= 5
        y = y*5 - int(h/2) +2
        if ori==wx.RIGHT: x -= w+2
        dc.DrawText(txt, x, y)


    def drawFilledRect(self, dc, coord, size):
        """ Simply draws a light-gray filled rectangle. (Used to draw the 
            costmap). 
            
            @param dc: The drawing context to draw on. You can get it from 
                beginDrawing() method.
            @param coord: A (x,y) tuple specifies the upper-left coordinates 
                of the rectangle.
            @param size: A (w,h) tuple defines the width and height of the 
                rectangle. """
        (x,y) = coord
        (w,h) = size
        x *= 5
        y *= 5
        w *= 5
        h *= 5
        
        dc.SetBrush( wx.Brush("LIGHTGREY") )
        dc.SetPen( wx.Pen("RED", 1))
        dc.DrawRectangle(x,y,w,h)


