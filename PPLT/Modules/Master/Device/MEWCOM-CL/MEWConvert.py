import struct;
import NAISAddress;

def UnPack(HexStr):
    if len(HexStr)==1:
        return(struct.pack("B",int(HexStr,16)));
    if len(HexStr)==4:
        return(struct.pack("!H",int(HexStr,16)));
    elif len(HexStr) == 8:
        return(struct.pack("!HH",int(HexStr[0:2],16),int(HexStr[2:],16)));
    return(None);1

def Pack(Data, Type):
    if not Data:
        return(None);
    if Type == NAISAddress.NAIS_WORD:
        try:
            (Val) = struct.unpack("!H", Data);
            return("%04X"%Val);
        except:
            return(None);
    elif Type == NAISAddress.NAIS_DWORD:
        try:
            (ValA,ValB) = struct.unpack("!HH",Data);
            return("%04X%04X"%(ValA,ValB));
        except:
            return(None);
    return(None);
    
               
