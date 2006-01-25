# ############################################################################ #
# This is part of the PPLT project.                                            #
#                                                                              #
# Copyright (C) 2003-2006 Hannes Matuschek <hmatuschek@gmx.net>                #
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
import S7Message;
import pyDCPU;
import struct;

class Object(pyDCPU.MasterObject):
    def setup(self):
        self.Logger.info("Setup Simatic-S7");
        return(True);

    def connect(self,AddrStr):
        RegAddr = S7Register.S7Register(AddrStr);
        self.Logger.debug("MkConnect for %s(%s)"%(AddrStr, str(RegAddr)));
        if not RegAddr:
            raise pyDCPU.ModuleError("Can't split Address \"%s\", my wrong format or not supported address range."%AddrStr);

        #map s7-types to pplt-type-names:
        if RegAddr.GetType() in (S7Register.S7Bit,): Type = pyDCPU.TBool;
        elif RegAddr.GetType() in (S7Register.S7Byte, S7Register.S7Word, S7Register.S7DWord): Type = pyDCPU.TInteger;

        Connection = pyDCPU.ValueConnection(self, Type, RegAddr);
        return(Connection);

    def write(self, Connection, Value):
        if Value == None: raise pyDCPU.ModuleError("No value given to write!");

        Data = Value2Raw(Value, Connection.Address.GetType());          # convert Value to raw byte-data
        DataSet = S7Message.S7DataSet(Data, Connection.Address);        # assamble dataset
        CommSet = S7Message.S7CommandSet(S7Message.S7FunctionWrite, Connection.Address);    # assamble command set
        Message = S7Message.S7Message(CommSet, DataSet);                # assamble message

        self.Logger.debug("Will send a %i byte message."%len(Message.GetString()));
        
        self.Connection.flush()
        # write cmd-message: 
        self.Connection.write(Message.GetString());
        
        # read response:
        MsgString = self.Connection.read_seq();
        
        Message = S7Message.S7Message(MsgString = MsgString);
        CommSet = Message.GetCommandSet();
        DataSet = Message.GetDataSet();
        if DataSet.GetErrCode() == 0xff: return(True);       # 0xff means: all ok.

        self.Logger.error("S7 returned error code: %x"%ord(DataSet.GetErrCode()));
        raise pyDCPU.ModuleError("S7 returned error code: %x"%ord(DataSet.GetErrCode()));


    def read(self, Connection, Len=None):
        self.Logger.debug("Read... Function %s, Addr: %s"%(str(S7Message.S7FunctionRead),str(Connection.Address)));
        CommSet = S7Message.S7CommandSet(S7Message.S7FunctionRead, Connection.Address);
        Message = S7Message.S7Message(CommSet);
        
        self.Connection.flush();
        ret = self.Connection.write(Message.GetString());

        MsgString = self.Connection.read_seq();
        
        Message = S7Message.S7Message(MsgString = MsgString);
        CommSet = Message.GetCommandSet();
        DataSet = Message.GetDataSet();
        
        if DataSet.GetErrCode() == 0xff:
            return Raw2Value(DataSet.GetDataString(), Connection.Address.GetType());

        self.Logger.error("S7 returned error-code: %x"%ord(DataSetGetErrorCode()));
        raise pyDCPU.ModuleError("S7 returned error-code: %x"%ord(DataSetGetErrorCode()));


def Raw2Value(Data, Type):
    if Type == S7Register.S7Bit: (value,) = struct.unpack("B",Data);
    elif Type == S7Register.S7Byte: (value,) = struct.unpack("B",Data);
    elif Type == S7Register.S7Word: (value,) = struct.unpack("H",Data);
    elif Type == S7Register.S7DWord: (value,) = struct.unpack("I",Data);
    return value;

def Value2Raw(Value, Type):
    if Type == S7Register.S7Bit: return struct.pack("B", int(Value));
    elif Type == S7Register.S7Byte: return struct.pack("B", int(Value));
    elif Type == S7Register.S7Word: return struct.pack("H", int(Value));
    elif Type == S7Register.S7DWord: return struct.pack("I", int(Value));

