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
import S7Message;
import pyDCPU;
import struct;
import xdrlib;

class Object(pyDCPU.MasterObject):
    def setup(self):
        self.Logger.info("Setup Simatic-S7");
        return(True);

    def connect(self,AddrStr):
        self.Logger.debug("MkConnect for %s"%(AddrStr));
        RegAddr = S7Register.S7Register(AddrStr);
        if not RegAddr:
            self.Logger.waring("Can't split Address \"%s\""%AddrStr);
            return(None);
        Connection = pyDCPU.MasterConnection(self,RegAddr);
        return(Connection);

    def write(self, Connection, Data):
        Data = XDR2Raw(Data, Connection.Address.GetType());         #convert XDR to raw byte-data
        DataSet = S7Message.S7DataSet(Data, Connection.Address);
        CommSet = S7Message.S7CommandSet(S7Message.S7FunctionWrite, Connection.Address);
        Message = S7Message.S7Message(CommSet, DataSet);

        self.Logger.debug("Will send %i bytes message"%len(Message.GetString()));

        try:
            ret = self.Connection.write(Message.GetString());
        except:
            self.Logger.warning("Error while read");
            raise(pyDCPU.IOModError);
        
        self.Logger.debug("write ret: %i"%ret);

        try:
            MsgString = self.Connection.read(256);
        except:
            self.Logger.warning("Error while read..");
            raise(pyDCPU.IOModError);
        
        Message = S7Message.S7Message(MsgString = MsgString);
        CommSet = Message.GetCommandSet();
        DataSet = Message.GetDataSet();
        if DataSet.GetErrCode() == 0xff:
            return(len(Data));

        self.Logger.error("S7 returned error...");
        raise(pyDCPU.IOModError);

    def read(self, Connection, Data=None):
        CommSet = S7Message.S7CommandSet(S7Message.S7FunctionRead, Connection.Address);
        Message = S7Message.S7Message(CommSet);

        try:
            ret = self.Connection.write(Message.GetString());
        except:
            self.Logger.warning("Error while read...");
            raise(pyDCPU.IOModError);

        try:
            MsgString = self.Connection.read(256);
        except:
            self.Logger.warning("Error while read...");
            raise(pyDCPU.IOModError);
        
        Message = S7Message.S7Message(MsgString = MsgString);
        CommSet = Message.GetCommandSet();
        DataSet = Message.GetDataSet();

        if DataSet.GetErrCode() == 0xff:
            return(Raw2XDR(DataSet.GetDataString(), Connection.Address.GetType()));

        self.Logger.error("S7 returned error");
        raise(pyDCPU.IOModError);


def Raw2XDR(Data, Type):
    packer = xdrlib.Packer();
    if Type == S7Register.S7Bit:
        (value,) = struct.unpack("B",Data);
        packer.pack_bool(value);
    elif Type == S7Register.S7Byte:
        (value,) = struct.unpack("B",Data);
        packer.pack_uint(value);
    elif Type == S7Register.S7Word:
        (value,) = struct.unpack("H",Data);
        packer.pack_uint(value);
    elif Type == S7Register.S7DWord:
        (value,) = struct.unpack("I",Data);
        packer.pack_uint(value);
    return packer.get_buffer();

def XDR2Raw(Data, Type):
    unpacker = xdrlib.Unpacker(Data);
    if Type == S7Register.S7Bit: return struct.pack("B", unpacker.unpack_bool());
    elif Type == S7Register.S7Byte: return struct.pack("B", unpacker.unpack_uint());
    elif Type == S7Register.S7Word: return struct.pack("H", unpacker.unpack_uint());
    elif Type == S7Register.S7DWord: return struct.pack("I", unpacker.unpack_uint());

