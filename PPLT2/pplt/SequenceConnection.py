""" This module only contains the class L{CSequenceConnection}.

    The sequence connection can be used if a module proviedes sequences of
    data, i.e. datagrams in opposit to the L{CStreamConnection}. To recive a
    datagram you have to call the C{recv()} method and to send you have to 
    call C{send()}. Additionaly the sequence-connection provide an interface 
    like a  stream-connection using an internal buffer. So you can call the
    C{read()} and C{write()} methods like a stream-connection. 
    
    B{Note:} There is also an asynchronious version of the sequence-connction
    that allows you to write modules simply, that operates completely
    asynchronious. 
    
    An example connection method of a module that provides datagrams could 
    look like:
    
    >>> def connect(self, addr, child=None):
    >>>     # --- maybe check the address...
    >>>     con = CSequenceConnection(self, child)
    >>>     self._d_connections.addConnection(con,addr)
    >>>     return con

    The C{self._d_connection} attribute is a L{ConnectionDatabase} instance 
    that every module has to store the connections.  
    
    An very simple example for a module that provide a sequence-connection:
    
    >>> from pplt import CModule, ISequenceModule, CSequenceConnection
    >>>
    >>> #
    >>> # a stupid demo random module:
    >>> #
    >>> class StupidRandom(CModule, ISequenceModule):
    >>>
    >>>     def connect(self, address, child=None):
    >>>         if self._d_connections.count(address) >0:
    >>>             raise Exception("There is already one connection with addr %s"%address)
    >>>         con = CSequenceConnection(self, child)
    >>>         self._d_connections.addConnection(con, address)
    >>>         return con
    >>>
    >>>
    >>>     def disconnect(self, con_id):
    >>>         self._d_connections.remConnection(con_id)
    >>>
    >>>
    >>>     def send(self, con_id, data):
    >>>         (con, addr) = self._d_connections.getConnectionByID(con_id)
    >>>         print "Connection with address %s send \"%s\" "%(addr,data)
    >>>
    >>>
    >>>     def recv(self, con_id):
    >>>         (con, addr) = self._d_connections.getConnectionByID(con_id)
    >>>         return "Hello, you are connected with address: %s"%addr
    >>>
    >>> 
    >>> mod = StupidRandom()
    >>>
    >>> con1 = mod.connect("#1")
    >>> con2 = mod.connect("#2")
    >>>
    >>> con1.send("Hello module...")
    Connection with address #1 send "Hello module..."
    >>>
    >>> print con2.recv()
    Hello, you are connected with address: #2
    >>>
    >>> print con1.read(5)
    Hello
    >>> print con1.recv()
    , you are connected with address: #1                                                                                                                                                        """

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
from Interfaces import ISequenceModule
import threading
import logging
import weakref


class CSequenceConnection (CConnection):
    """ The SequenceConnection can be used for datagram connections.
    
        To recive a datagram from a sequence-connection you have to call the 
        recv() method. Otherwise to send a message you have to call the send()
        method. Additional the SequenceConnection class provides an interface
        identical to the on of the StreamModule, so an inner-module that 
        requires a stream-connection can handle sequence-connections."""    
    _d_buffer = None
    _d_buffer_lock = None
    _d_event_threads = None


    def __init__(self, parent, child=None):
        """ The constructor takes two arguments. The parent specifies the 
            parent (destiantion) of the connection. This should be the module,
            that create the connection instance. The second (optional) 
            parameter child may specifiy the child (source) of the connection.
            The child have to inherit from L{IDisposable} class. This will be
            checked by the connection. The child have to implement the 
            notify_data() method to satisfy the interface definition of the
            L{IDisposable} interface. This method will be called by the 
            connection if there is "sudden" data for the child. This data
            will be stored into an internal buffer that will be obtained by
            the next recv() or read() call. 

            @param parent: The parent of the connection. This should be the 
                           module that created the connection.
            @type  parent: Any derived from L{ISequenceModule}                           
            @param child:  The child of the connection, normaly an other 
                           module. This instance will be notified about 
                           sudden data.
            @type child:   Any derived from L{IDisposable} """                           
        
        if not isinstance(parent, ISequenceModule):
            raise CorruptInterface("Need a SequenceModule as parent!")
        
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



    def read(self, length):
        """ This method acts like the read() method of a L{CStreamConnection}
            unsing the internal buffer. Therefore each module that needs a 
            L{CStreamConnection} from its parent can deal with 
            L{CSequenceConnection}. The parameter length specifies the max. 
            number of bytes returned by the read() method. The method will 
            return a string containing the obtained data on success or will 
            raise an exception on error. 
           
            B{Note:} Please reserve() and release() the parent module by 
            calling these methodes just bevore and after you to any IO! All 
            connections inherit these methods from the L{CConnection} class.

            @param length: Maximum number of bytes returned by the method.
            @type length: integer
            @return: String containing the obtained data """ 
        data = self.recv();

        self._d_buffer_lock.acquire()
        if length < len(data):
            self._d_buffer.insert(0,data[length:])
            data = data[:length];
        self._d_buffer_lock.release()
        return data


   
    def recv(self):
        """ This method will recieve a datagram from the parent of the 
            connection or will raise an exception on error.

            B{Note:} Please reserve() and release() the parent module by 
            calling these methodes just bevore and after you to any IO! All 
            connections inherit these methods from the L{CConnection} class.

            @return: String containing the message. """
        self._d_buffer_lock.acquire()

        if len(self._d_buffer) > 0:
            data = self._d_buffer.pop(0)
            self._d_buffer_lock.release()
            return data

        self._d_buffer_lock.release()
        
        if self.autolock():
            self._d_parent_module.reserve()
        
        try:
            data = self._d_parent_module.recv(self.identifier())
        finally:
            if self.autolock():
                self._d_parent_module.release()
        return data



    def write(self, data):
        """ This method simply calls the send() method. It exists to satisfy 
            the interface of a L{CStreamConnection} to allow a module that 
            expects a stream-connection to use a sequence-connection. This
            method will raise an exception on error.
            
            B{Note:} Please reserve() and release() the parent module by 
            calling these methodes just bevore and after you to any 
            IO! All connections inherit these methods from the 
            L{CConnection} class.

            @param data: The data to send.
            @type data: string """
        self.send(data)



    def send(self, data):
        """ This method sends the given string to the parent of the 
            connection. The method will raise an exception on error.
            
            B{Note:} Please reserve() and release() the parent module by 
            calling these methodes just bevore and after you to any IO! All 
            connections inherit these methods from the L{CConnection} class.

            @param data: The message to send.
            @type data: string """
        if self.autolock():
            self._d_parent_module.reserve()
        try:
            self._d_parent_module.send(self.identifier(), data)
        finally:
            if self.autolock():
                self._d_parent_module.release()
            


    def push(self, data):
        """ This method will be called by the parent module to notify the 
            child module. The parameter data holda the message for the child 
            this message will not be delivered directly to the child. The data
            will be first stroed into an internal buffer. If the child inherit
            from the L{IDisposable} class the child will be informed about the
            sudden data by calling its notify_data() method. Otherwise nothing
            happens and the data will be simply kept in the buffer until the 
            next read() or recv() method call. You can also disable the 
            notification by calling events_enabled(False).
            
            @param data: The message passed to the child.
            @type data: string"""
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
        """ Internal used method to release the parent module. Do not use this
            method directly. Please use the release() method."""
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
           
