import pyDCPU;
import struct;
import xdrlib;
import random;
import string;

RAND_BOOL   = 1;
RAND_INTEGER  = 2;
RAND_FLOAT  = 3;
RAND_STRING = 4;
RAND_ARRAYBOOL = 5;
RAND_ARRAYINTEGER = 6;
RAND_ARRAYFLOAT = 7;
RAND_ARRAYSTRING = 8;
RAND_STREAM = 9;
RAND_SEQUENCE = 10;


class Object(pyDCPU.MasterObject):
    def setup(self): self.Logger.info("Setup Random Module");

    def connect(self, AddrStr):
        if AddrStr == 'Bool':
            ADDR = RAND_BOOL;
        elif AddrStr == 'Integer':
            ADDR = RAND_INTEGER;
        elif AddrStr == 'Float':
            ADDR = RAND_FLOAT;
        elif AddrStr == 'String':
            ADDR = RAND_STRING;
        elif AddrStr == 'ArrayBool':
            ADDR = RAND_ARRAYBOOL;
        elif AddrStr == 'ArrayInteger':
            ADDR = RAND_ARRAYINTEGER;
        elif AddrStr == 'ArrayFloat':
            ADDR = RAND_ARRAYFLOAT;
        elif AddrStr == 'ArrayString':
            ADDR = RAND_ARRAYSTRING;
        elif AddrStr == 'Stream':
            ADDR = RAND_STREAM;
        elif AddrStr == 'Sequence':
            ADDR = RAND_SEQUENCE;
        else: raise pyDCPU.ModuleError("Unknown address: %s"%AddrStr);
        if ADDR == RAND_STREAM: return pyDCPU.StreamConnection(self, ADDR);
        return( pyDCPU.ValueConnection(self, AddrStr, ADDR) );

    def read(self, Con, length=None):
        if Con.Address == RAND_BOOL:
            return(GetRandBool());
        elif Con.Address == RAND_INTEGER:
            return(GetRandInt());
        elif Con.Address == RAND_FLOAT:
            return(GetRandFloat());
        elif Con.Address == RAND_STRING:
            return(GetRandString());
        elif Con.Address == RAND_ARRAYBOOL:
            return(GetRandArrayOfBool());
        elif Con.Address == RAND_ARRAYINTEGER:
            return(GetRandArrayOfInt());
        elif Con.Address == RAND_ARRAYFLOAT:
            return(GetRandArrayOfFloat());
        elif Con.Address == RAND_ARRAYSTRING:
            return(GetRandArrayOfString());
        elif Con.Address == RAND_STREAM:
            return(GetRandString(length));
        elif Con.Address == RAND_SEQUENCE:
            return(GetRandString());
        else:
            self.Logger.error("Invalid Address!!!");
            raise pyDCPU.FatIOModError;

    def write(self, Con, Data):
        self.Logger.error("This is a read only module!!!");
        raise pyDCPU.IOModError;



def GetRandBool():
    if random.choice((1,0)): return True;
    return False;

def GetRandInt():
    return random.randint(0,100);

def GetRandFloat():
    return random.random();

def GetRandString(length = 79):
    length = random.randint(1,length);
    buff = str();
    for n in range(length): buff += random.choice(string.printable);
    return buff;
    
def GetRandArrayOfBool():
    t = list();
    for n in range(3): t.append(GetRandBool());
    return t;

def GetRandArrayOfInt():
    t = list();
    for n in range(3): t.append(GetRandInt());
    return t;

def GetRandArrayOfFloat():
    t = list();
    for n in range(3): t.append(GetRandFloat());
    return t;

def GetRandArrayOfString():
    t = list();
    for n in range(3): t.append(GetRandString());
    return t;
    
