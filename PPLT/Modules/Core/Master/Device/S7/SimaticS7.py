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
        Connection = pyDCPU.ValueConnection(self,RegAddr);
        return(Connection);

    def write(self, Connection, Value):
        if Value == None:
            self.Logger.error("No value given!");
            return None;

        Data = Value2Raw(Value, Connection.Address.GetType());          # convert Value to raw byte-data
        DataSet = S7Message.S7DataSet(Data, Connection.Address);        # assamble dataset
        CommSet = S7Message.S7CommandSet(S7Message.S7FunctionWrite, Connection.Address);    # assamble command set
        Message = S7Message.S7Message(CommSet, DataSet);                # assamble message

        self.Logger.debug("Will send %i bytes message"%len(Message.GetString()));
        
        self.Connection.flush()
        # write cmd-message: 
        try: ret = self.Connection.write(Message.GetString());
        except:
            self.Logger.warning("Error while read");
            raise(pyDCPU.IOModError);
        
        self.Logger.debug("write ret: %i"%ret);

        # read response:
        try: MsgString = self.Connection.read_seq();
        except:
            self.Logger.warning("Error while read..");
            raise(pyDCPU.IOModError);
        
        Message = S7Message.S7Message(MsgString = MsgString);
        CommSet = Message.GetCommandSet();
        DataSet = Message.GetDataSet();
        if DataSet.GetErrCode() == 0xff:        # 0xff means: all ok.
            return(True);

        self.Logger.error("S7 returned error...");
        raise(pyDCPU.IOModError);


    def read(self, Connection, Len=None):
        CommSet = S7Message.S7CommandSet(S7Message.S7FunctionRead, Connection.Address);
        Message = S7Message.S7Message(CommSet);
        
        self.Connection.flush();
        try: ret = self.Connection.write(Message.GetString());
        except:
            self.Logger.warning("Error while read...");
            raise(pyDCPU.IOModError);

        try: MsgString = self.Connection.read_seq();
        except:
            self.Logger.warning("Error while read...");
            raise(pyDCPU.IOModError);
        
        Message = S7Message.S7Message(MsgString = MsgString);
        CommSet = Message.GetCommandSet();
        DataSet = Message.GetDataSet();
        
        if DataSet.GetErrCode() == 0xff:
            try: ret = Raw2Value(DataSet.GetDataString(), Connection.Address.GetType());
            except Exception, e:
                self.Logger.error("Error while convert data->Value! (invalid format? wrong type?): %s"%e);
                return None;
            return ret;

        self.Logger.error("S7 returned error-code: %x"%ord(DataSetGetErrorCode()));
        raise(pyDCPU.IOModError);



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

