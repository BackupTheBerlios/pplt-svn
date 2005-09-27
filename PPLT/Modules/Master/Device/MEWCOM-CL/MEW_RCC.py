import pyDCPU;
import NAISAddress;
import MEWConvert;
import logging;

def RCC(Connection, Address):
    Logger = logging.getLogger('pyDCPU');

    if not isinstance(Address, NAISAddress.NAIS_Address):
        return(None);

    Segment = Address.GetSegment();
    if Segment > 9999:
        return(None);

    AreaCode = NAISAddress.AreaCode.get(Address.GetArea());
    if not AreaCode:
        return(None);

    CMD = "RCC%s%04i%04i"%(AreaCode, Segment, Segment);
    
    try:
        Connection.write(CMD);
    except:
        Logger.error("Error while send command");
        raise pyDCPU.ModIOError;

    try:
        buff = Connection.read(100);
    except:
        Logger.error("Error while read: maybe a bad Marker-Address???");
        raise pyDCPU.ModIOError;
    Value = MEWConvert.HexUnpack(buff[2:]);
    return(MEWConvert.UIntPack(Value));
