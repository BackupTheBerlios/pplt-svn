import pyDCPU;
import Configuration;
import Logging;
import AliasTable;
import Install;


MODUS_FMT_OCTAL = 1;
MODUS_FMT_STRING = 2;
MODGRP_MASTER = 'Master';
MODGRP_SERVER = 'Server';
MODGRP_DEVICE = 'Device';

class System:
    def __init__(self):
        """ This is the PPLTSystem class all work can be don over a instanc if this class """
        self.__Config = Configuration.Config();
        self.__Core = pyDCPU.Core(UserDBFile = self.__Config.GetUserDB(),
                                  LogLevel = self.__Config.GetLogLevel(),
                                  LogFile = self.__Config.GetLogFile(),
                                  SysLog = self.__Config.GetSysLog());
        self.__Logger = Logging.Logger();
        #self.__ModuleDB = Module.DataBase(self.__Config.GetModuleDB());
        
    
    # ######################################################################## #
    # Module/Device handling                                                   #
    # ######################################################################## #
    # - install                                                                #
    # - uninstall                                                              #
    # ######################################################################## #
    def Install(self, InstallFile):
        """ This method will install all core-modules and pplt-devices listed in
 the InstallFile. """
        return(self.__ModuleDB.Install(InstallFile));
            
    def UnIstall(self, ModuleName):
        """ This method will uninstall the given module/divice """
        return(self.__ModuleDB.UnInstall(ModuleName));
        
    def ListKnownModules(self, ModGroup):
        return(self.__ModuleDB.List(ModGroup));
    
    def GetModuleInfo(self, Name):
        """ Return a info object... """
        return(self.__ModuleDB.Info(Name));
        
    
    
    # ######################################################################## #
    # User/Group management                                                    #
    # ######################################################################## #
    # ######################################################################## #
    def CreateGroup(self, ParentGroup, Name):
        pass;
    def DeleteGroup(self, Name):
        pass;
    def ListGroups(self, Name):
        pass;
    def CreateMember(self, Group, Name, Password, Description):
        pass;
    def DeleteMember(self, Name):
        pass;
    def ListMembers(self, Name):
        pass;
    def CheckPassword(self, Name, Password):
        pass;
    def ChangePassword(self, Name, NewPassword):
        pass;
    def SetSuperUser(self, Name):
        pass;
    def GetSuperUser(self):
        pass;
        
        
    
    # ######################################################################## #
    # Manage Devices                                                           #
    # ######################################################################## #
    # ######################################################################## #
    def LoadDevice(self, DeviceName, Alias):
        """ return a device object """
        pass;
    def UnLoadDevice(self, Alias):
        pass;
    def ListDevices(self):
        pass;
    
            
    
    # ######################################################################## #
    # Manage SymbolTree                                                        #
    # ######################################################################## #
    # ######################################################################## #
    def CreateFolder(self, Path, Modus='600', Owner=None, Group=None):
        pass;
    def DeleteFolder(self, Path, Recur=False):
        pass;
    def ListFolders(self, Path):
        pass;
    def CraeteSymbol(self, Path, Slot, Modus='600', Owner=None, Group=None):
        pass;
    def DeleteSymbol(self, Path):
        pass;
    def ListSymbols(self, Path):
        pass;
    def GetModus(self, Path, Format=MODUS_FMT_OCTAL):
        pass;
    def ChangeModus(self, Path, Modus):
        pass;
    def GetOwner(self, Path):
        pass;
    def ChangeOwner(self, Path, Owner):
        pass;
    def GetGroup(self, Path):
        pass;
    def ChangeGroup(self, Path, Group):
        pass;
    def GetValue(self, Path):
        pass;
    def SetValue(self, Path, Value):
        pass;
        
        
        
    # ######################################################################## #
    # Manage Server                                                            #
    # ######################################################################## #
    # ######################################################################## #
    def LoadServer(self, Name, Parameters, DefaultUser):
        pass;
    def UnLoadServer(self, Name):
        pass;        
    def ListRunningServers(self):
        pass;
        
