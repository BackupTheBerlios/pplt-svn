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

class SlaveStream:
    """ A instance of this will be returned from the parent... """
    def __init__():
        pass;
    def write():
        pass;
    def read():
        pass;
    def pwrite():
        pass;
    def length():
        pass;
    def overun():
        pass;
    def flush():
        pass;

    def _GetAddressString(self):
        pass;
    

class SlaveHandler:
    """ A instance of this will be given to the parent... """;
    def __init__(self, ChildObj):
        pass;
    def write():
        pass;



class Object:
    def __init__(self, Stream, Parameters, Class):
        self.Stream = Stream;
        self.Parameters = Parameters;
        self.Class = Class;
        self._ConnectionAddressString = Stream._GetAddressString();
        self._HandlerSet = SlaveHandlerSet();
        self.Logger = logging.getLogger('pyDCPU');
        
    def setup():
        pass;

    def newdata(self):
        """ This method will be called by the parent
            to tell you that there is new data in the
            stream
        """
        pass;
    
    def write(self):
        """ This mwthod will be called by the children indirect
            to return data that have to be send...
        """
        pass;
    
    def register(self, AddressStr, Handler):
        """ This method must convert Address-String into a
            format you understand. Then add handler to set
            (use self._add2set(Handler, newAddress)).
        """
        pass;
    
    def unregister(AddressStr):
        pass;
    
    def _add2set(self, Handler, Address):
        if not self._HandlerSet.Add(Handler):
            return(False);
        return(True);

    def _delhdl(self,Address):
        if not self._HandlerSet.Del(Address):
            return(False);
        return(True);

    def _GetID(self):
        pass;
    def _ToXMLNode(self):
        pass;
