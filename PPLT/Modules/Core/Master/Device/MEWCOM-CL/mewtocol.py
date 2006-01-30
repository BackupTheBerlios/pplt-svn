import pyDCPU;
import logging;
import MEW_RCS, MEW_WCS;
import MEW_RCC, MEW_WCC;
import MEW_RD,  MEW_WD;
import Status;
import MEWConvert;
import NAISAddress;


class Object (pyDCPU.MasterObject):
    def setup(self): self.Logger.info("Setup MEWTOCOL-COM Command Layer");


    def connect(self, AddrStr):
        self.Logger.debug("Get connection-request for %s"%AddrStr);
        addr = NAISAddress.NAIS_Address(AddrStr);
        if not addr.IsValid(): raise pyDCPU.ModuleError("Address \"%s\" is invalid!"%(AddrStr));
        
        if addr.GetType() == NAISAddress.NAIS_BOOL: Type = pyDCPU.TBool;
        elif addr.GetType() in (NAISAdress.NAIS_WORD, NAISAddress.NAIS_DWORD): Type = pyDCPU.TInteger;
        else: raise pyDCPU.ModuleError("Invalid type-code: %i."%addr.GetType());
        
        return pyDCPU.ValueConnection(self,Type,  addr);


    def read(self, Connection, Len): return(NAIS_read(self.Connection, Connection.Address, Len));

    def write(self, Connection, Data): return(NAIS_write(self.Connection, Connection.Address, Data));






#
# Functions:
#
def NAIS_read(Connection, Address, Len=None):
    # check parameters:
    if not isinstance(Connection, pyDCPU.ValueConnection):
        raise pyDCPU.ModuleError("Connection is not a ValueConnection");
    if not isinstance(Address, NAISAddress.NAIS_Address):
        raise pyDCPU.ModuleError("Embed addre-obj of wrong type!");
    if not Address.IsValid(): raise pyDCPU.ModuleError("Invalid Address!");
    # read:
    if Address.GetArea() == NAISAddress.NAIS_STATUS: return Status.GetStatus(Connection, Address);
    elif Address.GetArea() in (NAISAddress.NAIS_DATA,NAISAddress.NAIS_FILE,NAISAddress.NAIS_LINKREG):
        return MEW_RD.RD(Connection, Address);
    elif Address.GetSize() == NAISAddress.NAIS_WORD: return MEW_RCC.RCC(Connection, Address);
    elif Address.GetSize() == NAISAddress.NAIS_BOOL: return MEW_RCS.RCS(Connection, Address);
    raise pyDCPU.ModuleError("Valid address but no known method to handle the addr.");



def NAIS_write(Connection, Address, Data):
    # check parameters:
    if not isinstance(Connection, pyDCPU.ValueConnection):
        raise pyDCPU.ModuleError("Invalid Connection!");
    if not isinstance(Address, NAISAddress.NAIS_Address):
        raise pyDCPU.ModuleError("Address-object not a vlid address!");
    if not Data: return(1);
    if not Address.IsValid(): raise pyDCPU.ModuleError("Invalid address!");

    if Address.GetArea() == NAISAddress.NAIS_STATUS:
        return Status.SetStatus(Connection, Address, Data);
    elif Address.GetArea() in (NAISAddress.NAIS_DATA,NAISAddress.NAIS_FILE,NAISAddress.NAIS_LINKREG):
        return MEW_WD.WD(Connection, Address, Data);
    elif Address.GetSize() == NAISAddress.NAIS_WORD:
        return MEW_WCC.WCC(Connection, Address, Data);
    elif Address.GetSize() == NAISAddress.NAIS_BOOL:
        return MEW_WCS.WCS(Connection, Address, Data);
    raise pyDCPU.ModuleError("Fatal: Invalid Address but IsValid() returned true");
