import pyDCPU;
import struct;
import random;

RAND_BOOL   = 1;
RAND_BYTE   = 2;
RAND_WORD   = 3;
RAND_DWORD  = 4;
RAND_FLOAT  = 5;
RAND_DOUBLE = 6;



class Object(pyDCPU.MasterObject):
    def setup(self):
        self.Logger.info("Setup Random Module");
        return(True);

    def connect(self, AddrStr):
        if AddrStr == 'Bool':
            ADDR = RAND_BOOL;
        elif AddrStr == 'Byte':
            ADDR = RAND_BYTE;
        elif AddrStr == 'Word':
            ADDR = RAND_WORD;
        elif AddrStr == 'DWord':
            ADDR = RAND_DWORD;
        elif AddrStr == 'Float':
            ADDR = RAND_FLOAT;
        elif AddrStr == 'Double':
            ADDR = RAND_DOUBLE;
        else:
            self.Logger.error("Unknown type %s"%AddrStr);
            return(None);
        return( pyDCPU.MasterConnection(self, ADDR) );

    def read(self, Con, len):
        if Con.Address == RAND_BOOL:
            return(GetRandBool());
        elif Con.Address == RAND_BYTE:
            return(GetRandByte());
        elif Con.Address == RAND_WORD:
            return(GetRandWord());
        elif Con.Address == RAND_DWORD:
            return(GetRandDWord());
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
    return( struct.pack("B",random.choice( (1,0) )) );
def GetRandByte():
    return( struct.pack("B",random.randint(0,100)) );
def GetRandWord():
    return( struct.pack("H",random.randint(0,100)) );
def GetRandDWord():
    return( struct.pack("I",random.randint(0,100)) );
def GetRandFloat():
    return( struct.pack('f',random.random()) );
def GetRandDouble():
    return( struct.pack('d',random.random()) ); 
