from JVisuTypes import *;
import JVisuCMD;
import logging;
import time;


class JVisuVar:
    def __init__(self, Name, ID, Rate, Type, SymbolTree, Sock):
        self.__Name = Name;
        self.__ID = ID;
        self.__Rate = Rate;
        self.__Type = Type;
        self.__SymbolTree = SymbolTree;
        self.__LastUpdate = time.time();
        self.__Socket = Sock;
        self.__Value = 1;
        self.__Logger = logging.getLogger('pyDCPU');
        self.__Logger.debug("Update start time %f"%self.__LastUpdate);

    def NeedUpdate(self):
        diff = time.time()-self.__LastUpdate;
        if int(diff*1000) >= self.__Rate:
            return(True);
        return(False);

    def Update(self):
        self.__Logger.debug("Update %i"%self.__ID);
        self.__Value = self.__SymbolTree.GetValue(self.__Name, None);
        if self.__Value == None:
            self.__Logger.warning("Error while get value from symbol %s"%self.__Name);
            return(False);
        UP = JVisuCMD.JVisuCMD(CMD = JVISU_CMD_SNDVAR,
                               Type = self.__Type,
                               ID = self.__ID,
                               Value = self.__Value);
        tmp = UP.ToString();
        if not tmp:
            return(False);
        try:
            self.__Socket.send(tmp);
        except:
            return(False);
        self.__LastUpdate = time.time();
        return(True);

    def SetValue(self, Value):
        self.__Logger.debug("Set %s to %s"%(self.__Name, str(Value)));
        if not self.__SymbolTree.SetValue(self.__Name, Value, None):
            self.__Logger.warning("Error while set Value %s"%self.__Name);
            return(False);
        return(True);

