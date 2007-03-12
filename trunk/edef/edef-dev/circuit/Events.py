""" This file defines all events emmitted by the canvases. """

# ########################################################################## #
# Events.py
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


#
# Canvas Events:
#
class CanvasEvent(wx.PyCommandEvent):
    _coords = (0,0)
    def __init(self, evtType, ID):
        wx.PyCommandEvent.__init__(self, evtType, ID)
    def SetCoordinates(self, coords): self._coords = coords
    def GetCoordinates(self): return self._coords

class CanvasConnectEvent(wx.PyCommandEvent):
    _from, _to = None, None
    def __init(self, evtType, ID):
        wx.PyCommandEvent.__init__(self, evtType, ID)
    def SetFrom(self, obj): self._from=obj
    def SetTo(self, obj): self._to=obj
    def GetFrom(self): return self._from
    def GetTo(self): return self._to

class CanvasObjectEvent(CanvasEvent):
    _obj = None
    def SetObject(self, obj): self._obj=obj
    def GetObject(self): return self._obj

class CanvasMouseEvent(CanvasEvent): pass 
class CanvasClick(CanvasObjectEvent): pass
class CanvasDClick(CanvasObjectEvent): pass
class CanvasRClick(CanvasObjectEvent): pass
class CanvasMouseOver(CanvasObjectEvent): pass
class CanvasMouseLeft(CanvasObjectEvent): pass
class CanvasShowToolTip(CanvasObjectEvent): pass
class CanvasHideToolTip(CanvasEvent): pass
class CanvasBeginDrag(CanvasObjectEvent): pass
class CanvasDragging(CanvasEvent): pass
class CanvasEndDrag(CanvasObjectEvent): pass
class CanvasSelectEvent(CanvasObjectEvent): pass
class CanvasDeselectEvent(CanvasObjectEvent): pass

_event_canvas               = wx.NewEventType()
_event_can_mouse            = wx.NewEventType()
_event_can_click            = wx.NewEventType()
_event_can_dclick           = wx.NewEventType()
_event_can_rclick           = wx.NewEventType()
_event_can_mouse_over       = wx.NewEventType()
_event_can_mouse_left       = wx.NewEventType()
_event_can_show_tool_tip    = wx.NewEventType()
_event_can_hide_tool_tip    = wx.NewEventType()
_event_can_begin_drag       = wx.NewEventType()
_event_can_dragging         = wx.NewEventType()
_event_can_end_drag         = wx.NewEventType()
_event_can_connect          = wx.NewEventType()
_event_can_select           = wx.NewEventType()
_event_can_deselect         = wx.NewEventType()

EVT_CANVAS              = wx.PyEventBinder(_event_canvas, 1)
EVT_CAN_MOUSE           = wx.PyEventBinder(_event_canvas, 1)
EVT_CAN_CLICK           = wx.PyEventBinder(_event_can_click, 1)
EVT_CAN_DCLICK          = wx.PyEventBinder(_event_can_dclick, 1)
EVT_CAN_RCLICK          = wx.PyEventBinder(_event_can_rclick, 1)
EVT_CAN_MOUSE_OVER      = wx.PyEventBinder(_event_can_mouse_over, 1)
EVT_CAN_MOUSE_LEFT      = wx.PyEventBinder(_event_can_mouse_left, 1)
EVT_CAN_SHOW_TOOL_TIP   = wx.PyEventBinder(_event_can_show_tool_tip, 1)
EVT_CAN_HIDE_TOOL_TIP   = wx.PyEventBinder(_event_can_hide_tool_tip, 1)
EVT_CAN_BEGIN_DRAG      = wx.PyEventBinder(_event_can_begin_drag, 1)
EVT_CAN_DRAGGING        = wx.PyEventBinder(_event_can_dragging, 1)
EVT_CAN_END_DRAG        = wx.PyEventBinder(_event_can_end_drag, 1)
EVT_CAN_CONNECT         = wx.PyEventBinder(_event_can_connect, 1)
EVT_CAN_SELECT          = wx.PyEventBinder(_event_can_select, 1)
EVT_CAN_DESELECT        = wx.PyEventBinder(_event_can_deselect, 1)

