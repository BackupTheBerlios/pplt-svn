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

import xml.dom.minidom;
import pyDCPU;
import logging;
import traceback;
import sys;

class MasterConnection:
    """ This is the Connection Object,
            it handels the Connection Data like a non string
            representation of the Address...
    """
    def __init__(self, Parent, Address=None):
        self.Parent = Parent;
        self.Address = Address;
        self.AddrStr = None;
        self.Logger = logging.getLogger('pyDCPU');
        
    def close(self):
        return(self.Parent.close());

    def read(self, Len):
        if self.Parent.islocked():
            raise(pyDCPU.LockModError);
        self.Parent.lock();

        try:
            Data = self.Parent.read(self, Len);
        except pyDCPU.LockModError:
            self.Logger.error("Object locked");
            raise(pyDCPU.LockModError);
        except pyDCPU.IOModError:
            self.Logger.error("IOError");
            self.Parent.unlock();
            raise(pyDCPU.IOModError);
        except pyDCPU.ReadOnlyModError:
            self.Logger.error("Object read only");
            self.Parent.unlock();
            raise(pyDCPU.ReadOnlyModError);
        except:
            self.Logger.error("Unkown error");
            traceback.print_exc()
            self.Parent.unlock();
            raise(pyDCPU.FatIOModError);
        self.Parent.unlock();
        return(Data);
        
    def write(self, Data):
        if self.Parent.islocked():
            raise(pyDCPU.LockModError);
        self.Parent.lock();

        try:
            Len = self.Parent.write(self, Data);
        except pyDCPU.LockModError:
            raise(pyDCPU.LockModError);
        except pyDCPU.IOModError:
            self.Parent.unlock();
            raise(pyDCPU.IOModError);
        except pyDCPU.ReadOnlyModError:
            self.Parent.unlock();
            raise(pyDCPU.ReadOnlyModError);
        except:
            self.Parent.unlock();
            raise(pyDCPU.FatIOModError);

        self.Parent.unlock();
        return(Len);

    def b_read(self,Len):
        while(self.Parent.islocked()):
            pass;
        return(self.read(Len));

    def b_write(self,Data):
        while(self.Parent.islocked()):
            pass;
        return(self.write(Data));
    
    def flush(self):
        self.Parent.lock();
        self.Parent.flush();
        self.Parent.unlock();
        return(True);

    def _GetAddrStr(self):
        return(self.AddrStr);
    def _SetAddrStr(self,Addr):
        self.AddrStr = Addr;
        
class MasterObject:
    """ This is the Class of the Master-Object
        There are following functions:
            - __init__(Parameter)
            - destroy()

            - connect(Address)
            - close()

            - read(Connection, Data, Len)
            - write(Conection, Data, Len)
    """
    
    def __init__(self,ID, Connection, Parameters, Class, Logger):
        self.ID = ID;
        self.Connection = Connection;
        self.Class = Class;
        self.Counter = 0;
        if Parameters:
            self.Parameters = Parameters.copy();
        else:
            self.Parameters = None;
        self.Logger = Logger;
        self.Lock   = False;

    def setup(self):
        pass;

    def destroy(self):
        if self.Connection:
            self.Connection.close();
        return(True);

    def preconnect(self):
        self.Counter += 1;
        return(True);
    
    def connect(self,Address):
        Connection = MasterConnection(self, Address);
        return(Connection);

    def close(self,Connection=None):
        return(True);

    def read(self, Connection, Len):
        pass;

    def write(self, Connection, Data):
        pass;

    def flush(self):
        self.unlock();
        return(True);
    
    def lock(self):
        self.Lock = True;
        return(True);
    def unlock(self):
        self.Lock = False;
        return(True);
    def islocked(self):
        return(self.Lock);

    def _GetID(self):
        return(self.ID);
    def _GetClass(self):
        return(self.Class);
    
    def _ToXMLNode(self, Document):
        """ This function creates a xml.dom.minidom.Node from the
            saved parameters """
        ObjNode = Document.createElement("Object");

        ObjNode.setAttribute('id',str(self._GetID()));
        ObjNode.setAttribute('class',str(self.Class));

        ConAddr = self._GetConnectionAddress();
        if ConAddr:
            ObjNode.setAttribute("addr",str(ConAddr));
            
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
        if self.Connection:
           return(self.Connection._GetAddrStr());
        return(None);
