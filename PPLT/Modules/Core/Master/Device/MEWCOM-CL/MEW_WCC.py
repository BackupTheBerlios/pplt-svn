import pyDCPU;
import NAISAddress;
import logging;
import MEWConvert;


def WCC(Connection, Address, Data):
    Segment = Address.GetSegment();
    if Segment > 9999: raise pyDCPU.ModuleError("Mad Segment %s > 9999!"%Segment);

    AreaCode = NAISAddress.AreaCode[Address.GetArea()];

    if Address.GetSize()==NAISAddress.NAIS_WORD: Count = 0;
    elif Address.GetSize() == NAISAddress.NAIS_DWORD: Count = 1;
    else: raise pyDCPU.ModuleError("Bad format of data!");

    txtValue = MEWConvert.HexPack(Data, Address.GetSize());
    
    CMD = "WCC%s%04i%04i%s"%(AreaCode,Segment,Segment+Count,txtValue);
    Connection.write(CMD);

    buff = Connection.read_seq();

    if buff == 'WC': return(1);
    raise pyDCPU.ModuleError("PLC returned ERROR");
