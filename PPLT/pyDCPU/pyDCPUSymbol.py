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


import pyDCPUSymbolSlot
import pyDCPUConverter;
import UserDB;


Valid_Type_Names = ['Bool','Byte','Word','DWord','Float','Double','String'];



class Symbol:
    def __init__(self, Name, SymbolSlot, TypeName, Possession, Logger):
        self.__Logger = Logger;
        self.__Valid = True;
        if not Name:
            self.__Logger.error("No symbolname given");
            self.__Valid = False;
        if not isinstance(SymbolSlot, pyDCPUSymbolSlot.SymbolSlot):
            self.__Logger.error("No symbolslot given");
            self.__Valid = False;
        if not Valid_Type_Names.count(TypeName):
            self.__Logger.error("Bad Type");
            self.__Valid = False;
        if not isinstance(Possession, UserDB.Possession):
            self.__Logger.error("No PossessionObj given");
            self.__Valid = False;
            
        self.__Name = Name;
        self.__Possession = Possession;
        self.__TypeName = TypeName;         #FIXME: Convert to numbers...
        self.__SymbolSlot = SymbolSlot;
        self.__Converter = pyDCPUConverter.Converter(self.__TypeName);
        


    def IsValid(self):
        return(self.__Valid);

    def GetValue(self, SessionID):
        if not self.__Possession.CanRead(SessionID):
            self.__Logger.warning("Session %s: Access denied"%SessionID);
            return(None);
        return(self.__SymbolSlot.GetValue());


    def SetValue(self, Value, SessionID):
        if not self.__Possession.CanWrite(SessionID):
            self.__Logger.warning("Session %s: Access denied"%SessionID);
            return(False);
        return(self.__SymbolSlot.SetValue(Value));

    def GetData(self, Length, SessionID):
        if not self.__Possession.CanRead(SessionID):
            self.__Logger.warning("Session %s: Access denied"%SessionID);
            return(None);
        Value = self.__GetValue(SessionID);
        return(self.__Converter.ConvertToData(Value));

    def SetData(self, Data, SessionID):
        if not self.__Possession.CanWrite(SessionID):
            self.__Logger.warning("Session %s: Access denied"%SessionID);
            return(False);
        return(self.__SetValue(self.__Converter.ConvertToValue(Data),SessionID));
        
    def SetPossession(self, Possession):
        self.__Possession = Possession;
        return(True);

    def GetPossession(self):
        return(self.__Possession);
    
    def ToXML(self, Document):
        """ This method will return a xmlNode contain all info needed
            to rebuild """
        Node = Document.createElement("Symbol");

        Node.setAttribute("name",self.__Name);
        Node.setAttribute("type",self.__TypeName);
        Node.setAttribute("slot",str(self.__SymbolSlot._GetID()));
        Node.setAttribute("own",str(self.__Possession.GetOwner()));
        Node.setAttribute("grp",str(self.__Possession.GetGroup()));
        Node.setAttribute("mod",str(self.__Possession.GetRight()));
        
        return(Node);
#END CLASS "SYMBOL"
