import pyDCPU;
import logging;


class Object(pyDCPU.MasterObject):
    def setup(self):
        self.Logger.info("Setup MEWTOCOL Transport Layer");
        if not self.Parameters.has_key('BCC'):
            self.__WithBCC = True;
        elif self.Parameters.get('BCC')=='False':
            self.__WithBCC = False;
        else:
            self.__WithBCC = True;
        return(True);


    def connect(self, AddrStr):
        try:
            Addr = int(AddrStr);
        except:
            self.Logger.error("Invalid Address Format 1-255");
            return(False);

        if Addr<1 or Addr>255:
            self.Logger.error("Invalid address: %i (1-255)"%Addr);
            return(False);
        self.Logger.debug("Got connection-request for address %i"%Addr);
        Con = pyDCPU.MasterConnection(self, "%02X"%Addr);
        return(Con);


    def read(self, Connection, Len):
        return(MEWTocolCOMTLRead(self.Connection, Connection.Address));

    def write(self, Connection, Data):
        return(MEWTocolCOMTLWrite(self.Connection, Connection.Address, Data));

    def flush(self):
        return(self.Connection.flush());












# ############################################################################ #
# UseFullFunctions                                                             #
# ############################################################################ #
def MEWTocolCOMTLWrite(Connection, Address, Data):
    """ This method implements the transportlayer of the MEWTOCOL-COM protocol """
    # FIXME: implement also the longer version of MEWTOCOL-COM messages.
    #FIXME: Implement multible frames

    Logger = logging.getLogger('pyDCPU');
    
    PREFIX  = '%';
    ADDRESS = str(Address);
    if len(ADDRESS)!=2:
        Logger.error("Invalid Address Format for reciver \"%s\""%ADDRESS);
        raise pyDCPU.FatIOModError;
    
    TYPE    = "#";
    MSG     = AssambleMessage(PREFIX, ADDRESS, TYPE, Data, True);

    Logger.debug("Send: \"%s\""%MSG);

    try:
        return(Connection.write(MSG));
    except:
        Logger.error("Error while read a line");    
    return(None);



def MEWTocolCOMTLRead(Connection, Address):
    """ This method read back and check the message """
    #FIXME: Implement multible Frames
    Logger = logging.getLogger('pyDCPU');
    
    #Get a line
    Line = Connection.read(2048);
    
    if not Line:
	Logger.error("Error while read");
	return(None);
    Logger.debug("Got Line \"%s\""%Line);
    	
    #check address
    if not Address == Line[1:3]:
        Logger.warning("Multimaster BUS???");
        return(None);

    #check Type
    if not Line[3] == '$':
        Logger.warning("Got not a response, got \"%s\""%Line[3]);
        return(None);

    #check if multible
    if Line[-1] == '&':
        Logger.error("Multible Frames are not supported (yet)");
        return(None);

    #check BCC if needed:
    BCC = Line[-2:];
    if not BCC == '**':
        if not BCC == CalcBCC(Line[0:-2]):
            Logger.error("BAD BCC");
            return(None);
    #extract/return data:
    return(Line[4:-2]);
    


def AssambleMessage(Prefix, Address, Type, Data, IfBCC):
    BCC = '**';
    if IfBCC:
        BCC = CalcBCC(Prefix+Address+Type+Data);
    return(Prefix+Address+Type+Data+BCC);

def CalcBCC(Data):
    tmp = 0;
    for char in Data:
        tmp ^= ord(char);
    return("%02X"%tmp);

            
