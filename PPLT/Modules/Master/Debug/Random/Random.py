import pyDCPU;
import struct;
import xdrlib;
import random;

RAND_BOOL   = 1;
RAND_INTEGER  = 4;
RAND_FLOAT  = 5;
RAND_DOUBLE = 6;



class Object(pyDCPU.MasterObject):
    def setup(self):
        self.Logger.info("Setup Random Module");
        return(True);

    def connect(self, AddrStr):
        if AddrStr == 'Bool':
            ADDR = RAND_BOOL;
        elif AddrStr == 'Integer':
            ADDR = RAND_INTEGER;
        elif AddrStr == 'Float':
            ADDR = RAND_FLOAT;
        elif AddrStr == 'Double':
            ADDR = RAND_DOUBLE;
        else:
            self.Logger.error("Unknown type %s"%AddrStr);
            return(None);
        return( pyDCPU.MasterConnection(self, ADDR) );

    def read(self, Con, len=None):
        if Con.Address == RAND_BOOL:
            return(GetRandBool());
        elif Con.Address == RAND_INTEGER:
            return(GetRandInt());
        elif Con.Address == RAND_FLOAT:
            return(GetRandFloat());
        elif Con.Address == RAND_DOUBLE:
            return(GetRandDouble());
        else:
            self.Logger.error("Invalid Address!!!");
            raise pyDCPU.FatIOModError;

    def write(self, Con, Data):
        self.Logger.error("This is a read only module!!!");
        raise pyDCPU.IOModError;



def GetRandBool():
    packer = xdrlib.Packer();
    packer.pack_bool(random.choice( (1,0) ));
    return packer.get_buffer();

def GetRandInt():
    packer = xdrlib.Packer();
    packer.pack_int(random.randint(0,100));
    return packer.get_buffer();

def GetRandFloat():
    packer = xdrlib.Packer();
    packer.pack_float(random.random());
    return packer.get_buffer();
    
def GetRandDouble():
    packer = xdrlib.Packer();
    packer.pack_double(random.random());
    return packer.get_buffer();
