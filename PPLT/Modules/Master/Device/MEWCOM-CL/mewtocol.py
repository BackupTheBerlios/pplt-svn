import pyDCPU;
import logging;
import MEW_RCS, MEW_WCS;
import MEW_RCC, MEW_WCC;
import MEW_RD,  MEW_WD;
import Status;
import MEWConvert;
import NAISAddress;


class Object (pyDCPU.MasterObject):
    def setup(self):
        self.Logger.info("Setup MEWTOCOL-COM Command Layer");
        return(True);


    def connect(self, AddrStr):
        self.Logger.debug("Get connection-request for %s"%AddrStr);
        addr = NAISAddress.NAIS_Address(AddrStr);
        if not addr.IsValid():
            self.Logger.error("Addr %s is invalid"%AddrStr);
            return(None);
        con = pyDCPU.MasterConnection(self, addr);
        return(con);


    def read(self, Connection, Len):
        return(NAIS_read(self.Connection, Connection.Address, Len));

    def write(self, Connection, Data):
        return(NAIS_write(self.Connection, Connection.Address, Data));








def NAIS_read(Connection, Address, Len):
    Logger = logging.getLogger('pyDCPU');
    # check parameters:
    if not isinstance(Connection, pyDCPU.MasterConnection):
        Logger.error("ConnectionObject is not a MasterConnection");
        raise pyDCPU.FatIOModError;
    if not isinstance(Address, NAISAddress.NAIS_Address):
        Logger.error("AddressObject is not a NAIS_Address");
        raise pyDCPU.FatIOModError;
    if not Len:
        Logger.debug("Read nothing");
        return(None);
    if not Address.IsValid():
        Logger.error("NAIS Address is not Valid");
        raise pyDCPU.FatIOModError;

    if Address.GetArea() == NAISAddress.NAIS_STATUS:
        ret = Status.GetStatus(Connection, Address);
        if not ret:
            Logger.error("Error while get status");
            raise pyDCPU.IOModError;
        return(ret);
    elif Address.GetArea() in (NAISAddress.NAIS_DATA,NAISAddress.NAIS_FILE,NAISAddress.NAIS_LINKREG):
        ret = MEW_RD.RD(Connection, Address);
        if not ret:
            Logger.error("Error while read");
            raise pyDCPU.IOModError;
        return(ret);
    elif Address.GetSize() == NAISAddress.NAIS_WORD:
        ret = MEW_RCC.RCC(Connection, Address);
        if ret == None:
            Logger.error("Read Error");
            raise pyDCPU.IOModError;
        return(ret);
    elif Address.GetSize() == NAISAddress.NAIS_BOOL:
        ret = MEW_RCS.RCS(Connection, Address);
        if ret == None:
            Logger.error("Read Error");
            raise pyDCPU.IOModError;
        return(ret);

    Logger.error("Fatal: Invalid Address but IsValid() returned true");
    raise pyDCPU.FatIOModError;



def NAIS_write(Connection, Address, Data):
    Logger = logging.getLogger('pyDCPU');
    # check parameters:
    if not isinstance(Connection, pyDCPU.MasterConnection):
        Logger.error("ConnectionObject is not a MasterConnection");
        raise pyDCPU.FatIOModError;
    if not isinstance(Address, NAISAddress.NAIS_Address):
        Logger.error("AddressObject is not a NAIS_Address");
        raise pyDCPU.FatIOModError;
    if not Data:
        Logger.debug("No Data");
        return(None);
    if not Address.IsValid():
        Logger.error("NAIS Address is not Valid");
        raise pyDCPU.FatIOModError;

    if Address.GetArea() == NAISAddress.NAIS_STATUS:
        ret = Status.SetStatus(Connection, Address, Data);
        if not ret:
            Logger.error("Error while set status");
            raise pyDCPU.IOModError;
        return(ret);
    elif Address.GetArea() in (NAISAddress.NAIS_DATA,NAISAddress.NAIS_FILE,NAISAddress.NAIS_LINKREG):
        ret = MEW_WD.WD(Connection, Address, Data);
        if ret == None:
            Logger.error("Error while write (WD)");
            raise pyDCPU.IOModError;
        return(ret);
    elif Address.GetSize() == NAISAddress.NAIS_WORD:
        ret = MEW_WCC.WCC(Connection, Address, Data);
        if ret == None:
            Logger.error("Error while write (WCC)");
            raise pyDCPU.IOModError;
        return(ret);
    elif Address.GetSize() == NAISAddress.NAIS_BOOL:
        ret = MEW_WCS.WCS(Connection, Address, Data);
        if ret == None:
            Logger.error("Error while write(WCS)");
            raise pyDCPU.IOModError;
        return(ret);
    
    Logger.error("Fatal: Invalid Address but IsValid() returned true");
    raise pyDCPU.FatIOModError;
    


