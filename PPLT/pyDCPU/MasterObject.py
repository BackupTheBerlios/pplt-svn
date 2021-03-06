# ############################################################################ #
# This is part of the pyDCPU project. pyDCPU is a framework for industrial     # 
#   communication.                                                             # 
# Copyright (C) 2003-2005 Hannes Matuschek <hmatuschek@gmx.net>                # 
#                                                                              # 
# This library is free software; you can redistribute it and/or                # 
# modify it under the terms of the GNU Lesser General Public                   # 
# License as published by the Free Software Foundation; either                 #     
# version 2.1 of the License, or (at your option) any later version.           # 
#                                                                              # 
# This library is distributed in the hope that it will be useful,              # 
# but WITHOUT ANY WARRANTY; without even the implied warranty of               #     
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU             # 
# Lesser General Public License for more details.                              # 
#                                                                              # 
# You should have received a copy of the GNU Lesser General Public             # 
# License along with this library; if not, write to the Free Software          # 
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA    #
# ############################################################################ #

# CHANGELOG:
# 2006-03-29:
#   + more elegant way to lock a module
# 2006-01-14:
#   + fixed locking (should be now clear)
# 2005-12-08:
#   + added ValueConnection class

import xml.dom.minidom;
import pyDCPU;
from pyDCPU.Exceptions import *;    #import all Exceptions
import logging;
import traceback;
import sys;
import md5;
import time;
import thread;


class MasterConnection:
    """ This is the MasterConnection Object. The is the baseclass of
 classes like Stream, Sequence and ValueConnections. Please use these
 classes instead.  """

    def __init__(self, Parent, Address=None):
        self.Parent = Parent;
        self.Address = Address;
        self.AddrStr = None;
        self.Logger = logging.getLogger('pyDCPU');
        self.Buffer = None;
        self.Parent.inc_usage();
        self.TypeName = "undef";

    def close(self): 
        self.Parent.dec_usage();
        return(self.Parent.close());

    def read_seq(self): 
        self.Parent.lock();
        try: return self.Parent.read(self);     # finaly will be exec anyway
        finally: self.Parent.unlock();
        
    def write_seq(self, Data): 
        self.Parent.lock();
        try: return self.Parent.write(self, Data);
        finally: self.Parent.unlock();
        
    def read(self, Len=None): 
        self.Parent.lock();
        try: return self.Parent.read(self, Len);
        finally: self.Parent.unlock();

    def write(self, Data):
        self.Parent.lock();
        try: return self.Parent.write(self, Data);
        finally: self.Parent.unlock();

    def b_read(self,Len=None):
        return(self.read(Len));
    def b_read_seq(self):
        return self.read_seq();
    def b_write(self,Data):
        return(self.write(Data));
    def b_write_seq(self, Data):
        return self.write_seq(Data);

    def flush(self):
        #del self.Buffer;
        self.Buffer = None;
        self.Parent.lock();
        #self.Parent.flush();    #FIXME: maybe a bad idea
        self.Parent.unlock();
        return(True);

    def _GetAddrStr(self): return(self.AddrStr);
    def _SetAddrStr(self,Addr): self.AddrStr = Addr;
    def _GetFingerprint(self):
        """ This method is used internal. It create a fingerprint of this connection """
        ParentID = str(self.Parent._GetID());
        AddrStr  = str(self._GetAddrStr());
        return(md5.new(ParentID+AddrStr).hexdigest());  #uhh...
    def GetTypeName(self): return self.TypeName;
    def GetQuality(self): return "good";
    def GetLastUpdate(self): return time.time();


   

class StreamConnection(MasterConnection):
    """ CLASS: StreamConnection 
  This class implements the connection to or between modules that implements 
  streams. """
    def __init__(self, Parent, Address=None):
        MasterConnection.__init__(self, Parent, Address);
        self.TypeName = "Stream";

    def read_seq(self):
        self.Logger.warning("Trying to read a sequence out of a stream: will return only 1 byte.");
        self.Parent.lock();
        try: return self.Parent.read(1);
        finally: self.Parent.unlock();

    def write_seq(self, Data): return self.write(Data);

    def read(self, Len=None):
        self.Parent.lock();
        try: return self.Parent.read(self, Len);
        finally: self.Parent.unlock();

    def write(self, Data):
        self.Parent.lock();
        try: return self.Parent.write(self, Data);
        finally: self.Parent.unlock();





    
class SequenceConnection(MasterConnection):
    def __init__(self, Parent, Address = None):
        MasterConnection.__init__(self, Parent, Address);
        self.TypeName = "Sequence";

    def read_seq(self):
        if self.Buffer:
            tmp = self.Buffer;
            self.Buffer=None;
            return tmp;
        self.Parent.lock();
        # get data:
        try: return self.Parent.read(self);
        finally: self.Parent.unlock();

    def write_seq(self, Data): return self.write(Data);

    def read(self, Len=None):
        if self.Buffer==None:     #if buffer is empty -> fill up
            self.Parent.lock();
            try: self.Buffer = self.Parent.read(self, Len);
            finally: self.Parent.unlock();
        # if Len is not given:
        if not Len:
            tmp = self.Buffer;
            self.Buffer = None;
            return tmp;
        # if Len > len(Buffer): 
        if Len >= len(self.Buffer):
            tmp = self.Buffer;
            self.Buffer = None;
            return tmp;
        else:
            tmp = self.Buffer[:Len];
            self.Buffer = self.Buffer[Len:];
            return tmp;
       
        
    def write(self, Data):
        self.Parent.lock();
        try: return self.Parent.write(self, Data);
        finally: self.Parent.unlock();



class ValueConnection(SequenceConnection):
    """ A ValueConnection is the glue between the MasterObejcts and the symbols. """
    def __init__(self, Parent, Type, Address=None, Refresh = 0.0):
        SequenceConnection.__init__(self, Parent, Address);
        if not Type: raise Exception("A ValueConnection have to be typed!");
        self.Logger.debug("Init value-connection with ref.:%f and type: %s"%(float(Refresh),Type));
        self.TypeName = Type;
        self.LastUpdate = 0.0;
        self.Cache = None;
        self.Refresh = float(Refresh);
    
    def read_seq(self):
        # if a cache-time is set:
        if (self.Refresh > 0.0 and self.Cache != None):
            # if the cached value is still fresh:            
            if (time.time() - self.LastUpdate) < self.Refresh:
                self.Logger.debug("%f - %f < %f"%(time.time(), self.LastUpdate, self.Refresh));
                self.Logger.debug("Returning cached value(s). (Cachetime: %s)"%str(self.Refresh));
                return self.Cache;
        self.Logger.debug("Read \"new\" value(s) from module.");
        tmp = SequenceConnection.read_seq(self);
        if tmp:
            self.Cache = tmp;
            self.LastUpdate = time.time();
        return tmp;

    # only ValueConnections has timeout:
    def SetRefresh(self, Refresh): self.Refresh = float(Refresh);
        





        

class MasterObject:
    """ This is the Class of the Master-Object
  There are following functions:
      - __init__(Parameter)
      - destroy()

      - connect(Address)
      - close()

      - read(Connection, Data, Len)
      - write(Conection, Data, Len) """
    
    def __init__(self,ID, Connection, Parameters, Class, Logger):
        self.ID = ID;
        self.Connection = Connection;
        self.Class = Class;
        self.Counter = 0;
        if Parameters: self.Parameters = Parameters.copy();
        else: self.Parameters = None;
        self.Logger = logging.getLogger("pyDCPU");
        self.Lock   = thread.allocate_lock();

    def tear_down(self):
        if self.Connection: self.Connection.close();
        self.destroy();

    def inc_usage(self):
        self.Counter += 1;
    def dec_usage(self):
        self.Counter -= 1;


    def setup(self):
        pass;

    def destroy(self):
        return(True);
        
    def connect(self,Address):
        Connection = MasterConnection(self, Address);
        return(Connection);

    def close(self,Connection=None):
        return(True);

    def read(self, Connection, Len): pass;

    def write(self, Connection, Data): pass;

    def flush(self):
        self.Lock.release();
        return(True);
    
    def lock(self): return self.Lock.acquire();
    def unlock(self): return self.Lock.release();
    def islocked(self): return self.Lock.locked();

    def _GetID(self): return(self.ID);
    def _GetClass(self): return(self.Class);
    
    def _ToXMLNode(self, Document):
        """ This function creates a xml.dom.minidom.Node from the
            saved parameters """
        ObjNode = Document.createElement("Object");

        ObjNode.setAttribute('id',str(self._GetID()));
        ObjNode.setAttribute('class',str(self.Class));

        ConAddr = self._GetConnectionAddress();
        if ConAddr: ObjNode.setAttribute("addr",str(ConAddr));
            
        if self.Parameters:
            ParaList = self.Parameters.keys();
            for ParaName in ParaList:
                ParaNode = Document.createElement("Parameter");
                ParaNode.setAttribute("name",str(ParaName));
                ParaNode.setAttribute("value",str(self.Parameters[ParaName]));
                ObjNode.appendChild(ParaNode);
        return(ObjNode);
    
    def _GetConnectionAddress(self):
        """ This method return the Address used to connect with the Parent... (if any)"""
        if self.Connection: return(self.Connection._GetAddrStr());
        return(None);
