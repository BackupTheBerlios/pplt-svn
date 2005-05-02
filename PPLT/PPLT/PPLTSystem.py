import pyDCPU;
import Configuration;
import Logging;
import Install;
import Device;
import Server;
import DataBase;


MODUS_FMT_OCTAL = 1;
MODUS_FMT_STRING = 2;
MODUS_FMT_INTEGER = 3;


class System:
	def __init__(self):
		""" This is the PPLTSystem class all work can be don over a instanc if this class """
		self.__Config = Configuration.Config();								# Load Config

		self.__Core = pyDCPU.Core(UserDBFile = self.__Config.GetUserDB(),	# Start Core
                                  LogLevel = self.__Config.GetLogLevel(),
                                  LogFile = self.__Config.GetLogFile(),
                                  SysLog = self.__Config.GetSysLog());

		self.__Logger = Logging.Logger();									# Start Logging

		self.__DataBase = DataBase.DataBase(self.__Config.GetDBPath());		# Load the Module/Device database
		self.__UserDataBase = self.__Core.GetTheUserDB();
		self.__DeviceHash = {}												# init some tables
		self.__ServerHash = {}												# ...
		self.__SymbolTable = {};											# ...
		self.__SlotDeviceTable = {};										# ...


	def Stop(self):
		""" This methow will stop the system. Meaning stopping all servers,
 clear the whole Symboltree ans unload all devices. """ 
		pass;


    # ######################################################################## #
    # Module/Device handling                                                   #
    # ######################################################################## #
    # - install                                                                #
    # - uninstall                                                              #
    # ######################################################################## #
	def Install(self, InstallFile):
		""" This method will install all core-modules and pplt-devices listed in
 the InstallFile. """
		return(Install.InstallSet(InstallFile, self.__Config.GetBasePath()));
    
	def UnIstall(self, ModuleName):
		""" This method will uninstall the given module/divice/server """
		#FIXME implement!
		pass;

	def ListKnownServers(self, Class=None):
		return(self.__DataBase.ListServersIn(Class));
	def ListKnownServerClasses(self, Class=None):
		return(self.__DataBase.ListServerClassesIn(Class));
	def ListKnownDevices(self, Class=None):
		return(self.__DataBase.ListDevicesIn(Class));
	def ListKnownDeviceClasses(self, Class=None):
		return(self.__DataBase.ListDeviceClassesIn(Class));
	def GetServerInfo(self, Name):
		""" Return a info object """
		pass;
	def GetDeviceInfo(self, Name):
		#FIXME implement!
		pass;
    
    # ######################################################################## #
    # User/Group management                                                    #
    # ######################################################################## #
    # ######################################################################## #
	def CreateGroup(self, ParentGroup, Name):
		return(self.__UserDataBase.CreateGroup(ParentGroup,Name));

	def DeleteGroup(self, Name):
		return(self.__UserDataBase.DeleteGroup(Name));

	def ListGroups(self, GroupName = None):
		if not GroupName:
			group = self.__UserDataBase;
		else:
			group = self.__UserDataBase.GetGroupByName(GroupName);
		if not group:
			return(None);
		# list subgroups:
		return(group.ListSubGroups());

	def ListMembers(self, GroupName = None):
		if not GroupName:
			return([]);
		group = self.__UserDataBase.GetGroupByName(GroupName);
		if not group:
			return(None);
		#list memebers:
		return(group.ListMembers());

	def CreateMember(self, Group, Name, Password, Description):
		return(self.__UserDataBase.CreateMember(Group, Name, Password, Description));

	def DeleteMember(self, Name):
		group = self.__UserDataBase.GetGroupByUserName(Name);
		if not group:
			self.__Logger.warning("No group found for user %s: does he/she exists?"%Name);
			return(False);
		return(self.__UserDataBase.DeleteMember(group, Name));

	def CheckPassword(self, Name, Password):
		return(self.__UserDataBase.ValidUser(Name,Password));

	def ChangePassword(self, Name, Password):
		return(self.__UserDataBase.ChangePassword(Name,Password));

	def SetSuperUser(self, Name):
		return(self.__UserDataBase.SetSuperUser(Name));

	def GetSuperUser(self):
		return(self.__UserDataBase.GetSuperUser());
        
        
    
    # ######################################################################## #
    # Manage Devices                                                           #
    # ######################################################################## #
    # ######################################################################## #
	def LoadDevice(self, DeviceName, Alias, Parameters):
		""" Return a device object """
		# try to find out file name of DeviceName
		devFileName = self.__DataBase.GetDeviceFile(DeviceName);
		if not devFileName:
			self.__Logger.error("Can't load Device %s: not known!"%DeviceName);
		# load and init device
		try:
			device = Device.Device(self.__Core, devFileName, Parameters);
		except:
			self.__Logger.error("Error while load Device \"%s\""%DeviceName);
			return(False);
		
		#add device to table
		self.__DeviceHash.update( {Alias:device} );
		return(True);


	def UnLoadDevice(self, Alias):
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
		# simply return the keys of device table
		return(self.__DeviceHash.keys());
    
            
    
    # ######################################################################## #
    # Manage Server                                                            #
    # ######################################################################## #
    # ######################################################################## #
	def LoadServer(self, ServerName, Alias, DefaultUser, Parameters):
		serverFileName = self.__DataBase.GetServerFile(ServerName);
		if not serverFileName:
			self.__Logger.warning("No server found named %s"%ServerName);
			return(False);
		try:
			server = Server.Server(self.__Core, serverFileName, DefaultUser, Parameters);
		except:
			self.__Logger.warning("Error while load server %s"%ServerName);
			return(False);
		self.__ServerHash.update( {Alias:server} );
		return(True);

	def UnLoadServer(self, Name):
		# get Obj by name
		serverObj = self.__ServerHash.get(Name);
		if not serverObj:
			self.__Logger.warning("No server running named \"%s\""%Name);
			return(False);
		# stop it:
		return(serverObj.destroy());

	def ListRunningServers(self):
		# simply return a list of known aliases:
		return(self.__ServerHash.keys());
        


    # ######################################################################## #
    # Manage SymbolTree                                                        #
    # ######################################################################## #
    # ######################################################################## #
	def CreateFolder(self, Path, Modus='600', Owner=None, Group=None):
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
		#simply map call to core:
		return(self.__Core.SymbolTreeDeleteFolder(Path));
		#FIXME Add recursive detete


	def ListFolders(self, Path):
		# simply map call to core:
		return(self.__Core.SymbolTreeListFolders(Path));


	def CreateSymbol(self, Path, Slot, Type, Modus='600', Owner=None, Group=None):
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
		self.__SlotDeviceTable.update( {SlotID:DevName} );
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
		# get slotID by symbol path:
		SlotID = self.__SymbolTable.get(Path);
		if not SlotID:
			self.__Logger.error("Unknown symbol \"%s\""%Path);
			return(False);
		# get deviceName by slotID
		DevName = self.__SlotDeviceTable.get(SlotID);
		if not DevName:
			self.__Logger.fatal("no device enty for slotid in table! Main author!");
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
		#simple map call to core:
		return(self.__Core.SymbolTreeListSymbols(Path));


	def GetModus(self, Path, Format=MODUS_FMT_OCTAL):
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
		(user, group, old_modus) = self.__Core.GetAccess(Path);
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
		(user, group, modus) = self.__Core.SymbolTreeGetAccess(Path);
		return(user);

	def ChangeOwner(self, Path, Owner):
		(old_user, group, modus) = self.__Core.SymbolTreeGetAccess(Path);
		return(self.__Core.SymbolTreeSetAccess(Owner, group, modus));


	def GetGroup(self, Path):
		(owner, group, modus) = self.__Core.SymbolTreeGetAccess(Path);
		return(group);


	def ChangeGroup(self, Path, Group):
		(owner, old_group, modus) = self.__Core.SymbolTreeGetAccess(Path);
		return(self.__Core.SymbolTreeSetAccess(Path, owner, Group, modus));


	def GetValue(self, Path):
		return(self.__Core.SymbolTreeGetValue(Path));


	def SetValue(self, Path, Value):
		return(self.__Core.SymbolTreeSetValue(Path, Value));





#
# Usefull functions
#
def ModusToOctString(modus):
	any = modus & 0x07;
	grp = (modus>>3) &0x07;
	own = (modus>>6) &0x07;
	return("%i%i%i"%(any,grp,own));
	
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
