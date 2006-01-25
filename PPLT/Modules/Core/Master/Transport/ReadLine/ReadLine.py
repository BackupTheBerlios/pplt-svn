import pyDCPU;
import binascii;
import string;

class Object(pyDCPU.MasterObject):
    def setup(self):
        self.Logger.info("Setup ReadLine");
        if not self.Parameters.has_key("LineEnd"): raise pyDCPU.ModuleSetup("Need lineend!");
        tmp = self.Parameters.get('LineEnd');
        self.__LineEnd = binascii.a2b_hex(tmp);
    
    def connect(self,AddrStr): return pyDCPU.SequenceConnection(self, None);

    def read(self, Connection, Len=None):
        lineend = False;
        if Len == 0: lineend = True;
        buff = '';
        
        while not lineend:
            buff = buff + self.Connection.read(1);
            pos = string.find(buff,self.__LineEnd);
            if pos != -1:
                line = string.strip(buff,self.__LineEnd);
                lineend = True;
        return(line);
        

    def write(self, Connection, Data):
        tmp = Data + self.__LineEnd;
        return(self.Connection.write(tmp));

    def flush(self):
        return(self.Connection.flush());
