import pyDCPU;
import MEWConvert;
import NAISAddress;
import logging;

def RD(Connection, Address):
    Logger = logging.getLogger('pyDCPU');

    if not isinstance(Address, NAISAddress.NAIS_Address):
        return(None);

    Segment = Address.GetSegment();
    if Segment > 9999:
        return(None);

    AreaCode = NAISAddress.AreaCode.get(Address.GetArea());
    if not AreaCode:
        return(None);

    if Address.GetSize()==NAISAddress.NAIS_WORD:
        Count = 0;  # start and stop address are the same
    elif Address.GetSize() == NAISAddress.NAIS_DWORD:
        Count = 1;
    else:
        return(None);
    
    CMD = "RD%s%05i%05i"%(AreaCode,Segment,Segment+Count);
    
    try:
        Connection.write(CMD);
    except:
        Logger.error("Error while send command");
        raise pyDCPU.ModIOError;

    try:
        buff = Connection.read(100);
    except:
        Logger.error("Error while read: maybe a bad Marker-Address???");
        raise pyDCPU.ModIOErrZr;

    return(MEWConvert.UnPack(buff[2:]));
