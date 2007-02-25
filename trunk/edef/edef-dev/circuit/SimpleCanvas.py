import wx
import re
import Events
from copy import copy
import traceback
from SimpleCanvasObjects import gObject,gMoveable,gConnectable
from SimpleCanvasObjects import gModule,gPin,gWire
from PrimitiveCanvas import PrimitiveCanvas


class SimpleCanvas(PrimitiveCanvas):

    def __init__(self, parent, ID, virtSize=(1000,1000)):
        PrimitiveCanvas.__init__(self, parent, ID, virtSize)
        # FIXME reduce it to only self._objects
        self._objects           = []

        self._mouse_over_object = None
        self._mouse_over_coord  = (0,0)
        self._tool_tip_timer    = wx.Timer(self)
        self._tool_tip_showed   = False

        self._mouse_left_down   = False
        self._dragging          = False
        
        self._begin_drag_object = None

        self.Bind(wx.EVT_MOUSE_EVENTS, self._sc_OnMouseEvents)
        self.Bind(wx.EVT_LEFT_UP, self._sc_OnLeftUp)
        self.Bind(wx.EVT_LEFT_DOWN, self._sc_OnLeftDown)
        self.Bind(wx.EVT_RIGHT_UP, self._sc_OnRightUp)
        self.Bind(wx.EVT_LEFT_DCLICK, self._sc_OnLeftDClick)
        self.Bind(wx.EVT_MOTION, self._sc_OnMotion)
        self.Bind(Events.EVT_CAN_MOUSE_OVER, self._sc_OnMouseOver)
        self.Bind(Events.EVT_CAN_MOUSE_LEFT, self._sc_OnMouseLeft)
        self.Bind(wx.EVT_TIMER, self._sc_OnToolTipTimer)
        self.Bind(Events.EVT_CAN_BEGIN_DRAG, self._sc_OnBeginDrag)
        self.Bind(Events.EVT_CAN_DRAGGING, self._sc_OnDragging)
        self.Bind(Events.EVT_CAN_END_DRAG, self._sc_OnEndDrag)


    # tool method for emmiting events:
    def _emmitCanvasMouseEvent(self, coord):
        event = Events.CanvasMouseEvent(Events._event_can_mouse, self.GetId())
        event.SetCoordinates( coord )
        self.GetEventHandler().ProcessEvent(event)
        
    def _emmitMouseOver(self, coord, obj):
        event = Events.CanvasMouseOver(Events._event_can_mouse_over, self.GetId())
        event.SetCoordinates( coord )
        event.SetObject( obj )
        self.GetEventHandler().ProcessEvent(event)

    def _emmitMouseLeft(self, coord, obj):
        event = Events.CanvasMouseLeft(Events._event_can_mouse_left, self.GetId())
        event.SetCoordinates( coord )
        event.SetObject( obj )
        self.GetEventHandler().ProcessEvent(event)

    def _emmitCanvasClick(self, coord, obj):
        event = Events.CanvasClick(Events._event_can_click, self.GetId())
        event.SetCoordinates( coord )
        event.SetObject( obj )
        self.GetEventHandler().ProcessEvent(event)

    def _emmitCanvasDClick(self, coord, obj):
        event = Events.CanvasDClick(Events._event_can_dclick, self.GetId())
        event.SetCoordinates( coord )
        event.SetObject( obj )
        self.GetEventHandler().ProcessEvent(event)

    def _emmitCanvasRClick(self, coord, obj):
        event = Events.CanvasRClick(Events._event_can_rclick, self.GetId())
        event.SetCoordinates( coord )
        event.SetObject( obj )
        self.GetEventHandler().ProcessEvent(event)

    def _emmitCanvasShowToolTip(self, coord, obj):
        event = Events.CanvasShowToolTip(Events._event_can_show_tool_tip, self.GetId())
        event.SetCoordinates( coord )
        event.SetObject( obj )
        self.GetEventHandler().ProcessEvent(event)
    
    def _emmitCanvasHideToolTip(self, coord, obj):
        if not self._tool_tip_showed: return
        event = Events.CanvasHideToolTip(Events._event_can_hide_tool_tip, self.GetId())
        event.SetCoordinates( coord )
        event.SetObject( obj )
        self.GetEventHandler().ProcessEvent(event)
         
    def _emmitCanvasBeginDrag(self, coord, obj):
        self._dragging = True
        event = Events.CanvasBeginDrag(Events._event_can_begin_drag, self.GetId())
        event.SetCoordinates( coord )
        event.SetObject( obj )
        self.GetEventHandler().ProcessEvent(event)

    def _emmitCanvasDragging(self, coord):
        event = Events.CanvasDragging(Events._event_can_dragging, self.GetId())
        event.SetCoordinates( coord )
        self.GetEventHandler().ProcessEvent(event)
    
    def _emmitCanvasEndDrag(self, coord, obj):
        #print "emmit \"EndDrag\""
        event = Events.CanvasEndDrag(Events._event_can_end_drag, self.GetId())
        event.SetCoordinates( coord )
        event.SetObject( obj )
        self.GetEventHandler().ProcessEvent(event)
        self._dragging = False

    def _emmitCanvasConnect(self, from_obj, to_obj):
        #print "connecting: %s -> %s"%(from_obj.getName(), to_obj.getName())
        event = Events.CanvasConnectEvent(Events._event_can_connect, self.GetId())
        event.SetFrom( from_obj )
        event.SetTo( to_obj )
        self.GetEventHandler().ProcessEvent(event)

    #
    # wx.Window event-handler
    #
    def _sc_OnMouseEvents(self, evt):
        coord = self._convertEventCoords(evt)
        self._emmitCanvasHideToolTip(coord, None)
        self._emmitCanvasMouseEvent(coord)
        evt.Skip()

    def _sc_OnLeftDown(self, evt):
        self._mouse_left_down = True  # needed for draggig 
        evt.Skip()
    
    def _sc_OnLeftUp(self, evt):
        coord = self._convertEventCoords(evt)
        obj = self.hitTest( coord )
        
        if self._dragging: self._emmitCanvasEndDrag(coord, obj)
        if isinstance(obj, gObject): self._emmitCanvasClick(coord, obj)
        self._mouse_left_down = False
        evt.Skip()

    def _sc_OnLeftDClick(self, evt):
        coord = self._convertEventCoords(evt)
        obj = self.hitTest( coord )
        if isinstance(obj, gObject): self._emmitCanvasDClick(coord, obj)
        evt.Skip()

    def _sc_OnRightUp(self, evt):
        coord = self._convertEventCoords(evt)

        obj = self.hitTest( coord )
        if isinstance(obj, gObject): self._emmitCanvasRClick(coord, obj)
        evt.Skip()
   
    def _sc_OnMotion(self, evt):
        coord = self._convertEventCoords(evt)
        obj = self.hitTest(coord)
        
        # handle dragging:
        if self._mouse_left_down and not self._dragging:
            self._emmitCanvasBeginDrag(coord, obj)
        elif self._dragging:
            self._emmitCanvasDragging(coord)

        # generate mouse over events:
        if isinstance(obj, gObject):
            self._mouse_over_coord = coord
            # do not reemmit mouse over
            if not obj==self._mouse_over_object:
                self._mouse_over_object = obj
                self._emmitMouseOver(coord, obj)
            evt.Skip()
            return

        # generate mouse left events:
        if self._mouse_over_object:
            self._emmitMouseLeft(coord, self._mouse_over_object)
            self._mouse_over_object = None
            self._mouse_over_coord  = (0,0)
        evt.Skip()

    
    #
    # SimpleCanvas event handler
    #
    def _sc_OnMouseOver(self, evt):
        if self._tool_tip_timer.IsRunning():
            self._tool_tip_timer.Stop()
        self._tool_tip_timer.Start(3000, True)
        evt.Skip()

    def _sc_OnMouseLeft(self, evt):
        if self._tool_tip_timer.IsRunning():
            self._tool_tip_timer.Stop()
        evt.Skip()

    def _sc_OnToolTipTimer(self, evt):
        self._tool_tip_showed = True
        self._emmitCanvasShowToolTip(self._mouse_over_coord,
                                     self._mouse_over_object)
    
    def _sc_OnBeginDrag(self, evt):
        obj = evt.GetObject()
        if isinstance(obj, gObject):
            self._begin_drag_object = obj
        evt.Skip()

    def _sc_OnDragging(self, evt):
        #if isinstance(self._begin_drag_object, gModule):
        #    self._begin_drag_object.setPosition(evt.GetCoordinates())
        #    self.redraw()
        # FIXME maybe we should show here a simple square  
        pass

    def _sc_OnEndDrag(self, evt):
        start_obj = self._begin_drag_object
        x,y = evt.GetCoordinates()
        
        # handle moveable objects (ie. Modules):
        if isinstance(start_obj, gMoveable):
            print "move object to %s,%s"%(x,y)
            # prevet to move to close to border
            (w,h) = start_obj.getSize()
            if x >= 2 and x+w<=198 and y>=2 and y+h<=198:
                # set position and redraw
                start_obj.setPosition(evt.GetCoordinates())
                self.redraw()
        
        # handle connectable objects (ie. Pins):            
        elif isinstance(start_obj, gConnectable) \
          and not start_obj == evt.GetObject()   \
          and isinstance(evt.GetObject(), gConnectable):
            self._emmitCanvasConnect(start_obj, evt.GetObject())
        
        # precess remaining handlers
        evt.Skip()
        self._begin_drag_object = None 

    #
    # handleing objects 
    #
    def addObject(self, obj, auto_redraw=False):
        if obj in self._objects: return
        print "add object %s to canvas"%obj
        self._objects.append(obj)
        if auto_redraw: self.redraw()

    def getObjects(self, typ):
        objs = []
        for obj in self._objects:
            if isinstance(obj, typ): objs.append(obj)
        return objs

    def delObject(self, obj):
        if not obj in self._objects: raise Exception("No object %s found in list"%obj)
        del self._objects[self._objects.index(obj)]
    
    def hitTest(self, coord):
        for obj in self._objects:
            hobj = obj.hitTest( coord )
            if isinstance(hobj, (gObject, gWire)): return hobj

    def draw(self, dc):
        for obj in self._objects: obj.draw(dc)



