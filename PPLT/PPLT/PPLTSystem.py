import pyDCPU;
import Configuration;
import Logging;
import AliasTable;
import Install;
import Device;
import Server;
import DataBase;


MODUS_FMT_OCTAL = 1;
MODUS_FMT_STRING = 2;
MODGRP_MASTER = 'Master';
MODGRP_SERVER = 'Server';
MODGRP_DEVICE = 'Device';

class System:
	def __init__(self):
		""" This is the PPLTSystem class all work can be don over a instanc if this class """
		self.__Config = Configuration.Config();								# Load Config

		self.__Core = pyDCPU.Core(UserDBFile = self.__Config.GetUserDB(),	# Start Core
                                  LogLevel = self.__Config.GetLogLevel(),
                                  LogFile = self.__Config.GetLogFile(),
                                  SysLog = self.__Config.GetSysLog());

		self.__Logger = Logging.Logger();									# Start Logging

		self.__DataBase = DataBase.DataBase(self.__Config.GetDBPath());	# Load the Module/Device 
        
		self.__DeviceHash = {}												# init some tables
		self.__ServerHash = {}												# ...
		self.__SymbolTable = {};											# ...
		self.__SlotDeviceTable = {};										# ...

    
    # ######################################################################## #
    # Module/Device handling                                                   #
    # ######################################################################## #
    # - install                                                                #
    # - uninstall                                                              #
    # ######################################################################## #
	def Install(self, InstallFile):
		""" This method will install all core-modules and pplt-devices listed in
the InstallFile. """
		pass;
    
	def UnIstall(self, ModuleName):
		""" This method will uninstall the given module/divice """
		pass;

	def ListKnownModules(self, ModGroup):
		pass;

	def GetModuleInfo(self, Name):
		""" Return a info object... """
        #return(self.__ModuleDB.Info(Name));
		pass;
    
    
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
		#FIXME Add chown
		#FIXME Add chgrp
		#FIXME Add chmod


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
			self.__Logger.error("Slot address format: DEVICE::NAMESPACE::ADDRESS\n Namespace is optional if device only have one.");
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
		return(Ture);


	def ListSymbols(self, Path):
		#simple map call to core:
		return(self.__Core.SymbolTreeListSymbols(Path));


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
		return(self.__Core.SymbolTreeGetValue(Path));


	def SetValue(self, Path, Value):
		return(self.__Core.SymbolTreeSetValue(Path, Value));
