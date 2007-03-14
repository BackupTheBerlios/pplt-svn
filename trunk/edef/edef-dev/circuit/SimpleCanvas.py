""" This file specifies the L{SimpleCanvas} class. This class extend the 
    L{PrimitiveCanvas} class to handle grafical objects. """

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
from PrimitiveCanvas import PrimitiveCanvas
import logging
import Events
import sys


class SimpleCanvas(PrimitiveCanvas):
    """ This class extends the L{PrimitiveCanvas} class by object handleing. 
        
        This class is indirect derived from C{wx.ScrolledWindow} so it may 
        emmit all of it's events. But additionally it may emmit events defined
        in C{edef.dev.circuit.Events}. In the following section I will 
        describe them and when they are emmited. 
        
        Mouseevents
        -----------
        - L{EVT_CAN_MOUSE} - This event will be emited if any mouse event is
            noticed. I.e. moveing, left-click, ... The event-class is 
            L{CanvasMouseEvent}. You can get the coordinates of the event
            by GetCoordinates().
        - L{EVT_CAN_CLICK} - This event will be emited on a left click. But 
            only if a grafical object was click. In this case the event 
            contains the coordinates and the clicked object. You can get the
            coordinates by calling C{GetCoordinates()} and the object by 
            calling GetObject(). The event will be an instance of 
            L{CanvasClick}. 
        - L{EVT_CAN_RCLICK} - Same like L{EVT_CAN_CLICK} but for a 
            right-click. But the event will be an instance of 
            L{CanvasRClick}.
        - L{EVT_CAN_DCLICK} - Same like L{EVT_CAN_CLICK} but for a
            double-click. And the event will be an instance of 
            L{CanvasDClick}.
        - L{EVT_CAN_MOUSE_OVER} - This event will be emmited if the mouse 
            enters a grafical object. Like L{EVT_CAN_CLICK} you can get the 
            coordinates of the mouse and the entered object. Eventclass:
            L{CanvasMouseOver}
        - L{EVT_CAN_MOUSE_LEFT} - This event will be emmited if the mouse 
            left a grafical object. Like C{EVT_CAN_MOUSE_OVER} you can get the
            coordinates and the object left from the event instance. This will
            be an instance of the L{CanvasMouseLeft} class.
            
        Tooltip Events
        --------------
        - L{EVT_CAN_SHOW_TOOL_TIP} - This event will be emitted if the mouse 
            rest above a grafical object. The event-instance holds the 
            coordinates of the mouse and the object under the mouse.
            Eventclass: L{CanvasShowToolTip}
        - L{EVT_CAN_HIDE_TOOL_TIP} - This event will be emmited if a 
            "show tooltip" event was emitted and the mouse was moved or a 
            button was hit. Use this event to hide the tooltip (if any shown).
            Eventclass: L{CanvasHideToolTip}
        
        Moving Events
        -------------
        - L{EVT_CAN_BEGIN_DRAG} - This event will be emited if the left 
            mousebutton is hold above a graficobject and the mose is moved.
            The event holds the coordinates of the mouse and the object 
            dragged. Evtenclass: L{CanvasBeginDrag}
        - L{EVT_CAN_DRAGGING} - This event will be emitted while dragging an
            grafica object. The event-instance only holds the coordinates of
            the mouse. Eventclass: L{CanvasDragging}
        - L{EVT_CAN_END_DRAG} - This event will be emitted if the left mouse
            button is release after dragging an object. The event instance
            holds the coordinates and the grafic object at this coordinates
            if there is one otherwise it will hold the object dragged.
        - L{EVT_CAN_CONNECT} - This event will be emitted if you drag a grafic
            object that is an instance of L{gConnectable} to an other object,
            also an instance of C{gConnectable}. In this case the 
            event-instance holds the two C{gConnectable} objects.
            Evtenclass: L{CanvasConnectEvent}

        Selection Events
        ----------------
        - L{EVT_CAN_SELECTED} - This event will be emmited if a grafical 
            object was selected. The event-class L{CanvasSelectEvent} is 
            derived from L{CanvasObjectEvent}, so you get the object selected 
            and the coordinates of the mouse.
        - L{EVT_CAN_DESELECTED} - This event will be emmited if a grafical 
            object got deselected.
        """
   

    def __init__(self, parent, ID=-1, virtSize=(200,200)):
        """ This constructor takes the parent C{wx.Window} and an optional ID.
            Additional you can specify the size of the canvas with C{virtSize}.
            
            @param parent: Specifies the parent C{wx.Window} of the canvas.
            @param ID: Specifies the wx identifier. By default -1.
            @param virtSize: Takes a (x,y) tuple and specifies the size of the
                canvas.
            """
        # calling superclass constructor
        PrimitiveCanvas.__init__(self, parent, ID, virtSize)
        
        # this list will hold all grafical objects an redraw will loop through
        #   this list to redraw each object
        self._objects           = []
        
        # flags for tooltip-event generation 
        self._mouse_over_object = None
        self._mouse_over_coord  = (0,0)
        self._tool_tip_timer    = wx.Timer(self)
        self._tool_tip_showed   = False
        
        # flags for drag'n'drop events of moveable objects
        self._mouse_left_down   = False
        self._dragging          = False
        self._begin_drag_object = None

        # selected object
        self._selected_object   = None

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
        self.Bind(Events.EVT_CAN_SELECT, self._sc_OnSelect)
        self.Bind(Events.EVT_CAN_DESELECT, self._sc_OnDeselect)


    ### Overridden operators:
    def __contains__(self, obj): return self.hasObject(obj)
    

    ### handleing objects 
    def addObject(self, obj, auto_redraw=False):
        """ This method adds the give object to the internal object list.
            Note: You'll never need to call this method. This will be done
            be the contructor of the grafical object.
            This method takes a subclass of L{gObject} as argument. 
            
            @param obj: An instance of a grafical Object. Have to be an 
                instance of L{gObject} or derived.
            @param auto_redraw: This optional parameter specifies if the 
                canvas should be redrawn after the object is added. """
        # check object type
        if not isinstance(obj, gObject):
            raise Exception("Bad type: Object should be an instance of gObject but it is: %s"%type(obj))
        # check if object is allready known:            
        if obj in self._objects:
            self._logger.debug("gObject %s (%s) allready known!"%(obj, id(obj)))
            return
        # add object and optional redraw
        self._logger.debug("Add object %s(%s) to canvas"%(obj,id(obj)))
        self._objects.append(obj)
        #self._logger.debug("Object list now: %s"%self._objects)
        if auto_redraw: self.redraw()


    def getObjects(self, typ=None):
        """ This method retunrs all known grafical objects of the spcified 
            type. If C{typ} is C{None} or left it will return all grafical
            objects.
            @param typ: Specifies the type of the objects returned. 
            @return: A list of instances that have the specified type. """
        if typ == None: return self._objects
        objs = []
        for obj in self._objects:
            if isinstance(obj, typ): objs.append(obj)
        return objs


    def hasObject(self, obj):
        """ This method will return C{True} if the given object is known as an
            grafical-object to the canvas. You can also use the overridden 
            operator C{in}."""
        return obj in self._objects


    def delObject(self, obj, auto_redraw=False):
        """ This method will remove the given object from list. 
            If C{auto_redraw} is C{True} it will redraw the canvas. """
        self._logger.debug("Remove %s from list"%id(obj))
        
        if not obj in self._objects: raise Exception("No object %s(%s) found in list"%(obj,id(obj)))
        if self._selected_object == obj: self._selected_object = None
        if self._mouse_over_object == obj: self._mouse_over_object = None
        if self._begin_drag_object == obj: self._begin_drag_object = None
        if sys.getrefcount(obj) > 2: self._logger.warning("Referencecount (%i) of object > 2!"%sys.getrefcount(obj))
        
        del self._objects[self._objects.index(obj)]
        if auto_redraw: self.redaw()


    def hitTest(self, coord):
        """ This methdo returns the first object in list, that is hit by the 
            given coordinates.
            @param coord: A (x,y) tuple specifies the coordinates of the 
                hit-test.
            @retrun: A L{gObejct} instance or C{None} if no object was hit."""
        for obj in self._objects:
            hobj = obj.hitTest( coord )
            if isinstance(hobj, gObject): return hobj


    def draw(self, dc):
        """ This method draws the canvas on the given DC. Note: You'll never 
            have to call this method directly. Normaly this will be done in 
            the redraw() method. If you need to call this method, please 
            obtain the DC by calling the beginDrawing() method and finalize it
            with the endDrawing() method. 
            @param dc: The drawing context to draw on. """
        for obj in self._objects:
            self._logger.debug("Draw object %s"%id(obj))
            obj.draw(dc)


    def getSelection(self):
        """ Returns the selected object """
        return self._selected_object


    def unsetSelection(self):
        """ Unset the selection. This method does NOT raise an 
            EVT_CAN_DESELECT. """
        self._selected_object = None


    def OnModified(self): pass


    ### tool-methods for emmiting events:
    def _emmitCanvasMouseEvent(self, coord):
        """ Tool-method to emmit EVT_CAN_MOUSE events.
            @param coord: Specifies a (x,y) tuple with the coordinates of the 
                mouse. """
        assert isinstance(coord, tuple)
        
        event = Events.CanvasMouseEvent(Events._event_can_mouse, self.GetId())
        event.SetCoordinates( coord )
        self.GetEventHandler().ProcessEvent(event)
        

    def _emmitMouseOver(self, coord, obj):
        """ Tool-method to emmit EVT_CAN_MOUSE_OVER events.
            @param coord: Specifies a (x,y) tuple with the coordinates of the 
                mouse. 
            @param obj: Specifies the the object under the mouse."""
        assert isinstance(coord, tuple)
        assert isinstance(obj, gObject)

        event = Events.CanvasMouseOver(Events._event_can_mouse_over, self.GetId())
        event.SetCoordinates( coord )
        event.SetObject( obj )
        self.GetEventHandler().ProcessEvent(event)


    def _emmitMouseLeft(self, coord, obj):
        """ Tool-method to emmit EVT_CAN_MOUSE_LEFT events.
            @param coord: Specifies a (x,y) tuple with the coordinates of the 
                mouse. 
            @param obj: Specifies the the object just left."""
        assert isinstance(coord, tuple)
        assert isinstance(obj, gObject)
        
        event = Events.CanvasMouseLeft(Events._event_can_mouse_left, self.GetId())
        event.SetCoordinates( coord )
        event.SetObject( obj )
        self.GetEventHandler().ProcessEvent(event)


    def _emmitCanvasClick(self, coord, obj):
        """ Tool-method to emmit EVT_CAN_CLICK events.
            @param coord: Specifies a (x,y) tuple with the coordinates of the 
                mouse. 
            @param obj: Specifies the the object clicked."""
        assert isinstance(coord, tuple)
        assert isinstance(obj, gObject)
        
        event = Events.CanvasClick(Events._event_can_click, self.GetId())
        event.SetCoordinates( coord )
        event.SetObject( obj )
        self.GetEventHandler().ProcessEvent(event)

    
    def _emmitCanvasDClick(self, coord, obj):
        """ This internal used tool-method emmits a EVT_CAN_DCLICK event. 
            @param coord: A (x,y) tuple specifies the coordinates of the mouse.
            @param obj: The object double-clicked. """
        assert isinstance(coord, tuple)
        assert isinstance(obj, gObject)
        
        event = Events.CanvasDClick(Events._event_can_dclick, self.GetId())
        event.SetCoordinates( coord )
        event.SetObject( obj )
        self.GetEventHandler().ProcessEvent(event)

    
    def _emmitCanvasRClick(self, coord, obj):
        """ This internal used tool-method emmits a EVT_CAN_RCLICK event. 
            @param coord: A (x,y) tuple specifes the coordinates of the mouse.
            @param obj: The right clicked object. """
        assert isinstance(coord, tuple)
        assert isinstance(obj, gObject)

        event = Events.CanvasRClick(Events._event_can_rclick, self.GetId())
        event.SetCoordinates( coord )
        event.SetObject( obj )
        self.GetEventHandler().ProcessEvent(event)

    
    def _emmitCanvasShowToolTip(self, coord, obj):
        """ This internal used tool-method emmits a EVT_CAN_SHOW_TOOLTIP 
            event. """
        assert isinstance(coord, tuple)
        assert isinstance(obj, gObject)

        event = Events.CanvasShowToolTip(Events._event_can_show_tool_tip, self.GetId())
        event.SetCoordinates( coord )
        event.SetObject( obj )
        self.GetEventHandler().ProcessEvent(event)
    
    
    def _emmitCanvasHideToolTip(self, coord):
        """ This internal used tool-method emmits a EVT_CAN_HIDE_TOOLTIP 
            event. 
            @param coord: A (x,y) tuple specifies the coordinates of the 
                mouse. (Not realy needed) """
        assert isinstance(coord, tuple)

        event = Events.CanvasHideToolTip(Events._event_can_hide_tool_tip, self.GetId())
        event.SetCoordinates( coord )
        self.GetEventHandler().ProcessEvent(event)
         
    
    def _emmitCanvasBeginDrag(self, coord, obj):
        """ This internal used tool-method emmits a EVT_CAN_BEGIN_DRAG 
            event. """
        assert isinstance(coord, tuple)
        assert isinstance(obj, gObject)
        self._logger.debug("Emmit begin-drag")
        self._dragging = True
        self._begin_drag_object = obj
        event = Events.CanvasBeginDrag(Events._event_can_begin_drag, self.GetId())
        event.SetCoordinates( coord )
        event.SetObject( obj )
        self.GetEventHandler().ProcessEvent(event)


    def _emmitCanvasDragging(self, coord):
        """ This internal used tool-method emmits a EVT_CAN_DRAGGING event. """
        assert isinstance(coord, tuple)

        event = Events.CanvasDragging(Events._event_can_dragging, self.GetId())
        event.SetCoordinates( coord )
        self.GetEventHandler().ProcessEvent(event)
    

    def _emmitCanvasEndDrag(self, coord, obj):
        """ This internal used tool-method emmits a EVT_END_DRAG event. """
        assert isinstance(coord, tuple)
        assert isinstance(obj, gObject)

        self._logger.debug("Emmit end-drag")
        event = Events.CanvasEndDrag(Events._event_can_end_drag, self.GetId())
        event.SetCoordinates( coord )
        event.SetObject( obj )
        self.GetEventHandler().ProcessEvent(event)
        self._dragging = False
        self._begin_drag_event = None

    
    def _emmitCanvasConnect(self, from_obj, to_obj):
        """ This internal used tool-method emmits a EVT_CAN_CONNECT event. """
        assert isinstance(from_obj, gObject)
        assert isinstance(to_obj, gObject)

        self._logger.debug("Emmit logging debug!")
        event = Events.CanvasConnectEvent(Events._event_can_connect, self.GetId())
        event.SetFrom( from_obj )
        event.SetTo( to_obj )
        self.GetEventHandler().ProcessEvent(event)

    
    def _emmitCanvasSelected(self, coord, obj):
        """ This internal used tool-method emmits a EVT_CAN_SELECT event.
            @param coord: This (x,y) tuple specifies the coordinates of the 
                mouse.
            @param obj: Specifies the selected object. """                
        assert isinstance(coord, tuple)
        assert isinstance(obj, gObject)

        evt = Events.CanvasSelectEvent(Events._event_can_select, self.GetId())
        evt.SetObject( obj )
        evt.SetCoordinates( coord )
        self.GetEventHandler().ProcessEvent(evt)

    
    def _emmitCanvasDeselected(self, coord, obj):
        """ This internal used tool-method emmits a EVT_CAN_DESELECT event.
            @param coord: This (x,y) tuple specifies the coordinates of the 
                mouse.
            @param obj: Specifies the unselected object. """                
        assert isinstance(coord, tuple)
        assert isinstance(obj, gObject)
        
        evt = Events.CanvasDeselectEvent(Events._event_can_deselect, self.GetId())
        evt.SetObject( obj )
        evt.SetCoordinates( coord )
        self.GetEventHandler().ProcessEvent(evt)


    ### wx.Window event-handler
    def _sc_OnMouseEvents(self, evt):
        coord = self._convertEventCoords(evt)
        if self._tool_tip_showed: self._emmitCanvasHideToolTip(coord)
        self._emmitCanvasMouseEvent(coord)
        evt.Skip()


    def _sc_OnLeftDown(self, evt):
        self._mouse_left_down = True  # needed for draggig 
        evt.Skip()
    

    def _sc_OnLeftUp(self, evt):
        coord = self._convertEventCoords(evt)
        obj = self.hitTest( coord )
        
        if self._dragging:
            if not obj: self._emmitCanvasEndDrag(coord, self._begin_drag_object)
            else: self._emmitCanvasEndDrag(coord, obj)
        
        if isinstance(obj, gObject):
            if not self._selected_object == obj:
                if self._selected_object and self.hasObject(self._selected_object):
                    self._emmitCanvasDeselected(coord, self._selected_object)
                self._selected_object = obj
                self._emmitCanvasSelected(coord, obj)
            self._emmitCanvasClick(coord, obj)
        elif self._selected_object:
            if self.hasObject(self._selected_object):
                self._emmitCanvasDeselected(coord, self._selected_object)
            self._selected_object = None

        self._mouse_left_down = False
        evt.Skip()


    def _sc_OnLeftDClick(self, evt):
        coord = self._convertEventCoords(evt)
        obj = self.hitTest( coord )

        if isinstance(obj, gObject):
            if not self._selected_object == obj:
                if self._selected_object and self.hasObject(self._selected_object):
                    self._emmitCanvasDeselected(coord, self._selected_object)
                self._selected_object = obj
                self._emmitCanvasSelected(coord, obj)
            self._emmitCanvasDClick(coord, obj)
        elif self._selected_object:
            if self.hasObject(self._selected_object):
                self._emmitCanvasDeselected(coord, self._selected_object)
            self._selected_object = None
        evt.Skip()


    def _sc_OnRightUp(self, evt):
        coord = self._convertEventCoords(evt)
        obj = self.hitTest( coord )
        
        if isinstance(obj, gObject):
            if not self._selected_object == obj:
                if self._selected_object and self.hasObject(self._selected_object):
                    self._emmitCanvasDeselected(coord, self._selected_object)
                self._selected_object = obj
                self._emmitCanvasSelected(coord, obj)
            self._emmitCanvasRClick(coord, obj)
        elif self._selected_object:
            if self.hasObject(self._selected_object):
                self._emmitCanvasDeselected(coord, self._selected_object)
            self._selected_object = None
        evt.Skip()


    def _sc_OnMotion(self, evt):
        coord = self._convertEventCoords(evt)
        obj = self.hitTest(coord)
        
        # handle dragging:
        if obj and self._mouse_left_down and not self._dragging:
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

    
    ### SimpleCanvas event handler
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
        if self._mouse_over_object:
            self._emmitCanvasShowToolTip(self._mouse_over_coord,
                                         self._mouse_over_object)
    
    def _sc_OnBeginDrag(self, evt):
        obj = evt.GetObject()
        if isinstance(obj, gObject):
            self._begin_drag_object = obj
        evt.Skip()

    def _sc_OnDragging(self, evt):
        if not isinstance(self._begin_drag_object, gMoveable):
            evt.Skip(); return
        pos  = evt.GetCoordinates()
        size = self._begin_drag_object.getSize()
        dc = self.beginDrawing()
        dc.Clear()
        SimpleCanvas.draw(self, dc)
        self.drawRectangle(dc, pos, size)
        self.endDrawing(dc)

    def _sc_OnEndDrag(self, evt):
        start_obj = self._begin_drag_object
        x,y = evt.GetCoordinates()
        
        # handle moveable objects (ie. Modules):
        if isinstance(start_obj, gMoveable):
            self._logger.debug("move object to %s,%s"%(x,y))
            # prevet to move to close to border
            (w,h) = start_obj.getSize()
            if x >= 2 and x+w<=198 and y>=2 and y+h<=198:
                # set position and redraw
                start_obj.setPosition(evt.GetCoordinates())
                self.redraw()
                self.OnModified()
        
        # handle connectable objects (ie. Pins):            
        elif isinstance(start_obj, gConnectable) \
          and not start_obj == evt.GetObject()   \
          and isinstance(evt.GetObject(), gConnectable):
            self._emmitCanvasConnect(start_obj, evt.GetObject())
            self.OnModified()
        
        # precess remaining handlers
        evt.Skip()
        self._begin_drag_object = None 

    def _sc_OnSelect(self, evt):
        self._logger.debug("Object selected -> draw")
        obj = evt.GetObject()
        dc = self.beginDrawing()
        obj.drawSelected(dc)
        self.endDrawing(dc)
        evt.Skip()

    def _sc_OnDeselect(self, evt):
        self._logger.debug("Object deselected -> redraw")
        obj = evt.GetObject()
        dc = self.beginDrawing()
        obj.draw(dc)
        self.endDrawing(dc)
        evt.Skip()





#
# Some interfaces. These interfaces should be used to implement grafical
# objects.
#
class gObject:
    """ Interface for all objects, that wants to be displayed. """
    _canvas      = None
    _logger      = None
    
    def __init__(self, canvas):
        """ This constructor will automaticly add itself to the given canvas.
            So if you derive from this class please also call allways this 
            constructor. 
            @param canvas: An instance of L{SimpleCanvas}. """
        
        self._logger = logging.getLogger("edef.dev")
        
        if not isinstance(canvas, SimpleCanvas):
            raise Exception("Bad type: Canvas should be a instance of SimpleCanvas. Got: %s"%type(canvas))
        self._canvas = canvas
        self._canvas.addObject(self)
        

    def getCanvas(self):
        """ Returns the canvas associated with the object. """
        return self._canvas


    def draw(self, dc):
        """ This method have to be overridden to implement darwing of the 
            object """
        pass
    

    def drawSelected(self, dc):
        """ This method will be called if the object will be selected. It may
            redraw the object in an other colour. """
        pass


    def hitTest(self, coordinates):
        """ This method have to be overridden. It should return self if it is
            hited by the given coordinates. """
        raise Exception("Not implemented yet")


    def toXML(self, dom):
        """ This method should be overridden! It should assemble and return an
            XML Element """
        raise Exception("Not implemented yet")




class gMoveable(gObject):
    """ Declares the object to be moveable! """
    _coordinates = None
    
    def __init__(self, canvas, coordinates):
        """ This constructor takes the canvas and the coordinates where the 
            object will be placed. This constructor will call the constuctor
            of L{gObject} so it will be automatcly added to the canvas. 
            @param canvas: The canvas associated this this object.
            @param coordinates: A (x,y) tuple spcifies the initial 
                coordinates. Can be reseted by the C{setPosition()} method.
            """
        self._coordinates = coordinates
        self._size = (0,0)
        gObject.__init__(self, canvas)
        

    def setPosition(self, coordinates):
        """ This method should be overridden! It should reset the internal 
            used coordinates (C{self._coordinates}). So if the module's draw()
            method is called, it will be drawn at the new position! """
        assert isinstance(coordinates, tuple)
        self._coordinates = coordinates

    def getPosition(self):
        """ Retunrn the current coordinates. """
        return self._coordinates


    def getSize(self):
        """ This method should return the size (width, height) of the 
            object. """
        return self._size

    def setSize(self, size):
        """ This method can be used to set the size. """
        assert isinstance(size, tuple)
        self._size = size



class gConnectable(gObject):
    """ This dummy class identifies the object als a grafical and connectable
        one. """
    def __init__(self, canvas):
        """ Dummy constructor. Simply calls the constructor of L{gObject}. """
        gObject.__init__(self, canvas)


