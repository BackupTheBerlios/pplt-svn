import smtplib;
import pyDCPU;
import binascii;


class Object(pyDCPU.MasterObject):
    def setup(self):
        self.Logger.info("Setup SendMail");
        self.__FROM = self.Parameters.get('from');
        if not self.__FROM:
            self.Logger.error('No FROM addr. is given');
            return(False);

        self.__HOST = self.Parameters.get('host');
        if not self.__HOST:
            self.Logger.error('No HOST is given');
            return(False);

        if not self.Parameters.has_key('port'):
            self.__PORT = 25;
            self.Logger.debug("No Port is given: set to 25");
        else:
            try:
                self.__PORT = int(self.Pararmeters.get('port'));
            except:
                self.Logger.error("Invalid port number format: set to 25");
                self.__PORT = 25;
        return(True);

    def connect(self, AddrStr):
        if not AddrStr:
            self.Logger.error("This module needs a address from children");
            return(None);
        self.Logger.debug("make connection with address \"%s\""%AddrStr);
        con = pyDCPU.MasterConnection(self, AddrStr);
        return(con);

    def read(self, Connection, Length):
        self.Logger.error("This module is write-only");
        raise pyDCPU.IOModError;

    def write(self, Connection, Data):
        try:
            server = smtplib.SMTP(self.__HOST, self.__PORT);
        except:
            self.Logger.error("Error while connect to HOST %s:%i"%(self.__HOST,self.__PORT));
            raise pyDCPU.FatIOModError;

        MSG = "From: %s\r\nTo: %s\r\n\r\n%s"%(self.__FROM, Connection.Address, binascii.b2a_qp(Data));
        try:
            server.sendmail(self.__FROM, Connection.Address, MSG);
        except:
            self.Logger.error("Unable to send mail!");
            raise pyDCPU.IOModError;
        return(len(Data));
        
    def flush(self):
        return(True);


