import pyDCPU;
import NAISAddress;
import logging;
import MEWConvert;


def WCC(Connection, Address, Data):
    Logger = logging.getLogger('pyDCPU');

    if not isinstance(Address, NAISAddress.NAIS_Address):
        return(None);

    Segment = Address.GetSegment();
    if Segment > 9999:
        Logger.error("Segment to big");
        return(None);

    AreaCode = NAISAddress.AreaCode.get(Address.GetArea());
    if not AreaCode:
        Logger.error("Unknown AreaCode");
        return(None);

    if Address.GetSize()==NAISAddress.NAIS_WORD:
        Count = 0;
    elif Address.GetSize() == NAISAddress.NAIS_DWORD:
        Count = 1;
    else:
        Logger.error("Bad Format of Data");
        return(None);
    
    txtValue = MEWConvert.Pack(Data, Address.GetSize());            
    if not txtValue:
        Logger.error("Data in wrong format");
        return(None);
    
    CMD = "WCC%s%04i%04i%s"%(AreaCode,Segment,Segment+Count,txtValue);
    
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
