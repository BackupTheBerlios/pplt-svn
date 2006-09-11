# ########################################################################## #
# AsyncStreamConnection.py
#
# 2006-09-08
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


from StreamConnection import CStreamConnection;
from Exceptions import PPLTError, ItemBusy;
import threading;
import logging;
from Tools import _fmtid;

class CAsyncStreamConnection (CStreamConnection):
    """ The CAsyncStreamConnection has the same interface like the 
        CStreamConnection but it can be used by a module, that works complete
        asynchronious. That means the parent module of this connection doesn't
        need to implement the read() method beause it will never be called.
        Instead the parent will push() all data. If a child calls the read()
        method of this class, it will block until the parent pushes data or
        it returns immediately if there was data left in the internal buffer.
        If there is no child waiting, the push() method will behave like the
        one of the StreamConncetion, it will call the notify_data() method of
        the child. All other methods like write(), reserve(), release(), ...
        are inherited from the CStreamConnection class. 
        
        Because the PPLT mixes synchronious and asynchronious communication,
        implementing interfacemodules, that deals with hardware or with the 
        os can become hard. Therefor this connection can be usefull if you 
        want to implement a interfacemodule. I.e. a socket module, that waits
        in a seperate thread for new incoming data and push()es it. In the 
        opposite direction the write() method will simply write the data into 
        the socket.  """
    _d_condition    = None;
    _d_timeout      = None;
    _d_logger       = None;

    def __init__(self, parent, child = None, timeout = 1.0):
        CStreamConnection.__init__(self, parent, child);
        self._d_condition = threading.Condition(self._d_buffer_lock);
        self._d_timeout = timeout;
        self._d_logger  = logging.getLogger("PPLT.core"); 


    def read(self, length):
        self._d_logger.debug("Try to read %i bytes..."%length);
        self._d_condition.acquire();
   
        if self.autolock(): self._reserve();

        if len(self._d_buffer)>0:
            self._d_logger.debug("return data (%i bytes) left in buffer..."%len(self._d_buffer));
            if length > len(self._d_buffer): length = len(self._d_buffer);
            data = self._d_buffer[0:length];
            self._d_buffer = self._d_buffer[length:];

            if self.autolock(): self._release();
            self._d_condition.release();
            return data;

        self._d_condition.wait(self._d_timeout);                    
        if len(self._d_buffer)==0:
            raise ItemBusy("Timeout while read from asyc source! (in %s)"%_fmtid(self.Identifier()));

        if length > len(self._d_buffer): length = len(self._d_buffer);
        data = self._d_buffer[0:length];
        self._d_buffer = self._d_buffer[length:];
        
        if self.autolock(): self._release();
        self._d_condition.release();
        return data;


    
    def push(self, data, length=0):
        if not isinstance(data, str):
            raise PPLTError("push() requires string as argument!");
        
        self._d_logger.debug("Push (%i bytes from %i)"%(length, len(data)));
        
        self._d_condition.acquire();
       
        if length>len(data): length = len(data);
        if length>0: data = data[0:length];
        self._d_buffer += data;
        
        if self._d_events_enabled: 
            self._d_condition.release();
            self._d_child_module.notify_data();
            return;
        
        self._d_condition.notify();
        self._d_condition.release();
