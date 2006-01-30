import pyDCPU;
import logging;
import NAISAddress;
import MEWConvert;


def RCS(Connection, Address):
    Segment = Address.GetSegment();
    if Segment > 9999: raise pyDCPU.ModuleError("Segment %i to big (>9999)!"%Segment);

    Offset = Address.GetOffset();
    if Offset > 15: raise pyDCPU.ModuleError("Offset %i to big (>15)!"%Offset);

    AreaCode = NAISAddress.AreaCode[Address.GetArea()];

    CMD = "RCS%s%03i%X"%(AreaCode,Segment,Offset,);
    
    Connection.write(CMD);

    buff = Connection.read_seq();
        
    return MEWConvert.HexUnpack(buff[2]);
