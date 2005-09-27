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
# 2005-09-23:
#   + Typecode based on XDR (RFC1832)

import struct;
import logging;
import xdrlib;


class Converter:
    def __init__(self, Type):
        self.__TypeName = Type;
        self.__Logger = logging.getLogger('pyDCPU');

        if Type == "Bool":
            self.__Pack = "pack_bool";
            self.__Unpack = "unpack_bool";
            self.__TypeCode = "pack_bool";
        elif Type == "Integer":
            self.__Pack = "pack_int";
            self.__Unpack = "unpack_int";
            self.__TypeCode = "pack_int";
        elif Type == "uInteger":
            self.__Pack = "pack_uint";
            self.__Unpack = "unpack_uint";
            self.__TypeCode = "pack_uint";
        elif Type == "Long":
            self.__Pack = "pack_hyper";
            self.__Unpack = "unpack_hyper";
            self.__TypeCode = "pack_hyper";
        elif Type == "uLong":
            self.__Pack = "pack_uhyper";
            self.__Unpack = "unpack_uhyper";
            self.__TypeCode = "pack_uhyper";
        elif Type == "Float":
            self.__Pack = "pack_float";
            self.__Unpack = "unpack_float";
            self.__TypeCode = "pack_float";
        elif Type == "Double":
            self.__Pack = "pack_double";
            self.__Unpack = "unpack_double";
            self.__TypeCode = "pack_double";
        elif Type == "String":
            self.__Pack = "pack_string";
            self.__Unpack = "unpack_string";
            self.__TypeCode = "pack_string";
        elif Type == "ArrayBool":
            self.__Pack = "pack_array";
            self.__Unpack = "unpack_array";
            self.__TypeCode = "pack_bool";
        elif Type == "ArrayInteger":
            self.__Pack = "pack_array";
            self.__Unpack = "unpack_array";
            self.__TypeCode = "pack_int";
        elif Type == "ArrayuInteger":
            self.__Pack = "pack_array";
            self.__Unpack = "unpack_array";
            self.__TypeCode = "pack_uint";
        elif Type == "ArrayLong":
            self.__Pack = "pack_array";
            self.__Unpack = "unpack_array";
            self.__TypeCode = "pack_hyper";
        elif Type == "ArrayuLong":
            self.__Pack = "pack_array";
            self.__Unpack = "unpack_array";
            self.__TypeCode = "pack_uhyper";
        elif Type == "ArrayFloat":
            self.__Pack = "pack_array";
            self.__Unpack = "unpack_array";
            self.__TypeCode = "pack_float";
        elif Type == "ArrayDouble":
            self.__Pack = "pack_array";
            self.__Unpack = "unpack_array";
            self.__TypeCode = "pack_double";
        elif Type == "ArrayString":
            self.__Pack = "pack_array";
            self.__Unpack = "unpack_array";
            self.__TypeCode = "pack_string";
        else:
            self.__Logger.error("Unknown Datafromt: %s"%Type)
            raise Exception("Unknown data format: %s"%Type);
            

    def GetTypeName(self): return self.__TypeName;

    def ConvertToData(self, Value):
        packer = xdrlib.Packer();
        pack_funct = getattr(packer,self.__Pack);
        if self.__TypeName in ("ArrayBool", "ArrayInteger","ArrayuInteger","ArrayLong","ArrayuLong","ArrayFloat","ArrayDouble","ArrayString"):
            #handle array:
            item_funct = getattr(packer, self.__TypeCode);
            pack_funct(Value, item_funct);
        else:
            pack_funct(Value);
        Data = packer.get_buffer();
        packer.reset();
        return Data;

    def ConvertToValue(self, Data):
        packer = xdrlib.Unpacker(Data);
        unpack_funct = getattr(packer, self.__Unpack);
        value = unpack_funct();
        packer.done();
        return value;
 
















