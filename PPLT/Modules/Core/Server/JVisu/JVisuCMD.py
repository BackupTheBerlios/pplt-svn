import struct;
from JVisuTypes import *;
import JVisuConverter;
import binascii;
import logging;

class JVisuCMDHDR:
    def __init__(self, CMD = 0, Type = 0):
        self.__CMD = CMD;
        self.__Type = Type;
        self.__Len = 0;
        self.__Logger = logging.getLogger("pyDCPU");

    def HDRFromString(self, Str):
        if len(Str)>=4:
            DATA = Str[0:4];
            (self.__CMD,
             self.__Type,
             self.__Len) = struct.unpack("BBH",DATA);
            return(True);
        return(False);

    def HDRToString(self,Data):
        self.__Len = len(Data)+4;
        FMT = "BBH%is"%(len(Data));
        DATA = struct.pack(FMT, self.__CMD, self.__Type, self.__Len, Data);
        return(DATA);

    def GetCMD(self):
        return(self.__CMD);
    def GetType(self):
        return(self.__Type);
    def GetLen(self):
        return(self.__Len);



class JVisuCMD(JVisuCMDHDR):
    def __init__(self, Sock = None, CMD = 0, Type = 0, ID = 0, Rate = 0, DATA = None, Value = None):
        JVisuCMDHDR.__init__(self, CMD, Type);
        self.__Logger = logging.getLogger('pyDCPU');
        self.__ID = ID;
        self.__Rate = Rate;
        self.__DATA = DATA;
        self.__Value = Value;
        self.__Sock = Sock;
        if self.__Sock:
            self.FromSock();



    def FromSock(self):
        Str = self.__Sock.recv(4);
        if not len(Str) == 4:
            #self.__Logger.warning("To less data recv");
            return(False);
        
        self.__Logger.debug("Got Hader: %s"%binascii.b2a_hex(Str));
        self.HDRFromString(Str);
        self.__Logger.debug("Get Packet %i"%self.GetLen());
        Str = self.__Sock.recv(self.GetLen()-4);
        if not len(Str) == (self.GetLen()-4):
            self.__Logger.warning("To less data");
            return(False);

        if self.GetCMD() == JVISU_CMD_REGVAR:
            self.__Logger.debug("CMD: register var");
            FMT = "II%is"%(self.GetLen()-12);
            (self.__ID,
             self.__Rate,
             self.__DATA) = struct.unpack(FMT,Str);
            self.__Logger.debug("Add var with id %i"%self.__ID);
            return(True);
        elif self.GetCMD() == JVISU_CMD_DELVAR:
            self.__Logger.debug("CMD: unregister var");
            (self.__ID,) = struct.unpack("I",Str);
            return(True);
        elif self.GetCMD() == JVISU_CMD_SNDVAR:
            self.__Logger.debug("CMD: set value");
            FMT = "I%is"%(self.GetLen()-8);
            (self.__ID,self.__DATA) = struct.unpack(FMT,Str);
        else:
            self.__Logger.warning("Command %x not implemented"%self.GetCMD());
            self.__Logger.debug("LINE: %s"%binascii.b2a_hex(Str));
        return(False);

    def ToString(self, Data = None):
        if Data:
            self.__DATA = Data;
        if self.__Value != None:
            self.__DATA = JVisuConverter.ToData(self.__Value, self.GetType());

        if self.GetCMD() == JVISU_CMD_SNDVAR:
            FMT = "I%is"%(len(self.__DATA));
            p = struct.pack(FMT, self.GetID(), self.__DATA);
            return(self.HDRToString(p));
        else:
            self.__Logger.warning("Unknown CMD %x"%self.GetCMD());
            return(None);

    def GetID(self):
        return(self.__ID);
    def GetRate(self):
        return(self.__Rate);
    def GetData(self):
        return(self.__DATA);
    def GetValue(self):
        return(self.__Value);
