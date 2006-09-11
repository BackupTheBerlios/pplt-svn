# ########################################################################## #
# Connection.py
#
# 2006-09-01
# Copyright 2006 Hannes Matuschek
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


from Exceptions import PPLTError, CorruptInterface;
from Object import CObject;
from Module import CModule;
from Interfaces import IDisposable;
import logging;
import weakref;
from Tools import _fmtid;



class CConnection (CObject):
    """ This is the base class for all types of connections. This class 
        contains the basic functionanlity of a connection; Locking.

        This class provides the methods reserve() to reserve the connection 
        and also the parent of the connection. And release to release them.
        Also there is a method called autolock() this method can be used to 
        controll the autolock mechanism that can automaticly lock the 
        connection if the child excesses the connection. """

    _d_events_enabled   = None;
    _d_autolock         = None;
    _d_parent_module    = None;
    _d_child_module     = None;
    _d_event_status     = None;
    _d_logger           = None;


    def __init__(self, parent, child = None):
        """ Constructor. This method gets two parameters the parameter parent
            have to be a instance derived from CModule class and specifies the
            parent of the connection (the underlaying module). The optional 
            parameter child specifies the child of the connection. This should 
            be an instance of a class implementing the IDisposable interface. 
            This parameter specifies the child of the connection (the 
            module/symbol/what_ever) laying above the parent). A connection 
            instance should allway be created in the connection() method of a 
            module. """

        CObject.__init__(self);
        if not isinstance(parent, CModule):
            raise CorruptInterface("Parentmodule have to inherence CModule!");

        self._d_parent_module   = parent;
        self._d_autolock        = False;
        self._d_events_enabled  = True;
        self._d_event_status    = True;
        if child != None: self._d_child_module = weakref.proxy(child);
        else: self._d_child_module = None;
        self._d_logger          = logging.getLogger("PPLT.core");

        if(None == child): self._d_events_enabled = False;
        elif not isinstance(child, IDisposable):
            raise CorruptInterface("Child have to inherence IDisposable!");



    def __del__(self):
        if isinstance(self._d_parent_module, CModule): 
            self._d_parent_module.disconnect(self.Identifier());
        CObject.__del__(self);



    def reserve(self):
        """ This method will reserve the connection and also the parent of the 
            connection. This method should called bevore any interaction will
            be done. And release() should be called after all interactions.
            Unless you have enabled the autolock mechanism! Which is disabled 
            by default. 
            
            This method will also disable all events for this connection. So
            if the parent will emmit an event for this connection, this child
            will not be notified. Instead the event will be buffered unless 
            the release method is called."""
        if(self._d_autolock):
            self._d_logger.warn("Autolock enabled AND reserve called: This may cause into a deadlock!");
        self._reserve();



    def _reserve(self): 
        self._d_logger.debug("Reserve Connection! Disable events and save eventstate: %s"%self._d_events_enabled);
        self._d_event_status = self._d_events_enabled;
        self._d_events_enabled = False;
        self._d_parent_module.reserve();



    def release(self):
        """ This method will release the parent module and this connection.
            Also it will restore the event status. If there where unhandled 
            events they may emmited again to the child (depending of the 
            type of the connection). """ 
        if(self._d_autolock):
            self._d_logger.warn("Autolock enabled AND release() called!");
        self._release();



    def _release(self):
        self._d_logger.debug("Release connenction. Restore eventstate: %s"%self._d_events_enabled);
        self._d_events_enabled = self._d_event_status;
        self._d_parent_module.release();



    def autolock(self, status = None):
        """ This method will return the current status of the autolock 
            mechanism if no parameters is given. Other wise if the parameter 
            is  Ture the autolock mechanism will be enabled and if False it
            will be disabled. Please be care full using the autolock. Only
            if you are sure that all operations will consist of only on 
            methodcall to parent this may an option for you. """
        if(status == None): return self._d_autolock;
        if(not status in [True, False]):
            raise PPLTError("Only boolean values are allowed as parameters for autolock()");
        self._d_logger.info("Autolocking changed to %s for connetion %s!"%(status, _fmtid(self.Identifier())));
        self._d_autolock = status;
        return None;
           
        
