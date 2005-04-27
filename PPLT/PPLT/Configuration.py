import os.path;
import sys;

class Config:
	def __init__(self):
		self.__LogLevel   = 'debug';
		self.__LogFile    = None; #os.path.normpath(sys.exec_prefix+'/PPLT/LogFile.log');
		self.__SysLog     = False;
		self.__BasePath   = os.path.normpath(sys.exec_prefix+'/PPLT/');
		self.__UserDB     = os.path.normpath(self.__BasePath+'/UserDB.xml');
		self.__DBPath     = os.path.normpath(self.__BasePath+'/Mods');
		self.__IconPath   = os.path.normpath(self.__BasePath+'/icons');
    
	def GetBasePath(self):
		return(self.__BasePath);
	def GetUserDB(self):
		return(self.__UserDB);
	def GetDBPath(self):
		return(self.__DBPath);
	def GetIconPath(self):
		return(self.__IconPath);
	def GetLogLevel(self):
		return(self.__LogLevel);
	def GetLogFile(self):
		return(self.__LogFile);
	def GetSysLog(self):
		return(self.__SysLog);
