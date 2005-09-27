import pyDCPU;
import NAISAddress;
import logging;


def WCS(Connection, Address, Data):
    Logger = logging.getLogger('pyDCPU');

    if not isinstance(Address, NAISAddress.NAIS_Address):
        return(None);

    Segment = Address.GetSegment();
    if Segment > 9999:
        return(None);

    Offset = Address.GetOffset();
    if Offset > 15:
        return(None);

    AreaCode = NAISAddress.AreaCode.get(Address.GetArea());
    if not AreaCode:
        return(None);

    if MEWBoolUnpack(Data):
        Value = 1;
    else:
        Value = 0;
        
    
    CMD = "WCS%s%03i%X%X"%(AreaCode,Segment,Offset,Value);
    
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

    if buff == 'WC':
        return(1);

    Logger.error("SPS returned ERROR");
    return(None);
