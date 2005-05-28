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

#CHANGELOG:
#	2005-05-27:
#		+ Start changelog. (sorry i missed it)
#		+ Release as Version 0.2.0 (alpha)
#		- Fixed wrong Symbol<->DeviceAlias association

import pyDCPU;
import Configuration;
import Logging;
import Install;
import Device;
import Server;
import DataBase;
import DeviceDescription;
import ServerDescription;
import gettext;

MODUS_FMT_OCTAL = 1;
MODUS_FMT_STRING = 2;
MODUS_FMT_INTEGER = 3;


class System:
	"""This is the PPLTSystem class all work can be done over a instanc if this 
 class. To get a instance of this class simply call:
   >>> obj = PPLT.System(). 
 
 There is a optional parameter for this method: "ConfigFile":
   >>> obj = PPLT.System(ConfigFile="/home/hannes/PPLT.conf")
 If you miss this parameter, the default sys.exec_prefix+"/PPLT/PPLT.conf" will
 be used. (will be installed)"""

	def __init__(self,ConfigFile=None):
		self.__Config = Configuration.Config(ConfigFile);					# Load Config

		self.__Core = pyDCPU.Core(ModulePath = self.__Config.GetBasePath(),
                                  UserDBFile = self.__Config.GetUserDB(),	# Start Core
                                  LogLevel = self.__Config.GetCoreLogLevel(),
                                  LogFile = self.__Config.GetLogFile(),
                                  SysLog = self.__Config.GetSysLog());

		self.__Logger = Logging.Logger(self.__Config.GetPPLTLogLevel(),
										self.__Config.GetLogFile(),
										self.__Config.GetSysLog());			# Start Logging

		self.__DataBase = DataBase.DataBase(self.__Config.GetDBPath());		# Load the Module/Device database
		self.__UserDataBase = self.__Core.GetTheUserDB();
		self.__DeviceHash = {}												# init some tables
		self.__ServerHash = {}												# ...
		self.__SymbolTable = {};											# Association between SymbolPath and SlotID
		self.__SymbolDeviceTable = {};										# Ass. btw. SymbolPath and DeviceAlias

	def Stop(self):
		""" This method will stop the system. Meaning stopping all servers,
 clear the whole Symboltree ans unload all devices. (no parameters needed)""" 
		#FIXME implement!
		pass;


    # ######################################################################## #
    # Module/Device handling                                                   #
    # ######################################################################## #
    # - install                                                                #
    # - uninstall                                                              #
    # ######################################################################## #
	def Install(self, InstallFile):
		""" This method will install all core-modules and pplt-devices listed in
 the InstallFile. Return True on success."""
		return(Install.InstallSet(InstallFile, self.__Config.GetBasePath()));
    
	def UnIstall(self, ModuleName):
		""" This method will uninstall the given module/divice/server. 
 Return True on success. """
		#FIXME implement!
		pass;

	def ListKnownServers(self, Class=None):
		""" List all Servers in Class. Return a list of strings. """
		return(self.__DataBase.ListServersIn(Class));

	def ListKnownServerClasses(self, Class=None):
		""" List all server classes in give class. if class is missed, all
 root-classes will be listed. Return a list of strings. """
		return(self.__DataBase.ListServerClassesIn(Class));

	def ListKnownDevices(self, Class=None):
		""" List all devices in class. Return a list of strings. """
		return(self.__DataBase.ListDevicesIn(Class));

	def ListKnownDeviceClasses(self, Class=None):
		""" List all device classes. like "ListKnownServerClasses()". 
Return a list of strings. """
		return(self.__DataBase.ListDeviceClassesIn(Class));

	def GetServerInfo(self, Name):
		""" Return a info object for the server Name. """
		srvFileName = self.__DataBase.GetServerFile(Name);
		if not srvFileName:
			self.__Logger.error("No server named \"%s\" found!"%Name);
			return(None);
		return(ServerDescription.LoadDescription(srvFileName,
													self.__Config.GetLang(),
													self.__Config.GetAltLang()));

	def GetDeviceInfo(self, Name):
		""" Return a info object for the device Name. """
		devFileName = self.__DataBase.GetDeviceFile(Name);
		if not devFileName:
			self.__Logger.error("No Device named \"%s\" found"%Name);
			return(None);
		self.__Logger.debug("Load info from file \"%s\""%devFileName);
		return(DeviceDescription.LoadDescription(devFileName,
													self.__Config.GetLang(),
													self.__Config.GetAltLang()));


    # ######################################################################## #
    # User/Group management                                                    #
    # ######################################################################## #
    # ######################################################################## #
	def CreateGroup(self, ParentGroup, Name):
		""" Create a group within ParentGroup with Name. If ParentGroup is None,
 a new root group will be generated. Return True on success. """ 
		return(self.__UserDataBase.CreateGroup(ParentGroup,Name));

	def DeleteGroup(self, Name):
		""" Delete a group. Return True on success."""
		return(self.__UserDataBase.DeleteGroup(Name));

	def ListGroups(self, GroupName = None):
		""" List all subgroups of given GroupName. If GroupName = None or 
 missed, all root groups will be listed. Return a list of string. """

		if not GroupName:
			group = self.__UserDataBase;
		else:
			group = self.__UserDataBase.GetGroupByName(GroupName);
		if not group:
			return([]);
		# list subgroups:
		return(group.ListSubGroups());

	def ListMembers(self, GroupName = None):
		""" List all members of a give group. Return a list of strings. """
		if not GroupName:
			return([]);
		group = self.__UserDataBase.GetGroupByName(GroupName);
		if not group:
			return([]);
		#list memebers:
		return(group.ListMembers());

	def CreateMember(self, Group, Name, Password, Description):
		""" Create a new group member for the give Group with Name, Password 
 and Description. Return True on success. """
		return(self.__UserDataBase.CreateMember(Group, Name, Password, Description));

	def DeleteMember(self, Name):
		""" Delete a user. Return True on success. """
		group = self.__UserDataBase.GetGroupByUserName(Name);
		if not group:
			self.__Logger.warning("No group found for user %s: does he/she exists?"%Name);
			return(False);
		return(self.__UserDataBase.DeleteMember(group.GetName(), Name));

	def CheckPassword(self, Name, Password):
		""" Test Password if its match to user Name's one. Return True on 
 success. """
		return(self.__UserDataBase.ValidUser(Name,Password));

	def ChangePassword(self, Name, Password):
		""" Change the passwd for a the user Name. """
		return(self.__UserDataBase.ChangePassword(Name,Password));

	def SetSuperUser(self, Name):
		""" Make user Name become the SuperUser. """
		return(self.__UserDataBase.SetSuperUser(Name));

	def GetSuperUser(self):
		""" Return the name of the SuperUser """
		return(self.__UserDataBase.GetSuperUser());
	def GetSuperUserGrp(self):
		""" Return the group of the SuperUser """
		return(self.__UserDataBase.GetSuperUserGrp());
	def GetGroupByUser(self, UserName):
		""" Return the group of given user """
		grp = self.__UserDataBase.GetGroupByUserName(UserName);
		if not grp:
			return(None);
		return(grp.GetName());
    
    # ######################################################################## #
    # Manage Devices                                                           #
    # ######################################################################## #
    # ######################################################################## #
	def LoadDevice(self, DeviceName, Alias, Parameters):
		""" Load an init device DeviceName as Alias with Parameters. Return
 True on success."""
		#check alias:
		if self.__DeviceHash.has_key(Alias):
			self.__Logger.error("Alias %s already exists"%Alias);
			return(False);
		# try to find out file name of DeviceName
		devFileName = self.__DataBase.GetDeviceFile(DeviceName);
		if not devFileName:
			self.__Logger.error("Can't load Device %s: not known!"%DeviceName);
		# load and init device
		try:
			device = Device.Device(self.__Core, devFileName, DeviceName, Parameters);
		except:
			self.__Logger.error("Error while load Device \"%s\""%DeviceName);
			return(False);
		if not device:
			self.__Logger.error("Error while load device %s"%DeviceName);
			return(None);

		#add device to table
		self.__DeviceHash.update( {Alias:device} );
		return(True);


	def UnLoadDevice(self, Alias):
		""" Unload and destroy the given device. Return True on success. """
		#get device from table
		device = self.__DeviceHash.get(Alias);
		if not device:
			self.__Logger.warning("No device found named %s"%Alias);
			return(False);
		#try to destroy
		if not device.destroy():
			self.__Logger.warning("Can't destroy device %s"%Alias);
			return(False);
		#remove from table
		del self.__DeviceHash[Alias];
		return(True);


	def ListDevices(self):
		""" List all loaded devices. Return a list of strings. """
		# simply return the keys of device table
		return(self.__DeviceHash.keys());

	def GetFQDeviceName(self, Alias):
		dev = self.__DeviceHash.get(Alias);
		if not dev:
			self.__Logger.error("No device named \"%s\" found."%Alias);
			return(None);
		return(dev.getClassAndName());
 
            
    
    # ######################################################################## #
    # Manage Server                                                            #
    # ######################################################################## #
    # ######################################################################## #
	def LoadServer(self, ServerName, Alias, DefaultUser, Parameters):
		""" Load the server ServerName as Alias with Parameters and with
 default rights of the given DefaultUser. Return True on success."""
		#check alias:
		if self.__ServerHash.has_key(Alias):
			self.__Logger.error("Alias %s already exists"%Alias);
			return(False);

		serverFileName = self.__DataBase.GetServerFile(ServerName);
		if not serverFileName:
			self.__Logger.warning("No server found named %s"%ServerName);
			return(False);
		try:
			server = Server.Server(self.__Core, serverFileName, ServerName, DefaultUser, Parameters);
		except:
			self.__Logger.warning("Error while load server %s"%ServerName);
			return(False);
		if not server:
			self.__Logger.error("Error while load Server %s"%ServerName);
			return(False);
		self.__ServerHash.update( {Alias:server} );
		return(True);

	def UnLoadServer(self, Name):
		""" Unload a desatroy the give Server. Return True on success."""
		# get Obj by name
		serverObj = self.__ServerHash.get(Name);
		if not serverObj:
			self.__Logger.warning("No server running named \"%s\""%Name);
			return(False);
		# stop it:
		if not serverObj.destroy():
			return(False);
		del self.__ServerHash[Name];
		return(True);

	def ListRunningServers(self):
		""" List all running or hanging servers. Return a list of strings. """
		# simply return a list of known aliases:
		return(self.__ServerHash.keys());
	def GetFQServerName(self, Alias):
		srv = self.__ServerHash.get(Alias);
		if not srv:
			self.__Logger.error("No server named \"%s\" found"%Alias);
			return(None);
		return(srv.getClassAndName());



    # ######################################################################## #
    # Manage SymbolTree                                                        #
    # ######################################################################## #
    # ######################################################################## #
	def CreateFolder(self, Path, Modus='600', Owner=None, Group=None):
		""" Create a new Folder in Folder "Path" with Modus, Owner, Group.
 Modus, Owner, Group can be obmitted, then the SuperUser and the 
 SuperUserGroup will be used for Owner and Group and 600 will be used as
 the modus. Return True on success."""
		# map call to core-object:
		if not self.__Core.SymbolTreeCreateFolder(Path):
			return(False);
		if Owner:
			if not self.ChangeOwner(Path,Owner):
				self.__Logger.warning("Error while set owner to %s"%Owner);
		if not Group:
			if Owner:
				Group = self.__UserDataBase.GetGroupByUserName(Owner);
				if not Group:
					self.__Logger.warning("Unknown owner %s"%Owner);
				self.ChangeGroup(Path, Group);
		if Modus != '600':
			self.ChangeModus(Path,Modus);
		return(True);

	def DeleteFolder(self, Path, Recur=False):
		""" Simply delete a (empty) Folder. Return True on success. """
		#simply map call to core:
		return(self.__Core.SymbolTreeDeleteFolder(Path));
		#FIXME Add recursive detete


	def ListFolders(self, Path):
		""" List all folder in Path. """
		# simply map call to core:
		return(self.__Core.SymbolTreeListFolders(Path));


	def CreateSymbol(self, Path, Slot, Type, Modus='600', Owner=None, Group=None):
		""" Create a Symbol with Type in Path and attach it to Slot. Modus, Owner, Group
 can be obmitted. Then SuperUser, SuperUserGroup and 600 will be used. Return True on
 success. """
		# check if symbol allready exists:
		# split slot:
		tmp = Slot.split('::');
		if len(tmp) < 2 or len(tmp) > 3:
			self.__Logger.error("Slot address format: DEVICE::NAMESPACE::ADDRESS");
			return(False);
		# get device name:
		DevName = tmp[0];
		# get namespace
		if len(tmp) == 2:
			NameSpace = None;
		else:
			NameSpace = tmp[1];
		# get address:
		Address = tmp[-1];
		
		# try to create slot:
		# get device
		dev = self.__DeviceHash.get(DevName);
		if not dev:
			self.__Logger.error("No device named \"%s\" found!"%DevName);
			return(False);
		# get slotid
		SlotID = dev.register(NameSpace, Address, Type);
		# create symbol in core object
		if not self.__Core.SymbolTreeCreateSymbol(Path, SlotID):
			self.__Logger.error("Can't create symbol \"%s\""%Path);
			# unregister symbol:
			dev.unregister(SlotID);
			return(False);

		# fin
		self.__SymbolTable.update( {Path:SlotID} );
		self.__SymbolDeviceTable.update( {Path:DevName} );
		# CHANGE ACCESS
		# set modus:
		if Modus != '600':
			if not self.ChangeModus(Path,Modus):
				self.__Logger.warning("Unable to change modus to %s"%Modus);
		if Owner:
			if not self.ChangeOwner(Path,Owner):
				self.__Logger.warning("Unable to change owner to %s"%Owner);
			if not Group:
				if not self.ChangeGroup(Path,self.__UserDataBase.GetGroupByUserName(Owner)):
					self.__Logger.warning("Unable to set Group");
		if Group:
			if not self.ChangeGroup(Path,Group):
				self.__Logger.warning("Unable to change group to %s"%Group);
		return(True);


	def DeleteSymbol(self, Path):
		""" Simply delete the symbol in Path. Return True on success."""
		# get slotID by symbol path:
		SlotID = self.__SymbolTable.get(Path);
		if not SlotID:
			self.__Logger.error("Unknown symbol \"%s\""%Path);
			return(False);
		# get deviceName by slotID
		DevName = self.__SymbolDeviceTable.get(Path);
		if not DevName:
			self.__Logger.fatal("no device enty for slotid in table! Mail author!");
			return(False);
		# get device object by name
		Dev = self.__DeviceHash.get(DevName);
		if not Dev:
			self.__Logger.fatal("no device object for name \"%s\" in table! Mail author!"%DevName);
			return(False);
		#delete symbol from tree
		if not self.__Core.SymbolTreeDeleteSymbol(Path):
			self.__Logger.error("Can't del symbol \"%s\""%Path);
			return(False);
		if not Dev.unregister(SlotID):
			self.__Logger.error("Can't unregister symbol from device");
			self.__Logger.debug("Restore symbol...");
			self.__Core.SymbolTreeCreateSymbol(Path, SlotID);
			return(False);
		del self.__SymbolTable[Path];
		#FIXME check if it is ness. to del some else...
		return(True);


	def ListSymbols(self, Path):
		""" List all Symbols in Path. Return a lsit of strings. """
		#simple map call to core:
		return(self.__Core.SymbolTreeListSymbols(Path));


	def GetModus(self, Path, Format=MODUS_FMT_OCTAL):
		""" Return the modus of a symbol or folder in Format.
 If Format is OCTAL, a string with the octal representation of the
 modus will be returnd. If Format is STRING, a string formated like
 the modus in ls -l command will be returned. If Format is INTEGER
 the integer representation of the modus will be returned (base=10!!!)."""
 
		(User, Group, Modus) = self.__Core.SymbolTreeGetAccess(Path);
		if Modus == None:
			self.__Logger.warning("Error while get modus of %s, maybe it does not exist"%Path);
			return(None);
		if Format==MODUS_FMT_OCTAL:
			return(ModusToOctString(Modus));
		if Format==MODUS_FMT_STRING:
			return(ModusToString(Modus));
		if Format==MODUS_FMT_INTEGER:
			return(Modus);
		self.__Logger.warning("Invalid format...");
		return(None);


	def ChangeModus(self, Path, Modus):
		""" Change the modus of the symbol or folder pointed by path.
 Only the OCTAL string format is accepted. Return True on success. """
		(user, group, old_modus) = self.__Core.SymbolTreeGetAccess(Path);
		if isinstance(Modus,int):
			new_modus = Modus;
		elif isinstance(Modus,str):
			try:
				new_modus = int(Modus,8);
			except:
				self.__Logger.warning("Invalid vormat");
				return(None);
		return(self.__Core.SymbolTreeSetAccess(Path,user,group,new_modus));

	def GetOwner(self, Path):
		""" Return the owner name. """
		(user, group, modus) = self.__Core.SymbolTreeGetAccess(Path);
		return(user);

	def ChangeOwner(self, Path, Owner):
		""" Set the owner of a symbol or folder. Return True
 on success. """
		(old_user, group, modus) = self.__Core.SymbolTreeGetAccess(Path);
		return(self.__Core.SymbolTreeSetAccess(Path, Owner, group, modus));


	def GetGroup(self, Path):
		""" Return the groupname of a symbol or folder."""
		(owner, group, modus) = self.__Core.SymbolTreeGetAccess(Path);
		return(group);


	def ChangeGroup(self, Path, Group):
		""" Set the group of a symbol or folder. Return True on success."""
		(owner, old_group, modus) = self.__Core.SymbolTreeGetAccess(Path);
		return(self.__Core.SymbolTreeSetAccess(Path, owner, Group, modus));


	def GetValue(self, Path):
		""" Return the actual value of the symbol pointed by Path. """
		return(self.__Core.SymbolTreeGetValue(Path));


	def SetValue(self, Path, Value):
		""" Set the Value of a symbol pointed by path. """
		return(self.__Core.SymbolTreeSetValue(Path, Value));





#
# Usefull functions
#
def ModusToOctString(modus):
	any = modus & 0x07;
	grp = (modus>>3) &0x07;
	own = (modus>>6) &0x07;
	return("%i%i%i"%(own,grp,any));
	
def ModusToString(modus):
	any = modus & 0x07;
	grp = (modus>>3) & 0x07;
	own = (modus>>6) & 0x07;
	rstr= "";
	tmp = "";
	for mod in (own,grp,any):
		if mod & 0x01:
			tmp += "r";
		else:
			tmp += "-";
		if (mod>>1)&0x01:
			tmp += "w";
		else:
			tmp += "-";
		if (mod>>2)&0x01:
			tmp += "x";
		else:
			tmp += "-";
		rstr += tmp;
		tmp = "";
	return(rstr);
