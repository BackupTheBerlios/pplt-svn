import pyDCPU;
import struct;
import Check;

A200_CHECK = 1;
A200_VALUE = 2;


class A200Address:
    def __init__(self, AddrStr):
        self.__Valid = False;
        self.__Type  = None;
        self.__Number= 0

        if AddrStr == 'check':
            self.__Valid = True;
            self.__Type  = A200_CHECK;
            self.__Number = 0;
        elif not self.__Valid:
            try:
                self.__Valid = True;
                self.__Type = A200_VALUE;
                self.__Number = int(AddrStr);
            except:
                self.__Valid = False;
        if self.__Number < 0:
            self.__Valid = False;
            
    def IsValid(self):
        return(self.__Valid);
    def GetType(self):
        return(self.__Type);
    def GetNumber(self):
        return(self.__Number);


    
class Object(pyDCPU.MasterObject):
    def setup(self):
        self.__LastValues = None;
        self.Logger.info("Setup A200");
        # no setup needed
        return(True);

    def connect(self, AddrStr):
        Addr = A200Address(AddrStr);
        if not Addr.IsValid():
            self.Logger.error("Invalid Address: %s"%AddrStr);
            return(None);
        Con = pyDCPU.MasterConnection(self, Addr);
        return(Con);

    def read(self, Connection, Len):
        if Connection.Address.GetType() == A200_CHECK:
            try:
                tmp = Check.A200Check(self.Connection);
            except pyDCPU.ModError:
                self.Logger.error("IOError");
                raise pyDCPU.IOModError;
            
            if tmp == None:
                self.__LastValues= None;
                self.Logger.debug("A200 returned Error");
                return(struct.pack("B",0));
            else:
                self.__LastValues = tmp;
                self.Logger.debug("Got %i Values"%len(tmp));
                return(struct.pack("B",1));
        elif Connection.Address.GetType() == A200_VALUE:
            if not self.__LastValues:
                self.Logger.error("Read from 'check' before!!!");
                raise pyDCPU.IOModError;

            if (len(self.__LastValues)-1) < Connection.Address.GetNumber():
                self.Logger.error("Out of range");
                raise pyDCPU.IOModError;

            val = self.__LastValues[Connection.Address.GetNumber()];
            if val == 'e':
                self.Logger.warning("Calculation error");
                return(struct.pack("I",0));
            return(struct.pack("I",int(val)));

        self.Logger.error("Bat Address");
        raise pyDCPU.ModError;

    def write(self, Connection, data):
        self.Logger.error("This module is read only");
        raise pyDCPU.ReadOnlyModError;


            
