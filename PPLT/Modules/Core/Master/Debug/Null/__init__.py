import pyDCPU;

class Object(pyDCPU.MasterObject):
    def setup(self): self.Logger.info("Setup NULL module...");

    def connect(self, AddrStr):
        if AddrStr: raise pyDCPU.ModuleError("I don't need an address: %s"%AddrStr);
        return pyDCPU.StreamConnection(self, None);
        
    def read(self, Connection, Length=1):
        return "\000"*Length;
    
    def write(self, Connection, Buffer): return len(Buffer);

    def flush(self): pass;
