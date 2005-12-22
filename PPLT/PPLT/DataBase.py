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
# 2005-09-09:
#   + added [Un|]Install[Device|Server|CoreMods]() methods
# 2005-09-07:
#   - fixed damaged GetDescription() in CoreModItem class
# 2005-08-28:
#   - fixed crash if a module-requirement is not meet.
# 2005-08-20:
#   - fixed crash if no modules are preset. (in RGlob())
# 2005-06-19:
#   Initial.

import pyDCPU;
import ServerMeta;
import DeviceMeta;
import os.path;
import fnmatch;
import zipfile;
import xml.dom.minidom;
import logging;
import shutil;
import string;
  
class DataBase:
    """ The Module database handles all kinds of modules, like servers, devices
and core-modules.
You can install and uninstall (if you have the right to do) modules. """
    def __init__(self, CoreModPath, PPLTModPath, Lang, AltLang):
        self.__Logger           = logging.getLogger("PPLT");
        self.__CoreModulePath   = CoreModPath;
        self.__PPLTModulePath   = PPLTModPath;
        self.__Lang             = Lang;
        self.__AltLang          = AltLang;
    
        self.__Servers          = BaseClass();
        self.__Devices          = BaseClass();
        self.__CoreMods         = BaseClass();

        # find (recursive) all files ending with .zip starting at self.__CoreModulePath:         
        ZIPList = RGlob(self.__CoreModulePath,"*.zip");
        self.__Logger.info("Try to add %i DCPU-Modules to DB"%len(ZIPList));

        for ZIPFile in ZIPList:
            try:
                # try to create a meta-data item from the zip file
                Item = CreateItem(ZIPFile, Lang, AltLang, self);
            except Exception, e:
                self.__Logger.error("Error while add Core mod %s to DB: %s"%(ZIPFile,str(e)))
                Item = None;
                continue;
            if isinstance(Item, CoreModItem):
                # because the classname is a filepath i need to determ the classname:
                ClassList = ClassFromPath(ZIPFile,self.__CoreModulePath);
                ItemName  = Item.GetName();
                #add item to coremod list:
                self.__CoreMods.AddItem(Item, ItemName, ClassList);
            else:
                self.__Logger.fatal("DB-Item is not a CoreModItem! (%s)"%ZIPFile);
                
        # find (rec.) all files anding with .xml starting at path in self.__PPLTModulePath:
        XMLList = RGlob(self.__PPLTModulePath, "*.xml");
        self.__Logger.info("Try to add %i PPLT-Modules to DB"%len(XMLList));
        for XMLFile in XMLList:
            try:
                # create meta-data item from XML file:
                Item = CreateItem(XMLFile, Lang, AltLang, self);
            except Exception, e:
                self.__Logger.error("Error while load PPLT mod %s to DataBase: %s"%(XMLFile,str(e)));
                Item = None;
            if isinstance(Item, ServerItem):
                # if item is a server item:
                ClassList = Item.GetClass().split(".");
                ItemName  = Item.GetName()
                self.__Servers.AddItem(Item, ItemName, ClassList);
            elif isinstance(Item, DeviceItem):
                # if item is device item:
                ClassList = Item.GetClass().split(".");
                ItemName  = Item.GetName();
                self.__Devices.AddItem(Item, ItemName, ClassList);


    # ###################################################################### #
    # Objects to handle server/device info easily                            #
    # ###################################################################### #
    def GetServerInfo(self, SerName):
        """ Return a ServerInfo instance. To access server specific information."""
        if not self.HasServer(SerName):
            return(None);
        return(ServerInfo(SerName, self));

    def GetDeviceInfo(self, DevName):
        """Return a DeviceInfo instance. To access device specific information."""
        if not self.HasDevice(DevName):
            return(None);
        return(DeviceInfo(DevName, self));

    # ###################################################################### #
    # Methods to handle servers                                              #
    # ###################################################################### #
    def ListServerClasses(self, Class=None):
        """ List all server-classes in the given class,
 if Class is obmited, all root-classes will be returned."""
        if Class:
            ClassLst = Class.split(".");
        else:
            ClassLst = [];
        return(self.__Servers.ListClasses(ClassLst));

    def ListServers(self, Class=None):
        " List all servers in the given class. "
        if not Class:
            ClassLst = [];
        else:
            ClassLst = Class.split(".");
        return(self.__Servers.ListItems(ClassLst));

    def __GetServer(self, Name):
        " Internal Function!!! "
        tmp = Name.split(".");
        ClassLst = tmp[:-1];
        Name = tmp[-1];
        return(self.__Servers.FindItem(Name,ClassLst));

    def HasServer(self, Name):
        " This method returns true, if the given server is found "
        if self.__GetServer(Name): return(True);
        return(False);

    def InstallServer(self, File):
        " Install/Update the server in file. And add to DB."
        #test if I can write do dir:
        if not os.access(self.__PPLTModulePath, os.F_OK|os.W_OK):
            self.__Logger.error("Can't write to PPTL module dir %s."%self.__PPLTModulePath);
            return False;
        # parse and check file
        try: Item = CreateItem(File, self.__Lang, self.__AltLang, self);
        except Exception,e:
            self.__Logger.error("Error while add Server %s to DataBase: %s"%(File, str(e)));
            return False;
        #check if I know this server already:
        FQSN = Item.GetClass()+"."+Item.GetName();
        if self.HasServer(FQSN): 
            #remove server from list and from filesystem:
            if not self.UnInstallServer(FQSN):
                self.__Logger.error("Unable to uninstall old server (%s)."%FQSN);
                return False;
        #copy new server-file into PPLT-Module-Dir:
        newFile = string.join(FQSN.split("."),"_")+".xml";
        newFile = os.path.normpath(self.__PPLTModulePath+"/"+newFile);
        try: shutil.copyfile(File,newFile);
        except Exception, e:
            self.__Logger.error("Can't install new server %s: Can't copy from %s to %s. (%s)"%(FQSN,File,newFile,str(e)));
            return False;
        #create new server-item at new path:
        try: Item = CreateItem(newFile, self.__Lang, self.__AltLang, self);
        except:
            self.__Logger.error("Error while install server %s: Unable to reate DB item from file %s"%(FQSN, newFile));
            return False;
        # add to DB:        
        if not isinstance(Item, ServerItem):
            self.__Logger.error("Error while add %s from %s to DB."%(FQSN, newFile));
            return False;
        ClassList = Item.GetClass().split(".");
        ItemName  = Item.GetName()
        self.__Servers.AddItem(Item, ItemName, ClassList);
        return True;
        # ::: DONE :::

    def UnInstallServer(self, Name):
        " Uninstall and remove given server from database. "
        #check if server exisits:
        if not self.HasServer(Name):
            self.__Logger.error("Unable to uninstall server %s: Server unknown!"%Name);
            return False;
        # get server filename and remove it:
        Item = self.__GetServer(Name);
        try: os.remove(Item.GetFilePath());
        except:
            self.__Logger.error("Error while uninstall server %s: Unable to remove file %s!"%(Name, Item.GetFilePath()));
            return False;
        #remove item from DB:
        ClassList = Item.GetClass().split(".");
        ItemName = Item.GetName();
        self.__Servers.DelItem(ItemName, ClassList);
        return True;
        # ::: DONE :::

    def GetServerVersion(self, Name):
        " Returns the Version-Object of the given server. "
        Srv = self.__GetServer(Name);
        if not Srv: return(None);
        return(Srv.GetVersion());

    def GetServerPath(self, Name):
        " Returns the file-path to the server given. "
        Srv = self.__GetServer(Name);
        if not Srv: return(None);
        return(Srv.GetFilePath());

    def GetServerDescription(self, Name):
        """ Returns the description of the given server, if found. In the given
 Lang or AltLang. Return an empy string on error."""
        Srv = self.__GetServer(Name);
        if not Srv: return(None);
        return(Srv.GetDescription(self.__Lang, self.__AltLang));

    def GetServerVariables(self, Name):
        " Returns a list of variables (parameters) a server needs to setup. "
        Srv = self.__GetServer(Name);
        if not Srv: return(None);
        return(Srv.GetVariables());

    def GetServerVariableHelp(self, SrvName, VarName):
        """ Returns a short info about the given variable of the server. 
 Returns a empty string on error."""
        Srv = self.__GetServer(SrvName);
        if not Srv: return("");
        return(Srv.GetVariableHelp(VarName, self.__Lang, self.__AltLang));

    def GetServerDefaultValue(self, SrvName, VarName):
        """ Returns the default value of the given variable of the server.
 Returns None on error."""
        Srv = self.__GetServer(SrvName);
        if not Srv: return(None);
        return(Srv.GetDefaultValue(VarName));

    def GetServerReqCoreMods(self, SrvName):
        """ Returns the core modules required by the server. """
        Srv = self.__GetServer(SrvName);
        if not Srv: return(None);
        return Srv.GetReqCoreMods();

    # ###################################################################### #
    # Methods to handle devices                                              # 
    # ###################################################################### #
    def ListDeviceClasses(self, Class=None):
        """ Return a list of all device-classes in given class, if Class is obmited,
 all root classes will be listed. """
        if Class:
            ClassLst = Class.split(".");
        else:
            ClassLst = [];
        return(self.__Devices.ListClasses(ClassLst));

    def ListDevices(self, Class=None):
        " List all devices in class. "
        if not Class:
            ClassLst = [];
        else:
            ClassLst = Class.split(".");
        return(self.__Devices.ListItems(ClassLst));

    def __GetDevice(self, Name):
        " Internal used function. "
        tmp = Name.split(".");
        Class = tmp[:-1];
        Name  = tmp[-1];
        return(self.__Devices.FindItem(Name, Class));

    def HasDevice(self, Name):
        " Retuns True if device could be found. "
        if self.__GetDevice(Name): return(True);
        return(False);

    def InstallDevice(self, File):
        " Install/Update a device and add it to the DB." 
        #test if I can write do dir:
        if not os.access(self.__PPLTModulePath, os.F_OK|os.W_OK):
            self.__Logger.error("Can't write to PPTL module dir %s."%self.__PPLTModulePath);
            return False;
        # parse and check file
        try: Item = CreateItem(File, self.__Lang, self.__AltLang, self);
        except Exception, e:
            self.__Logger.error("Error while add Device %s: Parse error! (%s)"%(File,str(e)));
            return False;
        #check if I know this device already:
        FQDN = Item.GetClass()+"."+Item.GetName();
        if self.HasDevice(FQDN): 
            #remove device from list and from filesystem:
            if not self.UnInstallDevice(FQDN):
                self.__Logger.error("Unable to uninstall old device (%s)."%FQDN);
                return False;
        #copy new device-file into PPLT-Module-Dir:
        newFile = string.join(FQDN.split("."),"_")+".xml";
        newFile = os.path.normpath(self.__PPLTModulePath+"/"+newFile);
        try:shutil.copyfile(File,newFile);
        except Exception, e:
            self.__Logger.error("Can't install new device %s: Can't copy from %s to %s. (%s)"%(FQDN,File,newFile, str(e)));
            return False;
        #create new device-item at new path:
        try: Item = CreateItem(newFile, self.__Lang, self.__AltLang, self);
        except Exception,e:
            self.__Logger.error("Error while install device %s: Unable to reate DB item from file %s. (%s)"%(FQDN, newFile,str(e)));
            return False;
        # add to DB:        
        if not isinstance(Item, DeviceItem):
            self.__Logger.error("Error while add %s from %s to DB."%(FQDN, newFile));
            return False;
        ClassList = Item.GetClass().split(".");
        ItemName  = Item.GetName()
        self.__Devices.AddItem(Item, ItemName, ClassList);
        return True;
        # ::: DONE :::

    def UnInstallDevice(self, Name):
        " Uninstall a device "
        #check if device exisits:
        if not self.HasDevice(Name):
            self.__Logger.error("Unable to uninstall device %s: Device unknown!"%Name);
            return False;
        # get device filename and remove it:
        Item = self.__GetDevice(Name);
        try: os.remove(Item.GetFilePath());
        except:
            self.__Logger.error("Error while uninstall device %s: Unable to remove file %s!"%(Name, Item.GetFilePath()));
            return False;
        #remove item from DB:
        ClassList = Item.GetClass().split(".");
        ItemName = Item.GetName();
        self.__Devices.DelItem(ItemName, ClassList);
        return True;
        # ::: DONE :::

    def GetDeviceVersion(self, Name):
        " Returns the Version-Object of the given device. "
        Dev = self.__GetDevice(Name);
        if not Dev: return(None);
        return(Dev.GetVersion());

    def GetDevicePath(self, Name):
        " Returns the whole path to the device file. "
        Dev = self.__GetDevice(Name);
        if not Dev: return(None);
        return(Dev.GetFilePath());

    def GetDeviceDescription(self, Name):
        """ Returns the description of the given device in the Lang or AltLang,
 if found. Returns an empty string on error."""
        Dev = self.__GetDevice(Name);
        if not Dev: return("");
        return(Dev.GetDescription(self.__Lang, self.__AltLang));

    def GetDeviceVariables(self, Name):
        " Return a list of all variables the device need to setup. "
        Dev = self.__GetDevice(Name);
        if not Dev: return(None);
        return(Dev.GetVariables());

    def GetDeviceVariableHelp(self, DevName, VarName):
        " Return a short help for the variable of the deivce."
        Dev = self.__GetDevice(DevName);
        if not Dev: return("");
        return(Dev.GetVariableHelp(VarName, self.__Lang, self.__AltLang));

    def GetDeviceDefaultValue(self, DevName, VarName): 
        " Return the default value of the given variable of the device. "
        Dev = self.__GetDevice(DevName);
        if not Dev: return(None);
        return(Dev.GetDefaultValue(VarName));

    def GetDeviceNameSpaces(self, DevName):
        " Return a list of all Namespaces of the device. "
        Dev = self.__GetDevice(DevName);
        if not Dev: return(None);
        return(Dev.GetNameSpaces());

    def GetSlots(self, DevName, NS):
        " Return all slots of a namespace of a device. "
        Dev = self.__GetDevice(DevName);
        if not Dev: return(None);
        return(Dev.GetSlots(NS));

    def GetSlotDescription(self, DevName, NS, Slot):
        " Return a short description of the slot. "
        Dev = self.__GetDevice(DevName);
        if not Dev: return("");
        return(Dev.GetSlotDescription(NS, Slot, self.__Lang, self.__AltLang));

    def GetSlotType(self, DevName, NS, Slot):
        " Return the type (a string) of the slot. "
        Dev = self.__GetDevice(DevName);
        if not Dev: return(None);
        return(Dev.GetSlotType(NS, Slot));
    
    def GetSlotMode(self, DevName, NS, Slot):
        " Return the mode (one of: r, w, rw) of the slot. "
        Dev = self.__GetDevice(DevName);
        if not Dev: return(None);
        return(Dev.GetSlotMode(NS, Slot));

    def GetSlotRanges(self, DevName, NS):
        " Return all slot-ranges a namespace of a device. "
        Dev = self.__GetDevice(DevName);
        if not Dev: return(None);
        return(Dev.GetSlotRanges(NS));

    def GetSlotRangeDescription(self, DevName, NS, SlotRange):
        " Return a short description of the SlotRange. "
        Dev = self.__GetDevice(DevName);
        if not Dev: return("");
        return(Dev.GetSlotRangeDescription(NS, SlotRange, self.__Lang, self.__AltLang));

    def GetDeviceReqCoreMods(self, DevName):
        """ Return required coremodules for the device. """
        Dev = self.__GetDevice(DevName);
        if not Dev: return None;
        return Dev.GetReqCoreMods();

    

    # ###################################################################### #
    # Methods to handle core-modules                                         # 
    # ###################################################################### #
    def ListCoreModClasses(self, Class=None):
        """ List all sub-classes in the given class. If Class is obmited, all
 root classes will be returnd."""
        if Class:
            ClassLst = Class.split(".");
        else:
            ClassLst = [];
        return(self.__CoreMods.ListClasses(ClassLst));

    def ListCoreMods(self, Class):
        " List all core modules in the given class. "
        ClassLst = Class.split(".");
        return(self.__CoreMods.ListItems(ClassLst));

    def __GetCoreMod(self, Name):
        " Internal Function!!! "
        tmp = Name.split(".");
        Name = tmp[-1];
        ClassList = tmp[:-1];
        #print "Try to find %s in %s"%(Name,str(ClassList))
        return(self.__CoreMods.FindItem(Name,ClassList));

    def HasCoreMod(self, Name):
        " Return True if core module is found. "
        if self.__GetCoreMod(Name): return(True);
        return(False);

    def GetCoreModPath(self, Name):
        " Return the full path to the core module file. "
        Mod = self.__GetCoreMod(Name);
        if not Mod: return(None);
        return(Mod.GetFilePath());

    def GetCoreModVersion(self, Name):
        " Return the version object if the core module. "
        Mod = self.__GetCoreMod(Name);
        if not Mod: return(None);
        return(Mod.GetVersion());

    def GetCoreModDescription(self, Name):
        " Return a short description about the core module. "
        Mod = self.__GetCoreMod(Name);
        if not Mod: return("");
        return(Mod.GetDescription(self.__Lang, self.__AltLang));

    def InstallCoreMod(self, File, AsName):
        " Install a core module file as the give FQ core module name. "
        #check if module already exists, if yes -> then delete it:
        if self.HasCoreMod(AsName):
            if not self.UnInstallCoreMod(AsName):
                self.__Logger.error("Unable to install %s: Can't delete old Coremodule-file."%AsName);
                return False;
        #check if target folder already exists, if not -> create folder:
        FileName = AsName.split(".")[-1]+".zip";
        DirName  = os.path.normpath(self.__CoreModulePath+"/"+string.join(AsName.split(".")[:-1],"/"));
        if not os.path.exists(DirName):
            try: os.makedirs(DirName);
            except:
                self.__Logger.error("Unable to install %s: Can't create folder %s!"%(AsName,DirName));
                return False;
        FilePath = os.path.normpath(DirName+"/"+FileName);
        #copy file:
        try: shutil.copyfile(File, FilePath);
        except Exception, e:
            self.__Logger.error("Error while install %s: Can't copy file %s to %s. [%s]"%(AsName, File, FilePath,str(e)));
            return False;
        #crate item and add to db:
        Item = CoreModItem(FilePath);
        self.__CoreMods.AddItem(Item, AsName.split(".")[-1],AsName.split(".")[:-1]);
        return True;

    def UnInstallCoreMod(self, Name):
        " Uninstall a core module. "
        #Find and get core-mod-item:
        Item = self.__GetCoreMod(Name);
        if not Item:
            self.__Logger.error("Can't uninstall core-module %s: Module not known."%Name);
            return False;
        #get filename and remove file:
        FileName = Item.GetFilePath();
        try: os.remove(FileName);
        except:
            self.__Logger.error("Unable to uninstall core-module %s: Can't remove file %s"%(Name, FileName));
            return False;
        #remove item from database:
        ClassList = Name.split(".")[:-1];
        ItemName  = Name.split(".")[-1];
        self.__CoreMods.DelItem(ItemName, ClassList);
        return True;
        
                    
#
# *** END OF CLASS:   DataBase   ***





class BaseClass:
    """ Abstract base class for module classes  Do not use! """

    def __init__(self):
        self.__SubClasses = {};
        self.__Items={};
    
    def FindItem(self, ItemName, ClassList):
        if len(ClassList) == 0:                                             # if class lust is empty:
            return(self.__Items.get(ItemName));                                 # search in my item-list
        SubClass = ClassList.pop(0);                                    # pop next class to search:
        if self.__SubClasses.has_key(SubClass):                         # do i have such a sunclass?:
            return(self.__SubClasses[SubClass].FindItem(ItemName, ClassList));  # recursive:
        return(None);                                                   # subclass not found

    def AddItem(self, Item, ItemName, ClassList):
        if len(ClassList) == 0:
            self.__Items.update( {ItemName:Item} );
            #print "Add %s (%s)"%(ItemName,str(Item));                          # update my item-table
            return(True);
        SubClass = ClassList.pop(0);                                        # pop next subclass:
        if not self.__SubClasses.has_key(SubClass):                         # create a new subclass if missing:
            #print "Create new SubClass %s"%SubClass;
            self.__SubClasses.update( {SubClass:BaseClass()} );                     # ---
        return(self.__SubClasses[SubClass].AddItem(Item, ItemName, ClassList));     #recursive...

    def DelItem(self, Item, ClassList):
        if len(ClassList) == 0:
            if self.__Items.has_key(Item):
                del self.__Items[Item];
                return(True);
            return(False);
        SubClass = ClassList.pop(0);
        if self.__SubClasses.has_key(SubClass):
            return(self.__SubClasses[SubClass].DelItem(Item, ClassList));
        return(False);

    def ListItems(self, ClassList=[]):
        if len(ClassList) == 0:
            return(self.__Items.keys());
        SubClass = ClassList.pop(0);
        if self.__SubClasses.has_key(SubClass):
            return(self.__SubClasses[SubClass].ListItems(ClassList));
        return(None);
    
    def ListClasses(self, ClassList=[]):
        if len(ClassList) == 0:
            return(self.__SubClasses.keys());
        SubClass = ClassList.pop(0);
        if self.__SubClasses.has_key(SubClass):
            return(self.__SubClasses[SubClass].ListClasses(ClassList));
        return(None);


class BaseItem:
    def __init__(self, Name, MetaData):
        self.__Name = Name;
        self.__MetaData = MetaData;

    def GetName(self):
        return(self.__Name);
    def GetDescription(self, Lang, AltLang):
        pass;
    def GetVersion(self):
        pass;
    def GetFilePath(self):
        pass;
    def GetVariables(self):
        pass;
    def GetVariableHelp(self, VarName, Lang, AltLang):
        pass;
    def GetDefaultValue(self, VarName):
        pass;
    # following are only nessery for devices:
    def GetNameSpaces(self):
        pass;
    def GetSlots(self, NS):
        pass;
    def GetSlotRanges(self, NS):
        pass;
    def GetSlotDescription(self, Name, NS, Lang, AltLang):
        pass;
    def GetSlotRangeDescription(self, Name, NS, Lang, AltLang):
        pass;
    def GetSlotType(self, Name, NS):
        pass;
    def GetSlotMode(self, Name, NS):
        pass;





# Class: CoreModItem
#   Database item for a core module.
#
class CoreModItem(BaseItem):
    def __init__(self, FileName):
        self.__FilePath = FileName;
        self.__Meta = pyDCPU.MetaData(FileName);
        (tmp,FileName) = os.path.split(FileName);
        tmp = FileName.split(".");
        BaseItem.__init__(self, tmp[0], self.__Meta);
        self.__Logger = logging.getLogger("PPLT");
        
        if not self.__Meta.CheckDCPUVersion():
            #self.__Logger.error("Error while load %s: Invalid pyDCPU Version."%FileName);
            raise Exception("Can't load CoreMod %s: Invalid pyDCPU Version."%FileName);
        if not self.__Meta.CheckPythonVersion():
            #self.__Logger.error("Error while load %s: Invalid Python Version."%FileName);
            raise Exception("Can't load CoreMod %s: Invalid Python Version."%FileName);
        if not self.__Meta.CheckPythonModules():
            #self.__Logger.error("Error while load %s: Missing Python libs."%FileName);
            raise Exception("Can't load CoreMod %s: Missing python-lib(s)"%FileName);


    def GetDescription(self, Lang, AltLang):
        return(self.__Meta.GetDescription(Lang, AltLang));
    def GetVersion(self):
        return(self.__Meta.GetVersion());
    def GetFilePath(self): return(self.__FilePath);
    def _SetClass(self, Class):
        self.__Class = Class;
    def GetClass(self): return(self.__Class);
    



# Class: ServerItem
#   Database entry for a Server.
#
class ServerItem:
    def __init__(self, FileName, Document, Lang, AltLang, DataBase):
        self.__FileName = FileName;
        # load meta-data from file:
        self.__Meta = ServerMeta.MetaData(Document, Lang, AltLang);
        #check if all needed core-mods are present:
        self.ReqCoreMods = self.__Meta.GetRequiredModules();
        for core_mod in self.ReqCoreMods:
            if not DataBase.HasCoreMod(core_mod):
                raise Exception("Can't load PPLT Module %s: Missing Core-Mod: %s"%(self.__Meta.GetName(),core_mod));
        # ---done---


    def GetName(self):
        return(self.__Meta.GetName());
    def GetVersion(self):
        return(self.__Meta.GetVersion());
    def GetFilePath(self):
        return(self.__FileName);
    def GetClass(self):
        return(self.__Meta.GetClass());
    def GetDescription(self, Lang=None, AltLang=None):
        return(self.__Meta.GetDescription(Lang, AltLang));
    def GetVariables(self):
        return(self.__Meta.GetRequiredVariableNames());
    def GetDefaultValue(self, VarName):
        return(self.__Meta.GetVariableDefaultValue(VarName));
    def GetVariableHelp(self, VarName, Lang=None, AltLang=None):
        return(self.__Meta.GetVariableDescription(VarName, Lang, AltLang));
    def GetReqCoreMods(self): return(self.ReqCoreMods);




# Class: DeviceItem
#   Database entry for a Device.
#   
class DeviceItem:
    def __init__(self, FileName, Document, Lang, AltLang, DataBase):
        self.__FileName = FileName;
        # load meta-data:
        self.__Meta = DeviceMeta.MetaData(Document, Lang, AltLang);
        #check for core-modules:
        self.ReqCoreMods = self.__Meta.GetRequiredModules();
        for core_mod in self.ReqCoreMods:
            if not DataBase.HasCoreMod(core_mod):
                raise Exception("Missing core module %s"%core_mod);
        #---done---

    def GetName(self):
        return(self.__Meta.GetName());
    def GetVersion(self):
        return(self.__Meta.GetVersion());
    def GetClass(self):
        return(self.__Meta.GetClass());
    def GetFilePath(self):
        return(self.__FileName);
    def GetDescription(self, Lang=None, AltLang=None):
        return(self.__Meta.GetDescription(Lang, AltLang));
    def GetVariables(self):
        return(self.__Meta.GetRequiredVariableNames());
    def GetDefaultValue(self, VarName):
        return(self.__Meta.GetVariableDefaultValue(VarName));
    def GetVariableHelp(self, VarName, Lang=None, AltLang=None):
        return(self.__Meta.GetVariableDescription(VarName, Lang, AltLang));
    def GetNameSpaces(self):
        return(self.__Meta.GetNameSpaces());
    def GetSlots(self, NS):
        return(self.__Meta.GetSlots(NS));
    def GetSlotRanges(self, NS):
        return(self.__Meta.GetSlotRanges(NS));
    def GetSlotDescription(self, NS, Name, Lang=None, AltLang=None):
        return(self.__Meta.GetSlotDescription(NS, Name, Lang, AltLang));
    def GetSlotRangeDescription(self, NS, Name, Lang=None, AltLang=None):
        return(self.__Meta.GetSlotRangeDescription(NS, Name, Lang, AltLang));
    def GetSlotType(self, NS, Name):
        return(self.__Meta.GetSlotType(NS, Name));
    def GetSlotMode(self, NS, Name):
        return(self.__Meta.GetSlotMode(NS, Name));
    def GetReqCoreMods(self): return self.ReqCoreMods;


class ServerInfo:
    """Proxyclass for DataBase to access specific information for
 a singe server."""
    
    def __init__(self, ServerName, DataBaseObj):
        self.__DataBase = DataBaseObj;
        self.__ServerName = ServerName;

    def GetDescription(self):
        return(self.__DataBase.GetServerDescription(self.__ServerName));

    def GetRequiredVariableNames(self):
        return(self.__DataBase.GetServerVariables(self.__ServerName));
    
    def GetVariableDefaultValue(self, VarName):
        return(self.__DataBase.GetServerDefaultValue(self.__ServerName, VarName));

    def GetVariableDescription(self, VarName):
        return(self.__DataBase.GetServerDefaultValue(self.__ServerName, VarName));



class DeviceInfo:
    """ Proxyclass for Database to simplify accessing information for
 a specific Device. """
    def __init__(self, DeviceName, DataBaseObj):
        self.__DeviceName = DeviceName;
        self.__DataBase = DataBaseObj;

    def GetDescription(self):
        return(self.__DataBase.GetDeviceDescription(self.__DeviceName));

    def GetRequiredVariableNames(self):
        return(self.__DataBase.GetDeviceVariables(self.__DeviceName));

    def GetVariableDefaultValue(self, VarName):
        return(self.__DataBase.GetDeviceDefaultValue(self.__DeviceName, VarName));

    def GetVariableDescription(self, VarName):
        return(self.__DataBase.GetDeviceVariableHelp(self.__DeviceName, VarName));

    def GetNameSpaces(self):
        return(self.__DataBase.GetDeviceNameSpaces(self.__DeviceName));

    def GetSlots(self, NS):
        return(self.__DataBase.GetSlots(self.__DeviceName, NS));

    def GetSlotType(self, NS, Name):
        return(self.__DataBase.GetSlotType(self.__DeviceName, NS, Name));

    def GetSlotMode(self, NS, Name):
        return(self.__DataBase.GetSlotMode(self.__DeviceName, NS, Name));

    def GetSlotDescription(self, NS, Name):
        return(self.__DataBase.GetSlotDescription(self.__DeviceName, NS, Name));

    def GetSlotRanges(self, NS):
        return(self.__DataBase.GetSlotRanges(self.__DeviceName, NS));

    def GetSlotRangeDescription(self, NS, Name):
        return(self.__DataBase.GetSlotRangeDescription(self.__DeviceName, NS, Name));






def CreateItem(FileName, Lang, AltLang, DataBase):
    Logger = logging.getLogger("PPLT");
    if zipfile.is_zipfile(FileName):
        return(CoreModItem(FileName));

    try:
        doc = xml.dom.minidom.parse(FileName);
    except:
        Logger.error("Error while parese file %s"%FileName);    
        return(None);

    root = doc.documentElement;
    Item = None;

    #print root.localName;

    if root.localName == "PPLTDevice":
        Item = DeviceItem(FileName, doc, Lang, AltLang, DataBase);
    elif root.localName == "PPLTServer":
        Item = ServerItem(FileName, doc, Lang, AltLang, DataBase);
    return(Item);


def RGlob(Path, Pattern):
    """ Recursive glob() function. """
    Path = os.path.normpath(Path);
    List = [];

    try:
        for item in os.listdir(Path):
            item_path = os.path.join(Path,item);
            if os.path.isfile(item_path):
                if fnmatch.fnmatch(item_path,Pattern):
                    List.append(item_path);
            if os.path.isdir(item_path):
                SubList = RGlob(item_path, Pattern);
                List.extend(SubList);
    except:
        pass;
    return(List);


def ClassFromPath(Path, RelPath):
    """ Converters a fs-path to a class-path. """
    Path    = os.path.normpath(Path);
    RelPath = os.path.normpath(RelPath);
    PathLst = os.path.dirname(Path).split(os.path.sep);
    RelLst  = RelPath.split(os.path.sep);
    n = len(RelLst);
    return(PathLst[n:]);




if __name__ == "__main__":
    DB = DataBase("/usr/PPLT","/usr/PPLT/Mods","de","en");
    print DB.ListCoreMods("Master.Device");
