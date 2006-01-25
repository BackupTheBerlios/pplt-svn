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
        try: self.__TimeOut = float(tmp);
        except:
            self.Logger.warning("TimeOut in wrong format: set to 0.0");
            self.__TimeOut = 0.0;

    def connect(self, AddrStr):
        hp = AddrStr.split(':');
        if not len(hp) == 2:
            raise pyDCPU.ModuleError("Mad format for address: %s! Should be: \"host:port\""%str(AddrStr));
        Addr = hp[0];
        try: Port = int(hp[1]);
        except: raise pyDCPU.ModueError("Port %s is not a number"%str(hp[1]));

        SCon = SocketConnection(Addr,Port,self.__TimeOut);
        if not SCon: self.Logger.warning("Unable to connect: try later");
        return(pyDCPU.MasterConnection(self, SCon));


    def read(self, Con, Len):
        SCon = Con.Address;
        if not SCon.GetState(): SCon.ReConnect();

        try: return(SCon.Read(Len));
        except socket.error (errno, txt): raise(pyDCPU.ModuleError("Unable to read from connection: %s"%str(txt)));
        except socket.timeout: raise pyDCPU.ModuleError("Timeout!");


    def write(self, Con, Data):
        SCon = Con.Address;
        if not SCon.GetState(): SCon.ReConnect();

        try: return(SCon.Write(Data));
        except socket.error, e: raise pyDCPU.ModuleError("Unable to write: %s"%str(e));
        except socket.timeout: raise pyDCPU.ModuleError("Timeout");




#
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
