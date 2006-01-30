import pyDCPU;
import MEWConvert;
import NAISAddress;
import logging;

def RD(Connection, Address):
    Segment = Address.GetSegment();
    if Segment > 9999: raise pyDCPU.ModuleError("Segmen %i to big (>9999)!"%Segment);

    AreaCode = NAISAddress.AreaCode[Address.GetArea()];

    if Address.GetSize()==NAISAddress.NAIS_WORD: Count = 0;  # start and stop address are the same
    elif Address.GetSize() == NAISAddress.NAIS_DWORD: Count = 1;
    else: raise pyDCPU.ModuleError("Mad word count (size) %i!"%Address.GetSize());
    
    CMD = "RD%s%05i%05i"%(AreaCode,Segment,Segment+Count);
    
    Connection.write(CMD);
        
    buff = Connection.read_seq();
    return MEWConvert.HexUnpack(buff[2:]);
