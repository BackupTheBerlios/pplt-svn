# ############################################################################ #
# This is part of the PPLT project. PPLT is a framework for industrial         # 
# communication.                                                               # 
# Copyright (C) 2003-2005 Hannes Matuschek <hmatuschek@gmx.net>                # 
#                                                                              # 
# This library is free software; you can redistribute it and/or                # 
# modify it under the terms of the GNU Lesser General Public                   # 
# License as published by the Free Software Foundation; either                 # 
# version 2.1 of the License, or (at your option) any later version.           # 
#                                                                              # 
# This library is distributed in the hope that it will be useful,              # 
# but WITHOUT ANY WARRANTY; without even the implied warranty of               # 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU             # 
# Lesser General Public License for more details.                              # 
#                                                                              # 
# You should have received a copy of the GNU Lesser General Public             # 
# License along with this library; if not, write to the Free Software          # 
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA    # 
# ############################################################################ # 

# Changelog:
# 2005-05-27:
#	(Start change log.)
#	Release as Version 0.2.0

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
