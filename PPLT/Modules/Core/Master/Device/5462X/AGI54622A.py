import pyDCPU;
import LibAgi;


class Object(pyDCPU.MasterObject):
    def setup(self):
        self.Logger.info("Setup Agilent 5462X Module");
        if not self.Parameters.has_key('PSource'):
            self.Logger.error("Need primary source");
            return(False);
        if not self.Parameters.has_key('SSource'):
            self.Logger.error("Need secondary source");
            return(False);
        self.__Source = LibAgi.Source(self.Parameters['PSource'],
                                      self.Parameters['SSource']);
        if not self.__Source.IsValid():
            self.Logger.error("Invalid source format");
            return(False);
        return(True);

    def connect(self, AddrStr):
        if AddrStr == 'freq':
            addr = LibAgi.AGI_CMD_FREQ;
        elif AddrStr == 'phase':
            addr = LibAgi.AGI_CMD_PHASE;
        elif AddrStr == 'amp':
            addr = LibAgi.AGI_CMD_AMP;
        elif AddrStr == 'max':
            addr = LibAgi.AGI_CMD_MAX;
        elif AddrStr == 'min':
            addr = LibAgi.AGI_CMD_MIN;
        elif AddrStr == 'pp':
            addr = LibAgi.AGI_CMD_PP;
        elif AddrStr == 'top':
            addr = LibAgi.AGI_CMD_TOP;
        elif AddrStr == 'base':
            addr = LibAgi.AGI_CMD_BASE;
        elif AddrStr == 'width':
            addr = LibAgi.AGI_CMD_WIDTH;
        else:
            self.Logger.error("Invalid Slot %s"%AddrStr);
            return(None);
        return( pyDCPU.MasterConnection(self, addr) );

    def read(self, Connection, len):
        slot = Connection.Address;
        if not slot:
            self.Logger.error("No connection!!!");
            raise pyDCPU.FatIOModError;

        if slot == LibAgi.AGI_CMD_FREQ:
            return( LibAgi.PackDouble(LibAgi.GetFreq(self.Connection,
                                                     self.__Source)) );
        elif slot == LibAgi.AGI_CMD_PHASE:
            return( LibAgi.PackDouble(LibAgi.GetPhase(self.Connection,
                                                      self.__Source)) );
        elif slot == LibAgi.AGI_CMD_AMP:
            return( LibAgi.PackDouble(LibAgi.GetAmp(self.Connection,
                                                    self.__Source)) );
        elif slot == LibAgi.AGI_CMD_MAX:
            return( LibAgi.PackDouble(LibAgi.GetMax(self.Connection,
                                                    self.__Source)) );
        elif slot == LibAgi.AGI_CMD_MIN:
            return( LibAgi.PackDouble(LibAgi.GetMin(self.Connection,
                                                    self.__Source)) );
        elif slot == LibAgi.AGI_CMD_PP:
            return( LibAgi.PackDouble(LibAgi.GetPP(self.Connection,
                                                   self.__Source)) );
        elif slot == LibAgi.AGI_CMD_TOP:
            return( LibAgi.PackDouble(LibAgi.GetTop(self.Connection,
                                                    self.__Source)) );
        elif slot == LibAgi.AGI_CMD_BASE:
            return( LibAgi.PackDouble(LibAgi.GetBase(self.Connection,
                                                     self.__Source)) );
        elif slot == LibAgi.AGI_CMD_WIDTH:
            return( LibAgi.PackDouble(LibAgi.GetWidth(self.Connection,
                                                      self.__Source)) );
        
        self.Logger.error("Invalid Address ID %s"%str(slot));
        raise pyDCPU.FatIOModError;
        
    def write(self, Connection, Data):
        self.Logger.error("This module is read only");
        raise pyDCPU.IOModError;
    
