import pyDCPU;
import pyDCPU.UserDB;
import logging;

class ExportableSymbolTree:
    def __init__(self, SymbolTree, UserDB, DefaultUser):
        self.__Logger = logging.getLogger('pyDCPU');
        
        if not isinstance(SymbolTree, pyDCPU.SymbolTree):
            raise pyDCPU.Error;
        if not isinstance(UserDB, pyDCPU.UserDB.UserDB):
            raise pyDCPU.Error;
            
        self.__SymbolTree = SymbolTree;
        self.__UserDB = UserDB;
        self.__DefaultSession = UserDB.GetSession(DefaultUser);
        


    def Logon(self, UserName, Password):
        return(self.__UserDB.Logon(UserName, Password));

    def Logoff(self, SessionID):
        return(self.__UserDB.Logoff(SessionID));

    def GetValue(self, SymbolPath, SessionID):
        if not SessionID:
            SessionID = self.__DefaultSession;
        return(self.__SymbolTree.GetValue(SymbolPath,SessionID));

    def SetValue(self, SymbolPath, Value, SessionID):
        if not SessionID:
            SessionID = self.__DefaultSession;        
        return(self.__SymbolTree.SetValue(SymbolPath, Value, SessionID));

    def ListFolders(self, PathToFolder, SessionID):
        if not SessionID:
            SessionID = self.__DefaultSession;
        return(self.__SymbolTree.ListFolder(PathToFolder, SessionID));

    def ListSymbols(self, PathToFolder, SessionID):
        if not SessionID:
            SessionID = self.__DefaultSession;
        return(self.__SymbolTree.ListSymbols(PathToFolder, SessionID));
