import wx


class PrimitiveCanvas(wx.ScrolledWindow):
    def __init__(self, parent, ID, virtSize=(1000,1000)):
        wx.ScrolledWindow.__init__(self, parent, ID, (0,0), style=wx.SUNKEN_BORDER)
        self.virtualSize = virtSize
        (vx, vy) = virtSize

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
        vx,vy = self.GetViewStart()
        dx,dy = self.GetScrollPixelsPerUnit()
        x,y = (evt.GetX()+(vx*dx), evt.GetY()+(vy*dy))
        return (int(x/5), int(y/5))

    def _pc_OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)

    #
    # basic Drawing methods
    #
    def redraw(self):
        dc = self.beginDrawing()
        dc.Clear()
        print "call draw()"
        self.draw(dc)
        self.endDrawing(dc)

    def draw(self, dc): pass

    def beginDrawing(self):
        # get dc
        cdc = wx.ClientDC(self)
        self.PrepareDC(cdc)
        dc = wx.BufferedDC(cdc, self.buffer)
        dc.BeginDrawing()
        return dc

    def endDrawing(self, dc):
        dc.EndDrawing()


    def drawRectangle(self, dc, where, size):
        (x, y) = where
        x=x*5+2
        y=y*5+2
        
        (w, h) = size
        assert w >= 1
        assert h >= 1
        w = w*5-3
        h = h*5-3
        dc.SetBrush( wx.TRANSPARENT_BRUSH )
        dc.SetPen(wx.Pen("BLACK",2))
        dc.DrawRectangle(x,y, w,h)
        

    def drawLine(self, dc, frm, to):
        x1,y1 = frm
        x2,y2 = to
        x1 = x1*5+2
        y1 = y1*5+2
        x2 = x2*5+2
        y2 = y2*5+2

        dc.SetPen( wx.Pen("YELLOW",1) )
        dc.DrawLine( x1,y1, x2,y2 )


    def drawPin(self, dc, coord, pos=wx.LEFT):
        (x,y) = coord
        y = y*5+2
        if pos == wx.LEFT: x = x*5+2
        else: x = x*5-2
        
        dc.SetPen( wx.Pen("BLACK",1) )
        dc.DrawLine(x,y,x+5,y)
         

    def drawTitle(self, dc, txt, where):
        dc.SetFont( wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD) )
        dc.SetTextForeground( wx.Colour(0x00,0x00,0x00) )
       
        (w,h) = dc.GetTextExtent(txt)
        (x,y) = where
        x = x*5-int(w/2)
        y = y*5
        
        dc.DrawText(txt, x, y)


    def drawText(self, dc, txt, where, ori=wx.LEFT):
        dc.SetFont( wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL) )
        dc.SetTextForeground( wx.Colour(0x00,0x00,0xff) )
        (w,h) = dc.GetTextExtent(txt)
        
        (x,y) = where
        x *= 5
        y = y*5 - int(h/2) +2
        if ori==wx.RIGHT: x -= w+2
        dc.DrawText(txt, x, y)


    def drawFilledRect(self, dc, coord, size):
        (x,y) = coord
        (w,h) = size
        x *= 5
        y *= 5
        w *= 5
        h *= 5
        
        dc.SetBrush( wx.Brush("LIGHTGREY") )
        dc.SetPen( wx.Pen("RED", 1))
        dc.DrawRectangle(x,y,w,h)


