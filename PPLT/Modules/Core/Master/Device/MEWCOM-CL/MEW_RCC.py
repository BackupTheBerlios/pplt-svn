import pyDCPU;
import NAISAddress;
import MEWConvert;
import logging;

def RCC(Connection, Address):
    Logger = logging.getLogger('pyDCPU');

    Segment = Address.GetSegment();
    if Segment > 9999: raise pyDCPU.ModuleError("Sequence %i to big (>9999)!"%Segment);

    AreaCode = NAISAddress.AreaCode.get(Address.GetArea());

    CMD = "RCC%s%04i%04i"%(AreaCode, Segment, Segment);
    
    Connection.write(CMD);
    buff = Connection.read_seq();
    
    return MEWConvert.HexUnpack(buff[2:]);
