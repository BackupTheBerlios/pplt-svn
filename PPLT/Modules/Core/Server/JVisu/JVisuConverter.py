import pyDCPU;
from JVisuTypes import *;
import struct
def ToData(Value, Type):
    if Value == None: return None;
    if Type == JVISU_TYP_BOOL:
        if Value:  return struct.pack("B",1);
        return struct.pack("B",0);
    elif Type == JVISU_TYP_BYTE: return struct.pack("B",Value);
    elif Type == JVISU_TYP_WORD: return struct.pack("H", Value);
    elif Type == JVISU_TYP_DWORD: return struct.pack("I", Value);
    elif Type == JVISU_TYP_FLOAT: return struct.pack("f", Value);
    elif Type == JVISU_TYP_DOUBLE: return struct.pack("d", Value);
    elif Type == JVISU_TYP_STRING: return Value;
    else: return None;


def ToValue(Data, Type):
    if Type == JVISU_TYP_BOOL: 
        (tmp, ) = struct.unpack("B", Data);
        if tmp: return True;
        return False;
    elif Type == JVISU_TYP_BYTE:
        (tmp, ) = struct.unpack("B", Data);
        return tmp;
    elif Type == JVISU_TYP_WORD:
        (tmp, ) = struct.unpack("H", Data);
        return tmp;
    elif Type == JVISU_TYP_DWORD:
        (tmp, ) = struct.unpack("I", Data);
        return tmp;
    elif Type == JVISU_TYP_FLOAT:
        (tmp, ) = struct.unpack("f", Data);
        return tmp;
    elif Type == JVISU_TYP_DOUBLE:
        (tmp, ) = struct.unpack("d", Data);
        return tmp;
    elif Type == JVISU_TYP_STRING: return Data;
    else: return None;
