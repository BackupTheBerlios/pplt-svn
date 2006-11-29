""" This module contains only the L{CStreamConnection} class. 
    The stream-connection will be used by modules that provide data streams.
    The connection will be created by the connection() method of the 
    destination (parent) module. The module have to implement the
    L{IStreamModule} interface otherwise you are not able to create a stream
    connection. So a sample connection method of a module can look like:
    
    >>> def connect(self, address, child=None):
    >>>     # do something usefull
    >>>     con = CStreamConnection(self, child)
    >>>     self._d_connections.addConnection(con, address)
    >>>     return con
    
    This example also shows the useage of the L{ConnectionDatabase}. This 
    connection table should be used to handle all connection of a modle.
    Look at the documentation of the L{CConnectionDatabase} class for more
    details."""
# ########################################################################## #
# StreamConnection.py
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


from Connection import CConnection
from Exceptions import PPLTError, CorruptInterface
from Interfaces import IStreamModule, IDisposable
import threading
import logging
import weakref


class CStreamConnection (CConnection):
    """ This class represents the connection between modules, dealing with 
        data streams. This connection provide the read(), write() methods for the
        child module and the push() method for the parent.

        A instance of this class will be created by the parent and will be 
        used by the child to access the parent (read/write) and also by the
        parent to notify the child about new (unexpected) data.
        
        This class also inherences the methods reserve() and release() from 
        the CConnection class. These methods have to be used to reserve the 
        module and to unable the events while accessing the parent. Also this
        class inherences the method autolock(). This method has a optional
        parameter. If the parameter is set with a boolean value the autolock
        mechanism will be enabled/disabled if no parameter is given, the 
        method will return the current state. But please be carefull with 
        enabling the autolock. If the autolock is enabled, the parent will
        be locked each time a read or write method will be called but only
        while the method is called. This can be usefull if all operations 
        consists of only 1 read or write method call. If not autolock will be
        the wrong way! """

    _d_buffer           = None
    _d_buffer_lock      = None
    _d_event_threads    = None


    def __init__(self, parent, child = None):
        """ This is the constructor of the CStreamConnection class. The 
            parameter "parent" have to be a instance of a class derived from 
            the CModule class. This instance will be handled as the parent of
            the connection. The optional parameter child defines the child of 
            the connection an have to be an instance of a class implementing 
            the IDisposable interface. If no child is give the events will be 
            disabled. """

        if not isinstance(parent, IStreamModule):
            raise CorruptInterface("The parent have to be a StreamModule!")

        if child != None and not isinstance(child, IDisposable):
            raise CorruptInterface("The child have to be a IDisposable!")

        CConnection.__init__(self, parent, child)

        self._d_buffer = ""
        self._d_buffer_lock = threading.Lock()
        self._d_event_threads = []



    def __del__(self):
        # joins all (running) event threads 
        for t in self._d_event_threads: t.join()
        del self._d_event_threads[0:]
        # call destructor of super-class
        CConnection.__del__(self)



    def read(self, length):
        """ This method can be called by the child to retrieve data from the 
            partent module. This method works with an internal buffer. Meaning
            if there is data left in the buffer, ie. by a push() call of the 
            patent while the events are disabled, this data will be returned 
            first. Only if the buffer is empty the parent module will be 
            called to retrieve new data. The parameter length specifies the 
            max. number of bytes retuned. """
        log = logging.getLogger("PPLT.core")

        if(self.autolock()):
            self._reserve()

        self._d_buffer_lock.acquire()
        if(len(self._d_buffer) > 0):
            log.debug("%i bytes left in buffer: return them!"%len(self._d_buffer))
            if length > len(self._d_buffer):
                length = len(self._d_buffer)
            data = self._d_buffer[0:length]
            self._d_buffer = self._d_buffer[length:]
            if self.autolock():
                self._release()
            self._d_buffer_lock.release()
            return data
        
        try:
            data = self._d_parent_module.read(self.identifier(), length)
        finally:
            self._d_buffer_lock.release()
            if(self.autolock()):
                self._release()
        return data



    def write(self, data):
        """ This method will be called by the child module to send data to the
            parent module. Because this operation is quiet simple the internal
            buffer will not be used. This method simply call the wirte() 
            method of the parent module. The parameter data specifies the 
            string of data send to the parent. This method returns the number 
            of byted send."""

        if self.autolock():
            self._reserve()

        try:
            l = self._d_parent_module.write(self.identifier(), data)
        finally:
            if(self.autolock()):
                self._release()
        return l

            

    def push(self, data, length=0):
        """ This method will be called by the parent module to push data up to
            the child module. This method will append the given data to the 
            internal buffer and will notify the child if the connection is 
            not reserved. Otherwise the data will be simply appended to the 
            buffer. The notified child module may obtain the data by calling 
            the read method of this class. Note: If there is data left in the
            buffer. The connection will retun it by the next read method. And 
            if the connection will be released holding data in buffer, there
            will be a thread created to notify the child about unexpected data
            in buffer."""

        if not isinstance(data,str):
            raise PPLTError("Parameter of push() have to be a string");
        
        self._d_buffer_lock.acquire();
        if(length != 0 and length < len(data)):
            data = data[0:length];

        self._d_buffer += data;
        self._d_buffer_lock.release();

        if(self._d_events_enabled):
            self._d_events_enabled = False;
            try:
                self._d_child_module.notify_data();
            finally:
                self._d_events_enabled = True;



    def flush(self):
        """ This method will flush the internal buffer. Use the method with
            care! You may destroy data that should be handled an an event. """
        self._d_buffer_lock.aquire();
        self._d_buffer = "";
        self._d_buffer_lock.release();



    def length(self):
        """ This method will return the number of bytes hold on buffer. """
        return len(self._d_buffer);
       


    def _release(self):
        """ Internal used method to reserve the connection and the destination
            module. Please do not use this method! Use the inhered method 
            release() instead. """
        CConnection._release(self);
                    
        if(len(self._d_buffer)>0 and self._d_events_enabled):
            # create a new thread that holds a weakref of self to process the left data.
            t = threading.Thread(target=CStreamConnection._start_event_thread,
                                 args=(weakref.proxy(self),));
            self._d_event_threads.append(t);
            t.start();



    def _start_event_thread(*args):
        """ This method will be used internally! NEVER call it directly! This
            method will simply call the notify_data() method of the child. 
            Normaly this method will be called by the new "event-thread" 
            created to handle data, left in buffer when the connection is 
            released! """
        if len(args) != 1:
            raise CorruptInterface("_start_evt_thread have to called with 1 arg!");
        (self,) = args;

        log = logging.getLogger("PPLT.core");
        log.debug("Starting event-thread...");

        self._d_events_enabled = False;
        
        try: self._d_child_module.notify_data();
        finally: self._d_events_enabled = True;

