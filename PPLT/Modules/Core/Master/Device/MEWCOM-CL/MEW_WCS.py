import pyDCPU;
import NAISAddress;
import logging;


def WCS(Connection, Address, Data):
    Segment = Address.GetSegment();
    if Segment > 9999: raise pyDCPU.ModuleError("Mad segment %i > 9999!"%Segment);

    Offset = Address.GetOffset();
    if Offset > 15: pyDCPU.ModuleError("Mad offset %i > 15"%Offset);

    AreaCode = NAISAddress.AreaCode[Address.GetArea()];
    
    CMD = "WCS%s%03i%X%X"%(AreaCode,Segment,Offset,int(Data));
    
    Connection.write(CMD);

    buff = Connection.read_seq();
    if buff == 'WC': return(1);
    raise pyDCPU.ModuleError("SPS returned ERROR");
