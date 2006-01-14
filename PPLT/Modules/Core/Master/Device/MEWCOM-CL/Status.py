import pyDCPU;
import logging;
import MEWConvert;
import NAISAddress;


def GetStatus(Connection, Address):
    Logger = logging.getLogger('pyDCPU');

    if not isinstance(Address, NAISAddress.NAIS_Address):
        return(None);

    CMD = "RCSR9020";       # address of status bit

    try:
        Connection.write(CMD);
    except:
        Logger.error("Error while send command");
        raise pyDCPU.IOModError;

    try:
        buff = Connection.read(100);
    except Exception, e:
        Logger.error("Error while read: %s",str(e));
        raise pyDCPU.IOModError;
    Value = MEWConvert.HexUnpack(buff[2]);
    return MEWConvert.BoolPack(Value);
    #return(MEWConvert.UnPack(buff[2]));




def SetStatus(Connection, Address, Data):
    Logger = logging.getLogger('pyDCPU');

    if not isinstance(Address, NAISAddress.NAIS_Address):
        return(None);

    if MEWConvert.BoolUnpack(Data):
        Value = 'R';
    else:
        Value = 'P';

    
    CMD = "RM%s"%Value;

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

    if buff == 'RM':
        return(1);

    Logger.error("SPS returned ERROR");
    return(None);
