import pyDCPU;
import binascii;
import string;

class Object(pyDCPU.MasterObject):
    def setup(self):
        self.Logger.info("Setup ReadLine")
        tmp = self.Parameters.get('LineEnd');
        self.__LineEnd = binascii.a2b_hex(tmp);
        if len(self.__LineEnd)<1:
            return(False);
        return(True);
    
    def connect(self,AddrStr):
        Connection = pyDCPU.MasterConnection(self, None);
        return(Connection);

    def read(self, Connection, Len):
        lineend = False;
        if Len == 0:
            lineend = True;
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
