import os.path;
import sys;

class Config:
    def __init__(self):
        self.__LogLevel   = 'debug';
        self.__LogFile    = os.path.normpath(sys.exec_prefix+'/PPLT/LogFile.log');
        self.__SysLog     = False;
        self.__UserDB     = os.path.normpath(sys.exec_prefix+'/PPLT/UserDB.xml');
        self.__ModuleDB   = os.path.normpath(sys.exec_prefix+'/PPLT/ModuleDB.xml');
        self.__ModulePath = os.path.normpath(sys.exec_prefix+'/PPLT');

    def GetUserDB(self):
        return(self.__UserDB);

    def GetModulePath(self):
        return(self.__ModulePath);
    def GetModuleDB(self):
        return(self.__ModuleDB);

    def GetLogLevel(self):
        return(self.__LogLevel);
    def GetLogFile(self):
        return(self.__LogFile);
    def GetSysLog(self):
        return(self.__SysLog);
