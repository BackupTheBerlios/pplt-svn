# ############################################################################ #
# This is part of the PPLT project.                                            #
#                                                                              #
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


import S7Register;
import struct;

S7MessageRW     = 0x01;
S7MessageResult = 0x03;

S7FunctionRead  = 0x04;
S7FunctionWrite = 0x05;

class S7DataSet:
    def __init__(self, Data = None, RegAddr = None, DataString = None):
        self.__DataErrCode = 0;
        if Data and RegAddr:
            self.__DataErrCode  = 0;
            self.__DataUKB      = 0x04;
            self.__DataLength   = RegAddr.GetSize();      #Length in Bit
            self.__DataString   = Data;

            FMT = "!BBH%is"%len(Data);
            self.__String = struct.pack(FMT, self.__DataErrCode,
                                    self.__DataUKB,
                                    self.__DataLength,
                                    self.__DataString);
        elif DataString:
            if len(DataString) == 1:
                self.__DataErrCode = ord(DataString[0]);
            elif len(DataString) > 4:
                FMT = "!BBH";
                (self.__DataErrCode,
                 self.__DataUKB,
                 self.__DataLength) = struct.unpack(FMT, DataString[:4]);
                self.__DataString = DataString[4:]

    def GetString(self):
        return(self.__String);
    def GetDataString(self):
        return(self.__DataString);
    def GetErrCode(self):
        return(self.__DataErrCode);




class S7CommandSet:
    def __init__(self, Function = None, RegAddr = None, CommString = None):
        if Function and RegAddr:
            self.__CommFunction = Function;
            self.__CommNumber   = 1;

            self.__CommUKB1     = 0x12;
            self.__CommUKB2     = 0x0A;
            self.__CommUKB3     = 0x10;
            self.__CommDType    = RegAddr.GetType();
            self.__CommCount    = 1;
            self.__CommDBNum    = 0;
            self.__CommArea     = RegAddr.GetArea();

            Offset = RegAddr.GetMajor()*RegAddr.GetSize()+RegAddr.GetMinor();
            self.__CommOffSetLB = Offset & 0xff;
            self.__CommOffSetMB = (Offset>>8) & 0xff;
            self.__CommOffSetHB = (Offset>>16) & 0xff;
        elif CommString:
            self.__CommFunction = CommString[0];
            self.__CommCount    = CommString[1];
        
    def GetString(self):
        # Network byte order... ('!')
        FMT = "!BBBBBBHHBBBB";
        self.__CommString =  struct.pack(FMT, self.__CommFunction,
                                         self.__CommNumber,
                                         self.__CommUKB1,
                                         self.__CommUKB2,
                                         self.__CommUKB3,
                                         self.__CommDType,
                                         self.__CommCount,
                                         self.__CommDBNum,
                                         self.__CommArea,
                                         self.__CommOffSetHB,
                                         self.__CommOffSetMB,
                                         self.__CommOffSetLB);
        return(self.__CommString);



class S7Message:
    def __init__(self, CommandSet = None, DataSet = None, MsgString=None):
        if CommandSet:
            self.__CommandSet   = CommandSet;
            self.__DataSet      = DataSet;
            self.__MsgString    = MsgString;
            
            self.__MsgSync      = 0x32;
            self.__MsgType      = S7MessageRW;
            self.__MsgUKB1      = 0x00; #UKB == UnKnowByte (FIXME: find out sense)
            self.__MsgUKB2      = 0x00;
            self.__MsgNo        = 0x00;
            self.__MsgCommLen   = 0x00;
            self.__MsgDataLen   = 0x00;
        
            self.__MsgUKB3      = 0x00; #Only for result messg.
            self.__MsgUKB4      = 0x00; #Only for result messg.
        
            self.__MsgCommStr   = CommandSet.GetString();
            self.__MsgCommLen   = len(self.__MsgCommStr);

            if DataSet:
                self.__MsgDataStr   = DataSet.GetString();
                self.__MsgDataLen   = len(self.__MsgDataStr);

                FMT = "!BBBBHHH%is%is"%(self.__MsgCommLen,self.__MsgDataLen);
                self.__MsgString = struct.pack(FMT, self.__MsgSync,
                                           self.__MsgType,
                                           self.__MsgUKB1,
                                           self.__MsgUKB2,
                                           self.__MsgNo,
                                           self.__MsgCommLen,
                                           self.__MsgDataLen,
                                           self.__MsgCommStr,
                                           self.__MsgDataStr);
            else:
                FMT = "!BBBBHHH%is"%(self.__MsgCommLen);
                self.__MsgDataLen   = 0;
                self.__MsgString = struct.pack(FMT, self.__MsgSync,
                                           self.__MsgType,
                                           self.__MsgUKB1,
                                           self.__MsgUKB2,
                                           self.__MsgNo,
                                           self.__MsgCommLen,
                                           self.__MsgDataLen,
                                           self.__MsgCommStr);
        if MsgString:
            MessageHeader = MsgString[:12];
            MsgString = MsgString[12:]
            FMT = "!BBBBHHHBB";
            (self.__MsgSync,
             self.__MsgType,
             self.__MsgUKB1,
             self.__MsgUKB2,
             self.__MsgNo,
             self.__MsgCommLen,
             self.__MsgDataLen,
             self.__MsgUKB3,
             self.__MsgUKB4) = struct.unpack(FMT, MessageHeader);
            self.__MsgCommStr = MsgString[:self.__MsgCommLen];
            MsgString = MsgString[self.__MsgCommLen:]
            self.__MsgDataStr = MsgString[:self.__MsgDataLen];

            self.__CommandSet= S7CommandSet(CommString = self.__MsgCommStr);
            self.__DataSet = S7DataSet(DataString = self.__MsgDataStr);
            

    def GetString(self):
        return(self.__MsgString);

    def GetCommandSet(self):
        return(self.__CommandSet);
    def GetDataSet(self):
        return(self.__DataSet);

