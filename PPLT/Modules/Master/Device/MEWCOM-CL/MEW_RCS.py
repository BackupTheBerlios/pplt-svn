import pyDCPU;
import logging;
import NAISAddress;
import MEWConvert;


def RCS(Connection, Address):
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

    CMD = "RCS%s%03i%X"%(AreaCode,Segment,Offset,);
    
    try:
        Connection.write(CMD);
    except:
        Logger.error("Error while send command");
        raise pyDCPU.IOModError;

    try:
        buff = Connection.read(100);
    except:
        Logger.error("Error while read: maybe a bad Marker-Address???");
        raise pyDCPU.IOModError;
    return(MEWConvert.UnPack(buff[2]));
