""" This file defines the L{ElementMap} class. This class extends the 
    L{Canvas} class to deal with edef-modules. """


# ########################################################################## #
# ElementMap.py
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
from ElementMapObjects import emModule, emConnection
from Canvas import Canvas, coConnection
import Events
import edef
from edef.dev import Tools


class ElementMap( Canvas ):
    _importer = None

    def __init__(self, parent, ID):
        Canvas.__init__(self, parent, ID)
        
        self._importer = edef.Importer()
        
        self._selected_object = None

        self.Bind( Events.EVT_CAN_RCLICK, self.OnConRightClick)
        self.Bind( Events.EVT_CAN_RCLICK, self.OnModRightClick)
        self.Bind( Events.EVT_CAN_CONNECT, self.OnCanConnect)
        

    def loadModule(self, uri, x, y, params=None): #FIXME handle params
        self._logger.debug("load module %s @ (%s %s)"%(uri, x,y))
        
        (proto, path) = Tools.splitURI(uri)
        name = ".".join(path.split("/"))

        self._logger.debug("Get prameter for module %s"%name)
        (path, meta) = self._importer.getModuleMeta(name)
        
        if len(meta.getParameters()) > 0:
            param_dialog = ParameterDialog(self, -1, name)
            if not wx.ID_OK == param_dialog.ShowModal():
                self._logger.info("Module load aborted!")
                param_dialog.Destroy()
                return
            params = param_dialog.parameters
            param_dialog.Destroy()
        else:
            params = dict()

        self._logger.debug("Instance and place module with params: %s"%params)
        mod = self._importer.loadGrafical(self, (x,y), name, params)
        self.redraw()
        self.OnModified()
        return mod


    def delObject(self, obj):
        self._logger.debug("Delete object: %s"%id(obj))
        if isinstance(obj, emModule):
            cons  = self.getConnectionsFrom(obj)
            for con in self.getConnectionsTo(obj):
                if not con in cons: cons.append(con)
            for con in cons: self.delObject( con )
        Canvas.delObject( self, obj )
        self.OnModified()   #
   

    def connect(self, frm, to, auto_redraw=False):
        if self.isConnection(frm, to): return
        con = emConnection(frm,to)
        if auto_redraw: self.redraw()
        self.OnModified()   #
        return con
   
    
    def isConnection(self, frm, to):
        connections = self.getObjects( coConnection )
        for con in connections:
            if (frm, to) == (con.getFrom(), con.getTo()):
                return True
        return False


    def getConnectionsFrom(self, obj):
        lst = []
        connections = self.getObjects( coConnection )
        for con in connections:
            if obj == con.getFrom().getModule(): lst.append(con)
        return lst


    def getConnectionsTo(self, obj):
        lst = []
        connections = self.getObjects( coConnection )
        for con in connections:
            if obj == con.getTo().getModule(): lst.append(con)
        return lst


    def OnConRightClick(self, evt):
        if not isinstance(evt.GetObject(), emConnection):
            evt.Skip()
            return

        _id_remove = wx.NewId()
        _ctx_menu = wx.Menu()
        _ctx_menu.Append(_id_remove, "remove connection")
        self.Bind(wx.EVT_MENU, self.OnRemove, id=_id_remove)
        
        self.PopupMenu(_ctx_menu)
        evt.Skip()


    def OnModRightClick(self, evt):
        if not isinstance(evt.GetObject(), emModule):
            evt.Skip()
            return
        _id_remove = wx.NewId()
        _ctx_menu = wx.Menu()
        _ctx_menu.Append(_id_remove, "remove module")
        self.Bind(wx.EVT_MENU, self.OnRemove, id=_id_remove)
        
        self.PopupMenu(_ctx_menu)
        evt.Skip()


    def OnCanConnect(self, evt):
        # FIXME check if connect from "out" to "in"
        self.connect(evt.GetFrom(), evt.GetTo(), True)
        evt.Skip()


    def OnRemove(self, evt):
        self.delObject(self.getSelection())
        self.unsetSelection()
        self.redraw()


    def OnModified(self):
        """ This method will be called if the circuit will be modified. """
        pass




class ParameterDialog(wx.Dialog):
    def __init__(self, parent, ID, name):
        wx.Dialog.__init__(self, parent, ID, "Parameter for module %s"%name)
        self._params = dict()
        self.parameters = dict()
        
        self._importer = edef.Importer()
        (path, meta) = self._importer.getModuleMeta(name)
        params = meta.getParameters()

        box = wx.BoxSizer(wx.VERTICAL)


        for (param, default) in params:
            if not default: default = ""
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            label = wx.StaticText(self, -1, param)
            inp   = wx.TextCtrl(self, -1, default, size=(100,-1))
            self._params[param] = inp
            hbox.Add(label, 1, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.LEFT, 3)
            hbox.Add(inp,   1, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.RIGHT, 3)
            box.Add(hbox, 0, wx.EXPAND)
        
        btnbox = self.CreateStdDialogButtonSizer(wx.OK|wx.CANCEL)
        box.Add(btnbox, 0, wx.GROW|wx.ALL, 5)
        
        self.Bind(wx.EVT_BUTTON, self.OnOK, id=wx.ID_OK)

        self.SetSizer(box)
        box.Fit(self)


    def OnOK(self, evt):
        for (name, tctrl) in self._params.items():
            value = tctrl.GetValue()
            if not value.strip() == "":
                self.parameters[name] = value
        self.EndModal(wx.ID_OK)



