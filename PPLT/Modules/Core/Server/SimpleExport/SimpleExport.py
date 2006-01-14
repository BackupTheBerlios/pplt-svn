import pyDCPU;
import SimpleXMLRPCServer;
import logging;


class Object(pyDCPU.ExportObject):
    def setup(self):
        if self.Parameters.get('Address'):
            self.__BindAddress = self.Parameters['Address'];
        else:
            self.__BindAddress = '127.0.0.1';
        self.Logger.debug("Will bind to addr %s"%self.__BindAddress);

        try:
            self.__Port = int(self.Parameters['Port']);
        except:
            self.__Port = 8080;
        self.Logger.debug("Will bind to port %i"%self.__Port);
        
        self.__ExporterInstance = SimpleExport(self.SymbolTree);

        try:
            self.__Server = SimpleXMLRPCServer.SimpleXMLRPCServer((self.__BindAddress,
                                                                   self.__Port));
        except:
            self.Logger.error("Error while setup Server");
            return(False);

        self.__Server.register_introspection_functions();
        self.__Server.register_instance(self.__ExporterInstance);
        self.__Loop = True;
        return(True);

    def start(self):
        while self.__Loop:
            self.__Server.handle_request();

    def stop(self):
        self.__Loop = False;
        return(True);


class SimpleExport:
    def __init__(self, SymbolTree):
        self.__Logger = logging.getLogger('pyDCPU');
        self.__SymbolTree = SymbolTree;
        self.__DefaultSession = None;
        self.__LastError = False;
        
    def _dispatch(self, name, parameters):
        if name == 'get':
            if len(parameters) == 1:
                val = self.HandleGet(parameters[0], self.__DefaultSession);
                if val == None:
                    self.__LastError = True;
                    return(False);
                self.__LastError = False;
                return(val);
            elif len(parameters)==2:
                val = self.HandleGet(parameters[0], parameters[1]);
                if val == None:
                    self.__LastError = True;
                    return(False);
                self.__LastError = False;
                return(val);
            #else
            self.__Logger.info("Request has to many or none parameters");
            self.__LastError = True;
            return(False);
        elif name == 'set':
            if len(parameters) == 2:
                val = self.HandleSet(parameters[0], parameters[1], self.__DefaultSession);
                if val == None:
                    self.__LastError = True;
                    return(False);
                self.__LastError = False;
                return(val);
            elif len(parameters) == 3:
                val = self.HandleSet(parameters[0], parameters[1], parameters[2]);
                if val == None:
                    self.__LastError = True;
                    return(False);
                self.__LastError = False;
                return(val);
                self.__Logger.warning("Request has many or to less parameters");
                self.__LastError = True;
            return(False);
        elif name == 'listfolders':
            if len(parameters) == 1:
                self.__Logger.debug('List %s'%parameters[0]);
                list = self.HandleListFolders(parameters[0],self.__DefaultSession);
                if not list:
                    return(False);
                return(list);
            elif len(parameters)==2:
                self.__Logger.debug('List %s'%parameters[0]);
                list = self.HandleListFolders(parameters[0],parameters[1]);
                if not list:
                    return(False);
                return(list);       
            self.__Logger.warning("listfolders need 1or2 parameters");
            return(False);
        elif name == 'listsymbols':
            if len(parameters) == 1:
                self.__Logger.debug('List %s'%parameters[0]);
                list = self.HandleListSymbols(parameters[0],self.__DefaultSession);
                if not list:
                    return(False);
                return(list);
            elif len(parameters)==2:
                self.__Logger.debug('List %s'%parameters[0]);
                list = self.HandleListSymbols(parameters[0],parameters[1]);
                if not list:
                    return(False);
                return(list);       
            self.__Logger.warning("listsymbols need 1or2 parameters");
            return(False);
        elif name == 'logon':
            if not len(parameters)==2:
                self.__Logger.warning("Request need exact 2 arguments");
                return(False);
            session = self.HandleLogon(parameters[0],parameters[1]);
            if not session:
                return(False);
            return(session);
        elif name == 'logoff':
            if not len(parameters)==1:
                self.__Logger.warning("Logoff need only one parameter");
                return(False);
            return(self.__SymbolTree.Logoff(parameters[0]));
        elif name == 'error':
            return(self.__LastError);
        self.__Logger.warning("Command \"%s\" not known!"%name);
        self.__LastError = True;
        return(False);
        

    def HandleGet(self, Path, SessionID):
        self.__Logger.debug("Read %s"%Path);
        return(self.__SymbolTree.GetValue(Path,SessionID));


    def HandleSet(self, Path, Value, SessionID):
        self.__Logger.debug("Set %s to %s"%(Path,str(Value)));
        return(self.__SymbolTree.SetValue(Path, Value, SessionID));


    def HandleListFolders(self, Path, SessionID):
        return(self.__SymbolTree.ListFolders(Path, SessionID));


    def HandleListSymbols(self, Path, SessionID):
        return(self.__SymbolTree.ListSymbols(Path, SessionID));


    def HandleLogon(self, User, Pass):
        self.__Logger.debug("Logon: %s"%User);
        return(self.__SymbolTree.Logon(User,Pass));


    def HandleLogoff(self, SessionID):
        self.__Logger.debug("Logoff: %s"%SessionID);
        return(self.__SymbolTree.Logoff(SessionID));


#    def HandleError(self, parameters):
#        pass;
