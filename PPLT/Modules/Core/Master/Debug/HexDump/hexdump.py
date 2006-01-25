import binascii;
import string;
import pyDCPU;

class Object(pyDCPU.MasterObject):
    def setup(self): self.Logger.info("Setup HexDump");

    def connect(self, AddrStr):
        if AddrStr: raise pyDCPU.Exception("Need no address!");
        if isinstance(self.Connection, pyDCPU.StreamConnection):
            return pyDCPU.StreamConnection(self, None);
        elif isinstance(self.Connection, pyDCPU.SequenceConnection):
            return pyDCPU.SequenceConnection(self, None);
        raise pyDCPU.ModuleError("Parent have to provide a stream or sequence connection! Got: %s"%type(self.Connection));

    def read(self, Connection, Length=None):
        data = self.Connection.read(Length);
        if data: self.Logger.debug("READ:\n%s"%hexdump(data));
        return(data);

    def write(self, Connection, Data):
        if Data: self.Logger.debug("WRITE:\n%s"%hexdump(Data));
        return(self.Connection.write(Data));

    def flush(self): return(self.Connection.flush());




def hexdump(data):
    dump = ''
    length = len(data);
    lines  = int(length/16);
    n = 0;
    for n in range(0,lines):
        line = data[n*16:(n+1)*16];
        (h,t) = hexline(line);
        dump += "%s%s%s\n"%(h,' '*(40-len(h)), t);

    if not lines: line = data[0:];
    else: line = data[(n+1)*16:];

    (h,t) = hexline(line);
    dump += "%s%s%s"%(h,' '*(40-len(h)), t);

    return(dump);




def hexline(data):
    length = len(data);

    blob = ''
    blub = ''
    
    for n in range(0,length,1):
        if not n == 0:
            if not n%4:
                blob += ' ';

        blob += binascii.b2a_hex(data[n]);
        if ord(data[n])>31 and ord(data[n])<127: blub += data[n];
        else: blub += '.';
    return((blob,blub));


