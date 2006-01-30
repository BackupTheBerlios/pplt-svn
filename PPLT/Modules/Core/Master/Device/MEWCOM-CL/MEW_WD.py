import pyDCPU;
import NAISAddress;
import logging;
import MEWConvert;


def WD(Connection, Address, Data):
    Segment = Address.GetSegment();
    if Segment > 99999: raise pyDCPU.ModuleError("Mad segment %i > 9999!"%Segment);

    AreaCode = NAISAddress.AreaCode[Address.GetArea()];

    if Address.GetSize()==NAISAddress.NAIS_WORD: Count = 0;
    elif Address.GetSize() == NAISAddress.NAIS_DWORD: Count = 1;
    else: raise pyDCPU.ModuleError("Bad format of data!");
    
    txtValue = MEWConvert.HexPack(Data, Address.GetSize());
    
    CMD = "WD%s%05i%05i%s"%(AreaCode,Segment,Segment+Count,txtValue);
    
    Connection.write(CMD);

    buff = Connection.read_seq();
    if buff == 'WD': return(1);
    raise pyDCPU.ModuleError("SPS returned ERROR");
