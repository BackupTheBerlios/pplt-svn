import pyDCPU;
import time;


class Object(pyDCPU.MasterObject):
    def setup(self): self.myLock = 0;

    def connect(self, Address): return pyDCPU.ValueConnection(self, self.Connection.TypeID);

    def read(self, Len=None): return self.Connection.read_seq();
    def write(self, Data): return self.Connection.write(Data);
       
    def lock(self): self.myLock = time.time();
    def unlock(self): pass;
    
    def islocked(self):
        # this module will be allways locked for 5 sec.
        if (time.time() - self.myLock) >= 5: return False;
        return True;
