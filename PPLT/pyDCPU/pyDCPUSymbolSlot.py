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

#Revision:
# 2005-02-06
#   + caching

import pyDCPUConverter;
import pyDCPU;
import time;
import binascii;


class SymbolSlot:
    """
        A Dummy Class...
    """
    pass;





class MasterSlot(SymbolSlot):
    """ This Class represents a SymbolSlot for the Master Tree.
            It takes care of type cast.
            :::Cashing:::(default 0.5sec)
    """
    
    def __init__(self, Connection, ID, TypeName, Logger, TimeOut=0.5):
        if not Logger:
            return(None);
        self.__Logger = Logger;

        self.Class = "[MasterSymbolSlot]";
        self.Parameters=None;
        self.ID = ID;
        self.TypeName = TypeName;
        self.TimeOut = TimeOut;
        self.LastReadData = None;
	if TimeOut == 0.0:
	    self.LastReadUpdate = None;
	else:
    	    self.LastReadUpdate = time.time()-0.5;
       
        self.__Logger.info("Setup symbol-slot for master tree");
        if not Connection:
            self.__Logger.warning("Error: No active conncetion for me...");
            return(None);
        self.__Connection = Connection;

        if not TypeName:
            self.__Logger.warning("No Type!!! Need a type..");
            return(None);

        self.__Converter = pyDCPUConverter.Converter(TypeName);
        if not self.__Converter.GetState():
            self.__Logger.error("Error while create Converter...");
            return(None);

        

    def destroy(self):
        self.__Logger.warning("clean destroy not implemented: Mail the author..");
        return(True);
        

    def GetValue(self):
        if not self.__Connection:
            self.__Logger.warning("No Connection->No Value");
            return(None);
	if self.LastReadUpdate == None:
            try:
                self.LastReadData = self.__Connection.read(self.__Converter.GetSize());
            except:
                self.__Logger.error("error while read from object");
                return(None);
	    
        elif (self.LastReadUpdate+self.TimeOut)<=time.time():
            self.__Logger.debug("Update data...");
            try:
                self.LastReadUpdate = time.time();
                self.LastReadData = self.__Connection.read(self.__Converter.GetSize());
            except:
                self.__Logger.error("error while read from object");
                return(None);
        else:
            self.__Logger.debug("return cached data");
        try:
            return(self.__Converter.ConvertToValue(self.LastReadData));
        except:
            self.__Logger.error("Error while convert to value: maybe wrong data format");
            return(None);

        

    def SetValue(self, Value):
        if not self.__Connection:
            self.__Logger.error("No Connection->no write");
            return(False);
        try:
            Data = self.__Converter.ConvertToData(Value);
        except:
            Data = None;
            
        if not Data:
            self.__Logger.error("Error while convert value to data");
            return(False);
	self.__Logger.debug("SetData: %s"%(binascii.b2a_hex(Data)));

        try:
            length = self.__Connection.write(Data);
            if length != len(Data):
                self.__Logger.warning("retuned length != len(data): bad written modle???");
                self.__Logger.debug("DATA: %i SEND: %i"%(len(Data),length));
        except pyDCPU.IOModError:
            self.__Logger.error("IO error returned from Parent");
            self.__Connection.flush();
            return(False);
        except pyDCPU.LockModError:
            self.__Logger.error("One parent is locked");
            return(False);
        except pyDCPU.ModError:
            self.__Logger.error("?-error");
        except:
            self.__Logger.error("Python exception???");
            return(False);
        return(True);
    

    def read(self, Length):
        try:
            retVal = self.__Connection.read(Length);
        except:
            self.__Logger.error("Error while read from Parent");
            raise(pyDCPU.IOModError);
        return(retVal);
    

    def write(self, Data):
        try:
            retVal = self.__Connection.write(Data);
        except:
            self.__Logger.error("Error while write to parent");
            raise(pyDCPU.IOModError);
        return(retVal);


    def connect(self, Address):
        CON = pyDCPU.MasterConnection(self, None);
        return(CON);


    def close(self, Connection=None):
        return(True);
    

    def _GetID(self):
        return(self.ID);


    def _GetClass(self):
        return(self.Class);
    

    def _ToXMLNode(self, Document):
        """ This function creates a xml.dom.minidom.Node from the
            saved parameters """
        ObjNode = Document.createElement("Object");

        ObjNode.setAttribute("id",str(self._GetID()));
        ObjNode.setAttribute("class",str(self.Class));
        ObjNode.setAttribute("type",str(self.TypeName));
        ObjNode.setAttribute("timeout",str(self.TimeOut));
        
        ConAddr = self._GetConnectionAddress();
        if ConAddr:
            ObjNode.setAttribute('addr',str(ConAddr));

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
        if self.__Connection:
           return(self.__Connection._GetAddrStr());
        return(None);
    
