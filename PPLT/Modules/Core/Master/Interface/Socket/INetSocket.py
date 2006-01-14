import pyDCPU;
import socket;
import sys;


class Object(pyDCPU.MasterObject):
    def setup(self):
        self.Logger.info("Setup Socket-Module");
        tmp = self.Parameters.get('TimeOut');
        if not tmp:
            self.Logger.debug("No TimeOut: set to 0.0");
            self.__TimeOut = 0.0;
        try:
            self.__TimeOut = float(tmp);
        except:
            self.Logger.warning("TimeOut in wrong format: set to 0.0");
            self.__TimeOut = 0.0;
        return(True);


    def connect(self, AddrStr):
        hp = AddrStr.split(':');
        if not len(hp) == 2:
            self.Logger.warning("Address: Host:Port");
            return(None);
        Addr = hp[0];
        try:
            Port = int(hp[1]);
        except:
            self.Logger.warning("Port is not a number");
            return(None);
        SCon = SocketConnection(Addr,Port,self.__TimeOut);
        if not SCon:
            self.Logger.warning("Unable to connect: try later");
        return(pyDCPU.MasterConnection(self, SCon));


    def read(self, Con, Len):
        SCon = Con.Address;
        if not SCon.GetState():
            SCon.ReConnect();

        try:
            return(SCon.Read(Len));
        except socket.error (errno, txt):
            self.Logger.warning("Error while read: %s(%i)"%(errno, txt));
            raise(pyDCPU.IOModError);
            return(None);
        except socket.timeout:
            self.Logger.warning("Timeout");
            raise(pyDCPU.TimeOutError);
            return(None);
        except:
            self.Logger.warning("Error while read");
            raise(pyDCPU.FatIOModError);
        return(None);


    def write(self, Con, Data):
        SCon = Con.Address;
        if not SCon.GetState():
            SCon.ReConnect();

        try:
            return(SCon.Write(Data));
        except socket.error (errno, txt):
            self.Logger.warning("Error while write: %s(%i)"%(errno, txt));
            raise(pyDCPU.IOModError);
            return(None);
        except socket.timeout:
            self.Logger.warning("Timeout!?!");
            raise(pyDCPU.TimeOutError);
            return(None);
        except:
            self.Logger.warning("Error while write");
            raise(pyDCPU.FatIOModError);
        return(None);



# A simple Socket-Connection-Class:
#
class SocketConnection:
    def __init__(self, Host, Port, TimeOut):
        self.__Host = Host;
        self.__Port = Port;
        self.__TimeOut = TimeOut;
        self.__State = False;
        self.Connect();


    def Connect(self):
        return(self.ReConnect());
    def ReConnect(self):
        self.__Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);

        if not self.__Socket:
            self.Logger.error("Error while create socket");
            self.__State = False;
            return(False);

        if self.__Socket.connect( (self.__Host,self.__Port) ):
            self.Logger.error("Error while connect");
            self.__State = False;
            return(False);
        self.__Socket.settimeout(self.__TimeOut);
        self.__State = True;
        return(True);

    def Close(self):
        return(self.__Socket.close());

    def Read(self, Len):
        return(self.__Socket.recv(Len));
    def Write(self, Data):
        return(self.__Socket.send(Data));

    def GetState(self):
        return(self.__State);
