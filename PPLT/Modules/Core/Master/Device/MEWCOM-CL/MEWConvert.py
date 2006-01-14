import NAISAddress;
import xdrlib;


def HexUnpack(Buff):
    if len(HexStr)==1:
        return int(HexStr,16);
    if len(HexStr)==4:
        return int(HexStr,16);
    elif len(HexStr) == 8:
        return int(HexStr,16)  # decode and switch ByteOrder!
    return(None);


def HexPack(Val, Type):
    if not Data: return(None);
    if Type == NAISAddress.NAIS_WORD:
        try: return("%04X"%Val);
        except: return(None);
    elif Type == NAISAddress.NAIS_DWORD:
        try: return("%08X"%Val);
        except: return(None);
    return(None);




def BoolPack(Value):
    packer = xdrlib.Packer();
    packer.pack_bool(Value);
    return packer.get_buffer();

def BoolUnpack(Data):
    packer = xdrlib.Unpacker(Data);
    val = packer.unpack_bool();
    packer.done();
    return val;

def UIntPack(Value):
    packer = xdrlib.Packer();
    packer.pack_uint(Value);
    return packer.get_buffer();

def UIntUnpack(Data):
    packer = xdrlib.Unpacker(Data);
    val = packer.unpack_uint();
    packer.done();
    return val;

