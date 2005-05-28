import pyDCPU;
import socket;
import thread;
import JVisuClientHandler;
import traceback;


class Object (pyDCPU.ExportObject):
    def setup(self):
        self.Logger.info("Setup JVisuServer");

        self.__Address = self.Parameters.get("Address");
        if not self.__Address:
            self.Logger.error("Need address");
            return(False);

        tmp = self.Parameters.get("Port");
        if not tmp:
            self.__Port = 2200;
        else:
            try:
                self.__Port = int(tmp);
            except:
                self.__Port = 2200;

        self.__ServSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        if not self.__ServSock:
            self.Logger.error("Error while create socket");
            return(False);

        try:
            self.__ServSock.bind( (self.__Address, self.__Port) );
        except:
            self.Logger.error("Error while bind to %s:%i"%(self.__Address,self.__Port));
            return(False);
            
        self.__ServSock.listen(50);
        return(True);

    def start(self):
        self.__Loop = True;
        self.__ServSock.setblocking(0);
        while self.__Loop:
            try:
                (Client, CAddr) = self.__ServSock.accept();
            except:
                continue;
            self.Logger.debug("New Client at %s"%(str(CAddr)));
            try:
                if not thread.start_new_thread(JVisuClientHandler.HandleClient,
                                           (Client, CAddr, self.SymbolTree, self)):
                    self.Logger.error("Unable to create new client-handler");
                    Client.close();
            except:
                self.Logger.error("Exception while thread creation");
                traceback.print_exc();

        return(True);

    def stop(self):
        self.__Loop = False;
        self.__ServSock.close();
        return(True);

    def DoRun(self):
        return(self.__Loop);
