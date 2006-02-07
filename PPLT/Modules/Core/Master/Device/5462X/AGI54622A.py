import pyDCPU;
import LibAgi;


class Object(pyDCPU.MasterObject):
    def setup(self):
        self.Logger.info("Setup Agilent 5462X Module");
        if not self.Parameters.has_key('PSource'):
            raise pyDCPU.ModuleSetup("No primary source given!");
        if not self.Parameters.has_key('SSource'):
            raise pyDCPU.ModuleSetup("No secondary source.");
        self.__Source = LibAgi.Source(self.Parameters['PSource'],
                                      self.Parameters['SSource']);
        if not self.__Source.IsValid():
            raise pyDCPU.ModuleSetup("Invalid source format.");

    def connect(self, AddrStr):
        if AddrStr == 'freq': addr = LibAgi.AGI_CMD_FREQ;
        elif AddrStr == 'phase': addr = LibAgi.AGI_CMD_PHASE;
        elif AddrStr == 'amp': addr = LibAgi.AGI_CMD_AMP;
        elif AddrStr == 'max': addr = LibAgi.AGI_CMD_MAX;
        elif AddrStr == 'min': addr = LibAgi.AGI_CMD_MIN;
        elif AddrStr == 'pp': addr = LibAgi.AGI_CMD_PP;
        elif AddrStr == 'top': addr = LibAgi.AGI_CMD_TOP;
        elif AddrStr == 'base': addr = LibAgi.AGI_CMD_BASE;
        elif AddrStr == 'width': addr = LibAgi.AGI_CMD_WIDTH;
        else: raise pyDCPU.ModuleError("Invalid address: %s!"%AddrStr);
        return pyDCPU.ValueConnection(self, pyDCPU.TFloat addr);

    def read(self, Connection, len):
        slot = Connection.Address;
        if not slot: raise pyDCPU.ModuleError("Mad connection!");

        if slot == LibAgi.AGI_CMD_FREQ: return LibAgi.GetFreq(self.Connection, self.__Source);
        elif slot == LibAgi.AGI_CMD_PHASE: return LibAgi.GetPhase(self.Connection, self.__Source);
        elif slot == LibAgi.AGI_CMD_AMP: return LibAgi.GetAmp(self.Connection, self.__Source);
        elif slot == LibAgi.AGI_CMD_MAX: return LibAgi.GetMax(self.Connection, self.__Source);
        elif slot == LibAgi.AGI_CMD_MIN: return LibAgi.GetMin(self.Connection, self.__Source);
        elif slot == LibAgi.AGI_CMD_PP: return LibAgi.GetPP(self.Connection, self.__Source);
        elif slot == LibAgi.AGI_CMD_TOP: return LibAgi.GetTop(self.Connection, self.__Source);
        elif slot == LibAgi.AGI_CMD_BASE: return LibAgi.GetBase(self.Connection, self.__Source);
        elif slot == LibAgi.AGI_CMD_WIDTH: return LibAgi.GetWidth(self.Connection, self.__Source);
        raise pyDCPU.ModuleError("Invalid address id: %s"%str(slot));
        
    def write(self, Connection, Data): raise pyDCPU.AccessDenied("This module is read only");
