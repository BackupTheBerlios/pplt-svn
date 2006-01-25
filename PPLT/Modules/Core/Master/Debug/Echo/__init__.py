import pyDCPU;

class Object (pyDCPU.MasterObject):
    def setup(self):
        self.Logger.debug("Setup Echo module");
        self.Buffer = None;

    def connect(self, AddrStr):
        if AddrStr: raise pyDCPU.ModuleError("I don't need an address!");
        return pyDCPU.StreamConnection(self, None);
    
    def read(self, Connection, Length=None):
        if not self.Buffer: return '';
        if not Length:
            tmp = self.Buffer;
            self.Buffer = None;
            return tmp;
        if Length > len(self.Buffer):
            tmp = self.Buffer;
            self.Buffer = None;
            return tmp;
        tmp = self.Buffer[:Length];
        self.Buffer = self.Buffer[Length:];
        return tmp;

    def write(self, Connection, Data):
        if self.Buffer: self.Buffer += Data;
        else: self.Buffer = Data;
        return len(Data);

    def flush(self): self.Buffer = None;
