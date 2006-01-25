# ############################################################################ #
# This is part of the pyDCPU project. pyDCPU is a framework for industrial     # 
# communication.                                                               # 
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


# ChangeLog:
# 2005-12-09:
#   removed slots
# 2005-08-26:
#   add moveing symbols feature.
# 2005-08-25:
#   removed saving the non-existing typename in Symbol.ToXML()

import logging;
from Possession import Possession
import MasterObject
import Exceptions;


class Symbol:
    def __init__(self, Name, Connection, Address, Timeout, myPossession):
        self.__Logger = logging.getLogger("pyDCPU");
        self.__Valid = True;
        self.__Timeout = Timeout;
        self.__Address = Address;

        if not Name: raise Exceptions.Error("No name given!");
        #if not isinstance(Connection, (MasterObject.StreamConnection, MasterObject.SequenceConnection, MasterObject.ValueConnection) ): 
        #    raise Exceptions.Error("Invalid connection given: %s"%str(Connection));
        if not isinstance(myPossession, Possession): raise Exceptions.Error("No possesion object given.");
        self.__Name = Name;
        self.__Possession = myPossession;
        self.__Connection = Connection;

    def Rename(self, Name): self.__Name = Name;

    def Unregister(self): return(self.__Connection.close());

    def GetTypeName(self): return(self.__Connection.GetTypeName());
   
    def GetLastUpdate(self): return(self.__Connection.GetLastUpdate());

    def GetQuality(self): return self.__Connection.GetQuality();

    def GetValue(self, SessionID):
        self.__Logger.debug("Get value from (%s) ..."%self.__Name);
        if not self.__Possession.CanRead(SessionID): raise Exceptions.AccessDenied("Access denied for symbol %s"%self.__Name);
        return(self.__Connection.read_seq());

    def SetValue(self, Value, SessionID):
        self.__Logger.debug("Set value of (%s) to %s."%(self.__Name, str(Value)));
        if not self.__Possession.CanWrite(SessionID): raise Exceptions.AccessDenied("Access denied for symbol %s"%self.__Name);
        return(self.__Connection.write_seq(Value));

    def Read(self, Length, SessionID):
        if not self.__Possession.CanRead(SessionID): raise Exceptions.AccessDenied("Access denied for symbl %s"%self.__Name);
        self.__Logger.debug("Try to read %s bytes."%str(Length));
        if isinstance(self.__Connection, MasterObject.SequenceConnection): return self.__Connection.read_seq();
        elif isinstance(self.__Connection, MasterObject.StreamConnection): return self.__Connection.read(Length);
        raise Exceptions.Error("Can't read from connection (%s): use Get/SetValue instead."%str(self.__Connection));

    def Write(self, Data, SessionID):
        if not self.__Possession.CanWrite(SessionID): raise Exceptions.AccessDenied("Access denied for symbol %s"%self.__Name);
        if isinstance(self.__Connection,MasterObject.ValueConnection):
            raise Exceptions.Error("Can't read from connection: used Get/SetValue instead.");
        return self.__Connection.write(Data);
            
    def SetPossession(self, Possession): self.__Possession = Possession;

    def GetPossession(self): return(self.__Possession);
 
#END CLASS "SYMBOL"
