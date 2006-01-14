import pyDCPU;
import httplib;

class Object(pyDCPU.MasterObject):
    def setup(self):
        self.__HOST = self.Parameters.get('host');
        if not self.__HOST:
            self.Logger.error("no host name");
            return(False);

        if self.Parameters.has_key('port'):
            try:
                self.__PORT = int(self.Parameters.get('port'));
            except:
                self.Logger.warning("Invalid port number format: use 80");
                self.__PORT = 80;
        else:
            self.__PORT = 80;
        return(True);


    def connect(self, AddrStr):
        if not AddrStr:
            self.Logger.error("No path!!!");
            return(None);
        return(pyDCPU.MasterConnection(self, AddrStr));
    

    def read(self, Connection, Len):
        try:
            server = httplib.HTTPConnection(self.__HOST, self.__PORT);
        except:
            self.Logger.error("Error while connect to host %s:%i"%(self.__HOST, self.__PORT));
            raise pyDCPU.IOModError;

        server.request('GET',Connection.Address);
        res = server.getresponse();
        
        if not 200 == int(res.status):
            self.Logger.error("HTTP returned \"%s\""%res.reason);
            raise IOModError;
        return(res.read(Len));


    def write(self, Connection, Data):
        self.Logger.error("This module is read only");
        raise pyDCPU.IOModError;

    def flush():
        self.Logger.debug("flush: Do nothing.");
        return(True);
    
