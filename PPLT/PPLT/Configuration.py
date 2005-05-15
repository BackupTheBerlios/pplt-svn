import ConfigParser;
import os.path;
import sys;

class Config:
	def __init__(self, ConfigFileName = None):
		if not ConfigFileName:
			ConfigFileName = os.path.normpath(sys.exec_prefix+"/PPLT/PPLT.conf");
		self.__Conf = ConfigParser.SafeConfigParser();
		self.__Conf.read(ConfigFileName);

    
	def GetBasePath(self):
		tmp = self.__Conf.get("path","BasePath");
		if tmp == "AUTOMATIC":
			return(os.path.normpath(sys.exec_prefix+"/PPLT/"));
		return(os.path.normpath(tmp));
	
	def GetUserDB(self):
		tmp = self.__Conf.get("path","UserDB");
		if tmp == "AUTOMATIC":
			return(os.path.normpath(sys.exec_prefix+"/PPLT/UserDB.xml"));
		return(os.path.normpath(tmp));

	def GetDBPath(self):
		tmp = self.__Conf.get("path","DBPath");
		if tmp == "AUTOMATIC":
			return(os.path.normpath(sys.exec_prefix+"/PPLT/Mods/"));
		return(os.path.normpath(tmp));

	def GetIconPath(self):
		tmp = self.__Conf.get("path","IconPath");
		if tmp == "AUTOMATIC":
			return(os.path.normpath(sys.exec_prefix+"/PPLT/icons/"));
		return(os.path.normpath(tmp));

	def GetLang(self):
		return(self.__Conf.get("lang","language"));

	def GetAltLang(self):
		return(self.__Conf.get("lang","alt-lang"));

	def GetCoreLogLevel(self):
		tmp = self.__Conf.get("logging","CoreLevel");
		if tmp == "No":
			return(None);
		return(tmp);
	
	def GetPPLTLogLevel(self):
		tmp = self.__Conf.get("logging","PPLTLevel");
		if tmp == "No":
			return(None);
		return(tmp);

	def GetLogFile(self):
		tmp = self.__Conf.get("logging","File");
		if tmp == "No":
			return(None);
		return(tmp);

	def GetSysLog(self):
		tmp = self.__Conf.get("logging","SysLog");
		if tmp == "Yes":
			return(True);
		return(False);
