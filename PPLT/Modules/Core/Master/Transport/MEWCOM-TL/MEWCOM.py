import pyDCPU;
import logging;


class Object(pyDCPU.MasterObject):
    def setup(self):
        self.Logger.info("Setup MEWTOCOL Transport Layer");
        if not self.Parameters.has_key('BCC'): self.__WithBCC = True;
        elif self.Parameters.get('BCC')=='False': self.__WithBCC = False;
        else: self.__WithBCC = True;


    def connect(self, AddrStr):
        try: Addr = int(AddrStr);
        except Exception,e: raise pyDCPU.ModuleError("Invalid address: %s (Excp: %s)"%(AddrStr, str(e));

        if Addr<1 or Addr>255: raise pyDCPU.ModuleError("Invalid address: %s. Should be 1-255!"%AddrStr);
        self.Logger.debug("Got connection-request for address %i"%Addr);
        Con = pyDCPU.MasterConnection(self, "%02X"%Addr);
        return(Con);


    def read(self, Connection, Len): return(MEWTocolCOMTLRead(self.Connection, Connection.Address));

    def write(self, Connection, Data): return(MEWTocolCOMTLWrite(self.Connection, Connection.Address, Data));

    def flush(self): return(self.Connection.flush());












# ############################################################################ #
# UseFullFunctions                                                             #
# ############################################################################ #
def MEWTocolCOMTLWrite(Connection, Address, Data):
    """ This method implements the transportlayer of the MEWTOCOL-COM protocol """
    #FIXME: Implement multible frames

    Logger = logging.getLogger('pyDCPU');
    
    PREFIX  = '%';
    ADDRESS = str(Address);
    if len(ADDRESS)!=2: raise pyDCPU.ModuleError("Invalid address-formant for reciver \"%s\"."%ADDRESS);
    
    TYPE    = "#";
    MSG     = AssambleMessage(PREFIX, ADDRESS, TYPE, Data, True);

    Logger.debug("Send: \"%s\""%MSG);
    return(Connection.write(MSG));



def MEWTocolCOMTLRead(Connection, Address):
    """ This method read back and check the message """
    #FIXME: Implement multible Frames
    Logger = logging.getLogger('pyDCPU');
    
    #Get a line
    Line = Connection.read_seq();
    
    if len(Line)==0: raise pyDCPU.ModuleError("Unable to read from parent!");
    Logger.debug("Got Line \"%s\""%Line);
    
    #check address
    if not Address == Line[1:3]: raise pyDCPU.ModuleError("Multimaster BUS???");

    #check Type
    if not Line[3] == '$': raise pyDCPU.ModuleError("Got not a response, got \"%s\""%Line[3]);

    #check if multible
    if Line[-1] == '&': raise pyDCPU.ModuleError("Multible Frames are not supported (yet)");

    #check BCC if needed:
    BCC = Line[-2:];
    if not BCC == '**':
        if not BCC == CalcBCC(Line[0:-2]): raise pyDCPU.ModuleError("Transport error: Bad BCC!");
    #extract/return data:
    return(Line[4:-2]);
    


def AssambleMessage(Prefix, Address, Type, Data, IfBCC):
    BCC = '**';
    if IfBCC: BCC = CalcBCC(Prefix+Address+Type+Data);
    return(Prefix+Address+Type+Data+BCC);

def CalcBCC(Data):
    tmp = 0;
    for char in Data:
        tmp ^= ord(char);
    return("%02X"%tmp);
