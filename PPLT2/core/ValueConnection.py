# ########################################################################## #
# ValueConnection.py
#
# 2006-11-23
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

from Connection import CConnection
from Exceptions import CorruptInterface
from Interfaces import IValueModule
import threading
import logging
import weakref


class CValueConnection (CConnection):
    
    _d_buffer = None
    _d_buffer_lock = None
    _d_event_threads = None


    def __init__(self, parent, child=None):
        if not isinstance(parent, IValueModule):
            raise CorruptInterface("Need a ValueModule as parent!")
        
        CConnection.__init__(self, parent, child)
            
        self._d_buffer = []
        self._d_buffer_lock = threading.Lock()
        self._d_event_threads = []



    def __del__(self):
        # joins all (running) event threads 
        for th in self._d_event_threads:
            th.join()
        
        del self._d_event_threads[0:]
        
        # call destructor of super-class
        CConnection.__del__(self)

   
    def get(self):
        self._d_buffer_lock.acquire()

        if len(self._d_buffer) > 0:
            data = self._d_buffer.pop(0)
            self._d_buffer_lock.release()
            return data

        self._d_buffer_lock.release()
        
        if self.autolock():
            self._d_parent_module.reserve()
        
        try:
            data = self._d_parent_module.get()
        finally:
            if self.autolock():
                self._d_parent_module.release()
        return data


    def set(self, data):
        if self.autolock():
            self._d_parent_module.reserve()
        try:
            self._d_parent_module.set(self.identifier(), data)
        finally:
            if self.autolock():
                self._d_parent_module.release()
            


    def push(self, data):
        # store new data in buffer:
        self._d_buffer_lock.acquire()
        self._d_buffer.append(data)
        self._d_buffer_lock.release()

        
        if self._d_events_enabled:
            self._d_logger.debug("Events are enabled -> notify child")
            # disable events
            evt_stat = self._d_events_enabled;
            self._d_events_enabled = False
            # call notify_data of child and ensure that the events 
            # are restored
            try:
                self._d_child_module.notify_data()
            finally:
                self._d_events_enabled = evt_stat



    def _release(self):
        CConnection._release(self)
        if self._d_events_enabled and len(self._d_buffer)>0:
            # create a new thread that holds a weakref of self to process the 
            # left data.
            t = threading.Thread(target=CSequenceConnection._start_event_thread,
                                 args=(weakref.proxy(self),))
            self._d_event_threads.append(t)
            t.start()



    def _start_event_thread(*args):
        """ This method will be used internally! NEVER call it directly! This
            method will simply call the notify_data() method of the child. 
            Normaly this method will be called by the new "event-thread" 
            created to handle data, left in buffer when the connection is 
            released! """
        if len(args) != 1:
            raise CorruptInterface("_start_evt_thread needs only one arg!")
        (self,) = args

        log = logging.getLogger("PPLT.core")
        log.debug("Starting event-thread...")

        evt_stat = self._d_events_enabled
        self._d_events_enabled = False
        
        try:
            self._d_child_module.notify_data()
        finally:
            self._d_events_enabled = evt_stat
           
