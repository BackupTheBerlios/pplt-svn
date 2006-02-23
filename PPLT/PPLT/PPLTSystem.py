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

import pyDCPU;
import pyDCPU.SymbolTools
import Logging;
import Device;
import Server;
import DataBase;
import LoadSession;
import NameCheck;
from xml.dom.minidom import getDOMImplementation
import string;
import os.path;
import sys;

MODUS_FMT_OCTAL = 1;
MODUS_FMT_STRING = 2;
MODUS_FMT_INTEGER = 3;


class System:
    """This is the PPLTSystem class all work can be done over a instance if this 
 class. To get a instance of this class simply call:
 >>> obj = PPLT.System(). 
 
 A typical session could be:
 >>> import PPLT
 >>> #Start the pplt-system:
 >>> system = PPLT.System()
 >>> 
 >>> #Load device RandomGenerator:
 >>> # The first parameter is the full-qualified devicename, the next parameter is the
 >>> # alias you give to the loaded device to identify it later (to create symbols).
 >>> # The last parameter is a dict with all parameters for the device (RandomGenerator 
 >>> # needs no parameters)
 >>> system.LoadDevice("Debug.RandomGenerator", "rand", {})
 >>>
 >>> #Create a symbol:
 >>> # The first parameter is the full path to the sysmbol you want to create.
 >>> # NOTE: All folders on the path to the symbol must exsists.
 >>> # The second parameter is the full name of the symbol-slot the symbol will be
 >>> # attached to. The format for the symbol-slot name is ALIAS::NAMESPACE::SLOT.
 >>> system.CreateSymbol("/r_bool", "rand::Generator::Bool")
 >>> 
 >>> #Now start a server:
 >>> # The call of LoadServer is quied simular to the call of LoadDevice, but
 >>> # the additional 3rd parameter gives the default user. The server will run
 >>> # with this rights if it's protocol knows no authentication.
 >>> system.LoadServer("Web.PPLTWebServer", "web", "", {"Address":"127.0.0.1", "Port":"8080"})"""

    def __init__(self, BasePath=None, CoreLogLevel="info", PPLTLogLevel="info", LogFile=None, SysLog=None,
                 Lang="en", AltLang="en"):
        if not BasePath: BasePath = os.path.normpath(sys.exec_prefix+"/PPLT/");

        CoreModPath = os.path.normpath(BasePath+"/CoreMods/");
        PPLTModPath = os.path.normpath(BasePath+"/PPLTMods/");
        PPLTUserDB  = os.path.normpath(BasePath+"/UserDB.xml");
        CoreLL = CoreLogLevel;
        PPLTLL = PPLTLogLevel;

        self.__Core = pyDCPU.Core(ModulePath = CoreModPath,
                                  UserDBFile = PPLTUserDB,   # Start Core
                                  LogLevel = CoreLL,
                                  LogFile = LogFile,
                                  SysLog = SysLog);

        self.__Logger = Logging.Logger( PPLTLL,
                                        LogFile,
                                        SysLog);         # Start Logging

        self.__DataBase = DataBase.DataBase(CoreModPath,
                                            PPLTModPath,
                                            Lang,
                                            AltLang);        # Load the Module/Device database

        self.__UserDataBase = self.__Core.GetTheUserDB();
        self.__DeviceHash = {}                                                  # init some tables
        self.__ServerHash = {}                                                  # ...
        # Association between SymbolPath and Slot
        # mainly used to save the symbol-tree into a session file
        self.__SymbolTable = {};



    # ######################################################################## #
    # Stopping the whole system                                                #
    # ######################################################################## #
    # - stop all                                                               #
    # - stop servers                                                           #
    # - stop devices                                                           #
    # - clear symboltree                                                       #
    # ######################################################################## #
    def StopAll(self):
        """ This method will stop the system. Meaning stopping all servers,
 clear the whole Symboltree and unload all devices. (no parameters needed)""" 
        self.StopServers();
        self.ClearSymbolTree();
        self.StopDevices();
    
    def StopServers(self):
        """ This method will stop all servers. """
        srvlst = self.__ServerHash.keys();
        for srv in srvlst:
            self.__Logger.debug("Try to stop server \"%s\"."%srv);
            self.UnLoadServer(srv)

    def StopDevices(self):
        """ This method will unload all devices. """
        devlst = self.__DeviceHash.keys();
        for dev in devlst:
            self.__Logger.debug("Try to unload device \"%s\"."%dev);
            self.UnLoadDevice(dev);

    def ClearSymbolTree(self, path="/"):
        """ This method will clear the whole symbol tree or the path if given. """
        # delete all symbols in this folder:
        symlst = self.ListSymbols(path);
        for sym in symlst:
            if path[-1] == '/': sym = path+sym;
            else: sym = path+"/"+sym;
            self.DeleteSymbol(sym);

        #recursive delete all folders in this path:
        dirlst = self.ListFolders(path);
        for fol in dirlst:
            if path[-1] == '/': fol = path+fol;
            else: fol = path+"/"+fol;
            self.ClearSymbolTree(fol);
            self.DeleteFolder(fol);



    # ######################################################################## #
    # Project/Session-management                                               #
    # ######################################################################## #
    # - save                                                                   #
    # - load (have to be implemented)                                          #
    # ######################################################################## #
    def SaveSession(self, FileName):
        """ Save the running system as a session description file. """
        impl = getDOMImplementation();
        doc = impl.createDocument(None, "PPLTSession", None);
        top = doc.documentElement;

        fd = open(FileName, "w");

        #save servers:
        servers_tag = doc.createElement("Servers");
        top.appendChild(servers_tag);
        self.__SaveServers(doc, servers_tag);

        #save devices:
        devices_tag = doc.createElement("Devices");
        top.appendChild(devices_tag);
        self.__SaveDevices(doc, devices_tag);

        #save symboltree:
        symtree_tag = doc.createElement("SymbolTree");
        top.appendChild(symtree_tag);
        self.__SaveSymTree(doc, symtree_tag);

        #save to file:  
        txt = doc.toprettyxml()
        fd.write(txt);
        fd.close();

    def __SaveServers(self, Doc, Node):
        srvlst = self.__ServerHash.keys();
        for srv in srvlst:
            srv_obj = self.__ServerHash.get(srv);
            
            srv_tag = Doc.createElement("Server");
            Node.appendChild(srv_tag);

            srv_tag.setAttribute("alias",srv);
            srv_tag.setAttribute("fqsn",srv_obj.getClassAndName());
            srv_tag.setAttribute("user",srv_obj.getDefaultUser());
            srv_tag.setAttribute("root",srv_obj.getRoot());

            # append paramters:
            parmtr = srv_obj.getParameters();
            for par in parmtr.keys():
                prm_tag = Doc.createElement("Parameter");
                srv_tag.appendChild(prm_tag);
                prm_tag.setAttribute("name",par);
                val_tag = Doc.createTextNode(parmtr.get(par));
                prm_tag.appendChild(val_tag);
                
    def __SaveDevices(self, Doc, Node):
        devlst = self.__DeviceHash.keys();
        for dev in devlst:
            dev_obj = self.__DeviceHash.get(dev);
            
            dev_tag = Doc.createElement("Device");
            Node.appendChild(dev_tag);

            dev_tag.setAttribute("alias",dev);
            dev_tag.setAttribute("fqdn",dev_obj.getClassAndName());
            # append paramters:
            parmtr = dev_obj.getParameters();
            for par in parmtr.keys():
                prm_tag = Doc.createElement("Parameter");
                dev_tag.appendChild(prm_tag);
                prm_tag.setAttribute("name",par);
                val_tag = Doc.createTextNode(parmtr.get(par));
                prm_tag.appendChild(val_tag);
    
    def __SaveSymTree(self, Doc, Node, Path="/"):
        symlst = self.ListSymbols(Path);
        for sym in symlst:
            if Path[-1] == "/": sympath = Path+sym;
            else: sympath = Path+"/"+sym;
            Slot = self.__SymbolTable[sympath];
            sym_tag = Doc.createElement("Symbol");
            Node.appendChild(sym_tag);
            sym_tag.setAttribute("name",sym);
            sym_tag.setAttribute("slot",Slot);
            sym_tag.setAttribute("refresh",self.__Core.SymbolTreeGetRefresh(sympath))
            sym_tag.setAttribute("owner", self.GetOwner(sympath));
            sym_tag.setAttribute("group", self.GetGroup(sympath));
            sym_tag.setAttribute("modus", self.GetModus(sympath,MODUS_FMT_OCTAL));
            self.__Logger.debug("Sessionsave: Save symbol %s(%s) with slot %s, refresh %s, owner %s, group %s and modus %s"%(
                                sym, sympath, Slot, self.__Core.SymbolTreeGetRefresh(sympath), self.GetOwner(sympath),
                                self.GetGroup(sympath), self.GetModus(sympath, MODUS_FMT_OCTAL)));

        dirlst = self.ListFolders(Path);
        for fol in dirlst:
            if Path[-1]=="/": folpath = Path+fol;
            else: folpath = Path+"/"+fol;
            fol_tag = Doc.createElement("Folder");
            Node.appendChild(fol_tag);
            fol_tag.setAttribute("name",fol);
            fol_tag.setAttribute("owner",self.GetOwner(folpath));
            fol_tag.setAttribute("group",self.GetGroup(folpath));
            fol_tag.setAttribute("modus",self.GetModus(folpath,MODUS_FMT_OCTAL));
            self.__SaveSymTree(Doc, fol_tag, folpath);



    def LoadSession(self, FileName):
        """ Load session description file and setup the project. """
        return(LoadSession.LoadSession(self, FileName));





    # ######################################################################## #
    # Module/Device handling (DataBase)                                        #
    # ######################################################################## #
    # - install                                                                #
    # - uninstall                                                              #
    # ######################################################################## #
    def ListKnownServers(self, Class=None):
        """ List all Servers in Class. Return a list of strings. """
        return(self.__DataBase.ListServers(Class));

    def ListKnownServerClasses(self, Class=None):
        """ List all server classes in give class. if class is missed, all
 root-classes will be listed. Return a list of strings. """
        return(self.__DataBase.ListServerClasses(Class));

    def ListKnownDevices(self, Class=None):
        """ List all devices in class. Return a list of strings. """
        return(self.__DataBase.ListDevices(Class));

    def ListKnownDeviceClasses(self, Class=None):
        """ List all device classes. like "ListKnownServerClasses()". 
Return a list of strings. """
        return(self.__DataBase.ListDeviceClasses(Class));
    
    def GetServerVersion(self, Name):
        """Return the Version of the given server (if found)"""
        return(self.__DataBase.GetServerVersion(Name));

    def GetServerInfo(self, Name):
        """ Return a info object for the server Name. """
        return(self.__DataBase.GetServerInfo(Name));

    def GetDeviceVersion(self, Name):
        """ Return the version of the device (if found)"""
        return(self.__DataBase.GetDeviceVersion(Name));

    def GetDeviceInfo(self, Name):
        """ Return a info object for the device Name. """
        return(self.__DataBase.GetDeviceInfo(Name));



    # ######################################################################## #
    # User/Group management                                                    #
    # ######################################################################## #
    # ######################################################################## #
    def CreateGroup(self, ParentGroup, Name):
        """ Create a group within ParentGroup with Name. If ParentGroup is None,
 a new root group will be generated. """ 
        NameCheck.CheckGroup(Name);
        self.__UserDataBase.CreateGroup(ParentGroup,Name);

    def DeleteGroup(self, Name):
        """ Delete a group."""
        self.__UserDataBase.DeleteGroup(Name);

    def ListGroups(self, GroupName = None):
        """ List all subgroups of given GroupName. If GroupName = None or 
 missed, all root groups will be listed. Return a list of string. """

        if not GroupName: group = self.__UserDataBase;
        else: group = self.__UserDataBase.GetGroupByName(GroupName);
        if not group: return([]);
        # list subgroups:
        return(group.ListSubGroups());

    def ListMembers(self, GroupName = None):
        """ List all members of a give group. Return a list of strings. """
        if not GroupName: return([]);
        group = self.__UserDataBase.GetGroupByName(GroupName);
        if not group: return([]);
        #list memebers:
        return(group.ListMembers());

    def CreateMember(self, Group, Name, Password, Description):
        """ Create a new group member for the give Group with Name, Password 
 and Description. """
        NameCheck.CheckUser(Name);
        self.__UserDataBase.CreateMember(Group, Name, Password, Description, Encode=True);

    def DeleteMember(self, Name):
        """ Delete a user. """
        group = self.__UserDataBase.GetGroupByUserName(Name);
        if not group: raise pyDCPU.ItemNotFound("No group found %s is member of! Does he/she exists?"%Name);
        self.__UserDataBase.DeleteMember(group.GetName(), Name);

    def CreateProxy(self, Group, Name):
        """ Create a user-proxy for user (Name) in group (Group). """
        self.__UserDataBase.CreateProxy(Group, Name);

    def ListProxys(self, Group):
        """List all proxys in group (Group). """
        group = self.__UserDataBase.GetGroupByName(Group);
        if not group: raise pyDCPU.ItemNotFound("Group \"%s\" not found."%Group);
        self.__Logger.debug("List proxys of group %s"%group.GetName());
        return(group.ListProxys());

    def DeleteProxy(self, Group, User):
        """ Delete proxy for user (User) in group (Group) """
        self.__UserDataBase.DeleteProxy(Group, User);

    def CheckPassword(self, Name, Password):
        """ Test Password if its match to user Name's one. """
        return(self.__UserDataBase.ValidUser(Name,Password));

    def ChangePassword(self, Name, Password):
        """ Change the passwd for a the user Name. """
        self.__UserDataBase.ChangePassword(Name,Password,Encode=True);

    def SetSuperUser(self, Name):
        """ Make user Name become the SuperUser. """
        self.__UserDataBase.SetSuperUser(Name);

    def GetSuperUser(self):
        """ Return the name of the SuperUser """
        return self.__UserDataBase.GetSuperUser();

    def GetSuperUserGrp(self):
        """ Return the group of the SuperUser """
        return(self.__UserDataBase.GetSuperUserGrp());

    def GetGroupByUser(self, UserName):
        """ Return the group of given user """
        grp = self.__UserDataBase.GetGroupByUserName(UserName);
        if not grp: raise pyDCPU.ItemNotFound("User \"%s\" not found!"%UserName);
        return(grp.GetName());
    


    # ######################################################################## #
    # Manage Devices                                                           #
    # ######################################################################## #
    # ######################################################################## #
    def LoadDevice(self, DeviceName, Alias, Parameters):
        """ Load and init device DeviceName as Alias with Parameters."""
        #check Alias:
        NameCheck.CheckAlias(Alias);

        #check alias:
        if self.__DeviceHash.has_key(Alias):
            raise pyDCPU.Exceptions.ItemBusy("Alias \"%s\" already used."%Alias);

        # try to find out file name of DeviceName
        devFileName = self.__DataBase.GetDevicePath(DeviceName);
        if not devFileName:
            raise pyDCPU.Exceptions.ItemNotFound("Can't load device \"%s\": Associated file [%s] not found!"%(DeviceName, devFileName));

        # extend parameters with default values:

        # load and init device
        device = Device.Device(self.__Core, devFileName, DeviceName, Parameters);

        if not device: raise pyDCPU.Exceptions.Error("At first this should not happened! And the device can't be loaded!");

        #add device to table
        self.__DeviceHash.update( {Alias:device} );
        return(True);


    def UnLoadDevice(self, Alias):
        """ Unload and destroy the given device. """
        if not self.__DeviceHash.has_key(Alias):
            raise pyDCPU.Exceptions.ItemNotFound("No device with alias \"%s\" known!"%Alias);
       
        #check if device is used by symbols:
        for slot in self.__SymbolTable.values():
            (device, namespace, addr) = slot.split("::",3);
            if device == Alias:
                raise pyDCPU.ItemBusy("The device \"%s\" is used by (some) symbol(s)."%Alias);

        self.__DeviceHash[Alias].destroy();
        del self.__DeviceHash[Alias];


    def ListDevices(self):
        """ List all loaded devices. Return a list of strings. """
        # simply return the keys of device table
        return(self.__DeviceHash.keys());

    def GetFQDeviceName(self, Alias):
        """Return the full qualified device name of device known as Alias."""
        dev = self.__DeviceHash.get(Alias);
        if not dev: raise pyDCPU.ItemNotFound("No device named \"%s\" found."%Alias);
        return(dev.getClassAndName());

    def GetDeviceParameters(self, Alias):
        """ Return all Parameters of device known as.""" 
        dev = self.__DeviceHash.get(Alias);
        if not dev: raise pyDCPU.ItemNotFound("No device named \"%s\" found."%Alias);
        return(dev.getParameters());
            
    
    # ######################################################################## #
    # Manage Server                                                            #
    # ######################################################################## #
    # ######################################################################## #
    def LoadServer(self, ServerName, Alias, DefaultUser, Parameters, Root = "/"):
        """ Load the server ServerName as Alias with Parameters and with
 default rights of the given DefaultUser."""
        #check server-root:
        NameCheck.CheckPath(Root);

        #check alias:
        NameCheck.CheckAlias(Alias);

        #check servername:
        NameCheck.CheckServer(ServerName);

        #check alias:
        if self.__ServerHash.has_key(Alias):
            raise pyDCPU.ItemBusy("Alias \"%s\" allready used by an other device (or server)."%Alias);

        serverFileName = self.__DataBase.GetServerPath(ServerName);

        self.__Logger.debug("Try to load server %s with %s as %s"%(ServerName, str(Parameters), Alias));
        server = Server.Server(self.__Core, serverFileName, ServerName, DefaultUser, Parameters, Root);
        self.__ServerHash.update( {Alias:server} );


    def UnLoadServer(self, Name):
        """ Unload a desatroy the give Server."""
        # get Obj by name
        serverObj = self.__ServerHash.get(Name);
        if not serverObj:
            raise pyDCPU.ItemNotFound("No server runing named \"%s\"."%Name);
        # stop it:
        serverObj.destroy();
        del self.__ServerHash[Name];

    def ListRunningServers(self):
        """ List all running or hanging servers. """
        # simply return a list of known aliases:
        return(self.__ServerHash.keys());

    def GetFQServerName(self, Alias):
        """ This method returns the full qualified servername for the given
alias of a loaded server."""
        srv = self.__ServerHash.get(Alias);
        if not srv:
            raise pyDCPU.ItemNotFound("No server named \"%s\" found!"%Alias);
        return(srv.getClassAndName());

    def GetServerParameters(self, Alias):
        """ Return all parameters of the given server in a dict. """
        srv = self.__ServerHash.get(Alias);
        if not srv:
            raise pyDCPU.ItemNotFound("No server named \"%s\" found."%Alias);
        return(srv.getParameters());

    def GetServerDefaultUser(self, Alias):
        """ Return the name of the default user the server useses if it
doesn't know a authentification."""
        srv = self.__ServerHash.get(Alias);
        if not srv:
            raise pyDCPU.ItemNotFound("No server named \"%s\" found."%Alias);
        return(srv.getDefaultUser());

    def GetServerRoot(self, Alias):
        """ Return the server-root of a server. """
        srv = self.__ServerHash.get(Alias);
        if not srv:
            raise pyDCPU.ItemNotFound("No server named \"%s\" found."%Alias);
        return(srv.getRoot());
    

    # ######################################################################## #
    # Manage SymbolTree                                                        #
    # ######################################################################## #
    # ######################################################################## #
    def CreateFolder(self, Path, Modus='600', Owner=None, Group=None):
        """ Create a new Folder in Folder "Path" with Modus, Owner, Group.
 Modus, Owner, Group can be obmitted, then the SuperUser and the 
 SuperUserGroup will be used for Owner and Group and 600 will be used as
 the modus."""
        #check path:
        NameCheck.CheckPath(Path);

        # map call to core-object:
        self.__Core.SymbolTreeCreateFolder(Path);
        try:
            #try to set owner, group, modus 
            #if somethig goes wrong -> remove folder
            if Owner: self.ChangeOwner(Path,Owner);
            if not Group:
                if Owner:
                    Group = self.__UserDataBase.GetGroupByUserName(Owner);
                    self.ChangeGroup(Path, Group);
            if Modus != '600': self.ChangeModus(Path,Modus);
        except Exception,e:
            self.__Core.SymbolTreeDeleteFolder(Path);
            raise e;


    def MoveFolder(self, From, To):
        """ Move a folder from (From) to (To). """
        To = pyDCPU.SymbolTools.NormPath(To);
        From  = pyDCPU.SymbolTools.NormPath(From);
        self.__Logger.debug("Move Folder from %s to %s"%(From, To));

        NameCheck.CheckPath(To);
        
        if not self.__Core.SymbolTreeCheckPath(From):
            raise pyDCPU.ItemNotFound("Source-folder %s doesn't exists."%From);
        if self.__Core.SymbolTreeCheckPath(To):
            raise pyDCPU.ItemBusy("Destination folder allready exists");

        # get pathes of all symbols under folder (From):
        OSymList = RecursiveSymbolList(self, From);

        #map call to core object:
        self.__Core.SymbolTreeMoveFolder(From, To);

        # get pathes of all symbol under (new) folder (To) 
        #   (are in the sameorder):
        NSymList = RecursiveSymbolList(self, To);

        if len(OSymList) != len(NSymList):
            raise Exception("FATAL-ERROR: while move folder; Symbols lost! Mail author!");

        for Idx in range(len(OSymList)):
            From = OSymList[Idx];
            To   = NSymList[Idx];

            #update symbol<->slot table:
            slot = self.__SymbolTable.get(From);
            del self.__SymbolTable[From];
            self.__SymbolTable.update( {To:slot} );


    def DeleteFolder(self, Path, Recur=False):
        """ Simply delete a (empty) Folder. """
        return(self.__Core.SymbolTreeDeleteFolder(Path));


    def ListFolders(self, Path):
        """ List all folder in Path. """
        # simply map call to core:
        return(self.__Core.SymbolTreeListFolders(Path));


    def CreateSymbol(self, Path, Slot, Refresh=0.5, Modus='600', Owner=None, Group=None):
        """ Create a Symbol with Type in Path and attach it to Slot. Modus, Owner, Group
 can be obmitted. Then SuperUser, SuperUserGroup and 600 will be used. """
        # check slot-path:
        NameCheck.CheckPath(Path);

        # check slot:
        NameCheck.CheckSlot(Slot);

        # check if symbol allready exists:
        # split slot:
        tmp = Slot.split('::');

        # get device name:
        DevName = tmp[0];
        # get namespace
        NameSpace = tmp[1];
        # get address:
        Address = tmp[2];
        
        # try to create slot:
        # get device
        dev = self.__DeviceHash.get(DevName);
        if not dev: pyDCPU.ItemNotFound("No device named \"%s\" found!"%DevName);

        # get CoreModID by Namespace:
        ID = dev.GetIDByNameSpace(NameSpace);
        
        # create symbol in core object
        self.__Core.SymbolTreeCreateSymbol(Path, ID, Address, Refresh);

        # save Symbol<->Slot
        self.__SymbolTable.update( {Path:Slot} );
        
        # CHANGE ACCESS
        # set modus:
        try:
            if Modus != '600': self.ChangeModus(Path,Modus);
            if Owner:
                self.ChangeOwner(Path,Owner);
                if not Group:
                    GrpObj = self.__UserDataBase.GetGroupByUserName(Owner);
                    if GrpObj: self.ChangeGroup(Path,GrpObj.GetName());
            if Group: self.ChangeGroup(Path,Group);
        except Exception,e:
            self.DeleteSymbol(Path);
            raise e;

    def MoveSymbol(self, From, To):
        """Move a symbol from (From) to (To). Please use only full pathes."""
        To = pyDCPU.SymbolTools.NormPath(To);
        From = pyDCPU.SymbolTools.NormPath(From)
        NameCheck.CheckPath(To);

        self.__Core.SymbolTreeMoveSymbol(From,To);

        #update symbol<->slot table:
        slot = self.__SymbolTable.get(From);
        del self.__SymbolTable[From];
        self.__SymbolTable.update( {To:slot} );
        return(True);


    def DeleteSymbol(self, Path):
        """ Simply delete the symbol in Path."""
        # get slotID by symbol path:
        if not self.__SymbolTable.has_key(Path):
            raise pyDCPU.ItemNotFound("Unknwn symbol \"%s\""%Path);
        #delete symbol from tree
        self.__Core.SymbolTreeDeleteSymbol(Path);
        del self.__SymbolTable[Path];

    def SetSymbolRefresh(self, Path, Rate=0.5):
        """ (Re)Sets the refresh-rate of the given symbol to %%Timeout%%."""
        self.__Core.SymbolTreeSetRefresh(Path, Rate);
    
    def GetSymbolRefresh(self, Path):
        """ Returns the refresh-rate for the given symbol. """
        return self.__Core.SymbolTreeGetRefresh(Path);

    def GetSymbolType(self, Path):
        """ Returns the type of the symbol. """
        return self.__Core.SymbolTreeGetTypeName(Path);

    def GetSymbolSlot(self, Path):
        """ Returns the slot the given symbol is attached to. """
        if(not self.__SymbolTable.has_key(Path)):
            raise Exceptions.ItemNotFound("symbol-path %s not known."%Path);
        return self.__SymbolTable[Path];

    def ListSymbols(self, Path):
        """ List all Symbols in Path. Return a lsit of strings. """
        #simple map call to core:
        return(self.__Core.SymbolTreeListSymbols(Path));

    def GetSymbolTimeStamp(self, Path):
        """ Return the time of the last update of the symbol pointed by Path. """
        return self.__Core.SymbolTreeGetTimeStamp(Path);

    def GetModus(self, Path, Format=MODUS_FMT_OCTAL):
        """ Return the modus of a symbol or folder in Format.
 If Format is OCTAL, a string with the octal representation of the
 modus will be returnd. If Format is STRING, a string formated like
 the modus in ls -l command will be returned. If Format is INTEGER
 the integer representation of the modus will be returned (base=10!!!)."""
        (User, Group, Modus) = self.__Core.SymbolTreeGetAccess(Path);
        if Format==MODUS_FMT_OCTAL:
            return(ModusToOctString(Modus));
        if Format==MODUS_FMT_STRING:
            return(ModusToString(Modus));
        if Format==MODUS_FMT_INTEGER:
            return(Modus);
        raise pyDCPU.Error("Uknown format-type: %i"%Format);

    def ChangeModus(self, Path, Modus):
        """ Change the modus of the symbol or folder pointed by path.
 Only the OCTAL string format is accepted. """
        (user, group, old_modus) = self.__Core.SymbolTreeGetAccess(Path);
        if isinstance(Modus,int): new_modus = Modus;
        elif isinstance(Modus,(str,unicode)): new_modus = int(Modus,8);
        else: raise pyDCPU.Error("Invalid modus fromat. Expacted str or int got %s"%str(type(Modus)));
        return(self.__Core.SymbolTreeSetAccess(Path,user,group,new_modus));

    def GetOwner(self, Path):
        """ Return the owner name. """
        (user, group, modus) = self.__Core.SymbolTreeGetAccess(Path);
        return(user);

    def ChangeOwner(self, Path, Owner):
        """ Set the owner of a symbol or folder. """
        NameCheck.CheckUser(Owner);
        (old_user, group, modus) = self.__Core.SymbolTreeGetAccess(Path);
        self.__Core.SymbolTreeSetAccess(Path, Owner, group, modus);


    def GetGroup(self, Path):
        """ Return the groupname of a symbol or folder."""
        (owner, group, modus) = self.__Core.SymbolTreeGetAccess(Path);
        return(group);


    def ChangeGroup(self, Path, Group):
        """ Set the group of a symbol or folder."""
        NameCheck.CheckGroup(Group);
        (owner, old_group, modus) = self.__Core.SymbolTreeGetAccess(Path);
        self.__Core.SymbolTreeSetAccess(Path, owner, Group, modus);


    def GetValue(self, Path):
        """ Return the actual value of the symbol pointed by Path. """
        return(self.__Core.SymbolTreeGetValue(Path));


    def SetValue(self, Path, Value):
        """ Set the Value of a symbol pointed by path. """
        self.__Core.SymbolTreeSetValue(Path, Value);





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
        if mod & 0x01: tmp += "r";
        else: tmp += "-";
        if (mod>>1)&0x01: tmp += "w";
        else: tmp += "-";
        if (mod>>2)&0x01: tmp += "x";
        else: tmp += "-";
        rstr += tmp;
        tmp = "";
    return(rstr);


def RecursiveSymbolList(Sys, Path, List=None):
    if not List: List = [];
    FList = Sys.ListFolders(Path);
    for Folder in FList:
        nPath = NormPath(Path+"/"+Folder);
        nList = RecursiveSymbolList(Sys, nPath, List);
        List.extend(nList);
    SList = Sys.ListSymbols(Path);
    for Symbol in SList:
        Symbol = NormPath(Path+"/"+Symbol);
        List.append(Symbol)
    return(List);


def NormPath(Path):
    tmpList = Path.split("/");
    PList = [];
    for tmp in tmpList:
        if tmp and tmp != "": PList.append(tmp);
    Path = "/"+string.join(PList,"/");
    return(Path);














# CHANGELOG:
# 2006-02-09:
#   * updated to new core-API
# 2006-02-08:
#   + updated to new exception model
# 2005-08-28:
#   + add move/rename folders.
# 2005-08-26:
#   + add moveing/renaming symbols feature.
# 2005-08-25:
#   + add Alias-, user-, ... namecheck.
# 2005-07-23:
#   + implemented new Server/Device/Core-Mod management.
# 2005-06-05:
#   + Add module-version info-methods
# 2005-06-04:
#   + fixed some methods to provide variable 
#       server-root
# 2005-06-02:
#   + add StopServers() method      
#   + add StopDevices() method
#   + add ClearSymbolTree() method
#   + add StopAll() method
#   + add SaveSession() method
#   + add LoadSession() method
#   + add GetDeviceInfo() method
# 2005-05-27:
#   + Start changelog. (sorry i missed it)
#   + Release as Version 0.2.0 (alpha)
#   - Fixed wrong Symbol<->DeviceAlias association


