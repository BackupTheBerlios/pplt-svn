# ############################################################################ #
# This is part of the pyDCPU project. pyDCPU is a framework for industrial     # 
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
# 2005-08-28:
#   + add move/rename folders
# 2005-08-26:
#   + add removeing/renameing symbols feature.
# 2005-08-25:
#   + added check for master/export names, ...
# 2005-05-27:
#   - bug: inconsistent refcounter in Core.MasterTreeDel();

import xml.dom.minidom;
import Logging;
import UserDB;
import Importer;
import SymbolTree;
import ObjectTree;
import ExportableSymbolTree;
import NameCheck;
import Fingerprint;
import MasterObject;
import Exceptions;
import sys;

# ############################################################################ #
# The CoreClass:                                                               #
#   - handle all interactions with a controler                                 #
#   - manage all important elements internal                                   # 
#   - represent all obj by IDs (so it is exportable by RPC )                   #
# ############################################################################ #
class Core:
    """ This is the Core Object/Class
    """


    # ######################################################################## #
    # The INIT method:                                                         #
    #   + create a logger-object                                               #
    #   + init internal managment objects                                      #
    # ######################################################################## #
    def __init__(self,
                 ModulePath=None,
                 UserDBFile=None,
                 LogLevel='info',
                 LogFile = None,
                 SysLog = False):
        
        """ This Function will set the Runtime-Options """
        # Save Parameter
        if ModulePath: self.__ModuleBase   = ModulePath;
        else: self.__ModuleBase = sys.exec_prefix+"/PPLT/CoreMods/";         #if path is not given: default /usr/CoreMods/PPLT, ...
        if UserDBFile: self.__UserDBFile   = UserDBFile;
        else: self.__UserDBFile = sys.exec_prefix+"/PPLT/UserDB.xml";             #if not given -> default: /usr/PPLT/UserDB.xml

        self.__LoggingLevel = LogLevel;
        self.__LoggingFile  = LogFile;
        self.__IsSysLogging = SysLog;
        
        # Setup Logging...
        self.Logger = Logging.SetupLogger(self.__LoggingLevel,
                                          self.__LoggingFile,
                                          self.__IsSysLogging);

        # Load user/group database
        self.__UserDataBase = UserDB.UserDB(self.__UserDBFile);
        
        # Hash of all created Objects
        self.__ObjectHash      = {};
        self.__ObjectRefCount  = {};

        self.Logger.debug("Load modulemanager");
        self.__ModuleManager = Importer.Importer(self.__ModuleBase);
        self.Logger.debug("all modules loaded");

        #Setup Trees: 
        self.__MasterObjTree = ObjectTree.pyObjectTree(self.Logger);

        self.__SymbolTree    = SymbolTree.SymbolTree(self.__UserDataBase.GetSuperUser(),
                                                     self.__UserDataBase.GetSuperUserGrp(),
                                                     384,     #meaning 600 in OCT
                                                     self.__UserDataBase);
        self.__ExporterList  = [];
        
 
    #END OF INIT()


    def __del__(self): Logging.StopLogging();
    
    # ######################################################################## #
    #  Master Tree Handler                                                     # 
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    # MasterTreeAdd(ParentID, ModuleName, Address, Parameters)                 #
    #   - create/connect/add a object to the tree                              #
    #   - return a unique ID for the created obj or None on errror             #
    # ######################################################################## #
    def MasterTreeAdd(self, ParentID, ModName, Address, Parameter):
        """
            This method cares about Object creation and connections... 
        """
        # check Parameter:
        if not Parameter: Parameter = dict();
        
        #check if this module was loaded at the same place with the same prams.
        fingerprint = Fingerprint.Fingerprint(ModName,
                                              Parent = ParentID,
                                              Address = Address,
                                              Parameter = Parameter);
        if self.__ObjectHash.has_key(fingerprint):
            Object = self.__ObjectHash[fingerprint];
            self.Logger.debug("Return cached Object");
            c = self.__ObjectRefCount.get(Object._GetID());
            if not c:
                self.Logger.warning("Ref count is inconsisten!");
                c = 0;
            self.__ObjectRefCount.update( {Object._GetID():c+1} );
            self.Logger.debug("Set ref.-counter up to %i"%self.__ObjectRefCount.get(Object._GetID()));
            return(Object._GetID());
        
        # Connect new Object with Parent
        if ParentID:
            if not self.__ObjectHash.has_key(ParentID):
                raise ItemNotFound("ParentID ($s) not known! Can't connect new object."%ParentID);
            ParentObj = self.__ObjectHash[ParentID];
            Connection = ParentObj.connect(Address);
            if not Connection:
                raise Exceptions.ModuleError("Error while connect to parent (%s)!"%ParentID);
            Connection._SetAddrStr(Address);
        else:
            Connection = None;
            pass;

        Object = self.__ModuleManager.NewMaster(ModName, Connection, Parameter, fingerprint);
        if not Object: raise Exceptions.ItemNotFound("Unknown module $s! Check module path."%ModName);

        self.Logger.debug("Obj from %s with ID:%s created"%(ModName,Object._GetID()));
               
        if not self.__MasterObjTree.Add(ParentID,Object._GetID()):
            Object.destroy();
            del Object;
            raise Exceptions.Error("Can't add object to MasterTree! This should allways work: Mail author!")
       
        self.__ObjectHash.update({Object._GetID():Object});
        self.Logger.debug("Object Added to Tree...");
        self.__ObjectRefCount.update( {Object._GetID():1} );
        return(Object._GetID());



    # ###
    # Find/Destroy/Delete a object from tree by ID
    # MasterTreeDel(ObjectID);
    #   - return True on sucsess or False on error
    # ###
    def MasterTreeDel(self, ObjectID):
        """ This method deletes a object from the tree... """
        Object = self.__ObjectHash.get(ObjectID);
        if not Object: raise Exceptions.ItemNotFound("The requested object (ID: %s) is not known."%ObjectID); 

        c = self.__ObjectRefCount.get(ObjectID);
        if c == None:
            self.Logger.warning("Inconsistent ref counter");
            self.__ObjectRefCount.update( {ObjectID:1} );
        if c > 1:
            self.__ObjectRefCount.update( {ObjectID:c-1} );
            self.Logger.debug("Object ref counter redused to %i"%self.__ObjectRefCount.get(ObjectID));
            return;

        # check if object has no children:
        if Object.Counter != 0:  
            raise Exceptions.ItemBusy("Can't remove object %s(ID:%s): Item is used by others. Count: %i"%(self.GetObjectClass(ObjectID),ObjectID,Object.Counter));
        # destroy object:
        if not Object.destroy(): 
            raise Exceptions.Error("FATAL: Can't destroy object (ID:%s): error while call destroy() method! (MasterTree will be inconsistent)");
        #remove from master-tree:
        if not self.__MasterObjTree.Del(ObjectID):
            raise Exception.Error("FATAL: Can't remove object (ID:%s) from MasterTree! MasterTree may inconsistend! Mail author!");

        
        Object.tear_down();
        del self.__ObjectRefCount[ObjectID];    #remove from ref-count table
        self.Logger.debug("Obj ref count should be None: %s"%str(self.__ObjectRefCount.get(ObjectID)));
        del self.__ObjectHash[ObjectID];        #remove from object hash

        self.Logger.debug("Object removed and destroyed");


    def MasterTreeList(self, ParentID):
        """ This method will list all children of the obj [ParentID]... """
        return(self.__MasterObjTree.List(ParentID));
    



    # ######################################################################## #
    # Export Module handling                                                   # 
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #  
    #   +                                                                      # 
    # ######################################################################## #
    def ExporterAdd(self, ExportModule, Parameters, DefaultUser, Root = '/'):
        """ This method load an export-module """

        # check export-module-name:
        ExportModule = NameCheck.CheckServer(ExportModule);
        if not ExportModule: raise Exceptions.Error("Invalid format for ExportModuleName \"%s\"!"%ExportModule); 

        # check DefaultUserName:
        DefaultUser = NameCheck.CheckUser(DefaultUser);
        if not DefaultUser: raise Exceptions.Error("Invalid user name \"%s\" for default user!"%DefaultUser);

        # check server-root:
        Root = NameCheck.CheckPath(Root);
        if not Root: raise Exceptions.Error("Invalid path \"%s\" for server-root!"%Root);

        if (not self.__SymbolTree.CheckFolder(Root)) and (Root!="/"):
            raise Exceptions.ItemNotFound("Server-root \"%s\" doesn't exists!"%Root);

        fingerprint = Fingerprint.Fingerprint(Name = ExportModule, 
                                              DefaultUser = DefaultUser, 
                                              Parameter = Parameters,
                                              Root = Root);

        if self.__ObjectHash.has_key(fingerprint):
            self.Logger.debug("Return cached object");
            Obj = self.__ObjectHash[fingerprint];
            c = self.__ObjectRefCount.get(Obj._GetID());
            self.__ObjectRefCount.update( {Obj._GetID():c+1} );
            return(Obj._GetID());

        ExpSymTree = ExportableSymbolTree.ExportableSymbolTree(self.__SymbolTree,
                                                               self.__UserDataBase,
                                                               DefaultUser,
                                                               Root);

        Obj = self.__ModuleManager.NewExporter(ExportModule, Parameters, fingerprint, ExpSymTree);
        if not Obj: raise Exceptions.ModuleError("Error while setup module \"%s\"!"%ExportModule);

        self.Logger.debug("Export Module %s loaded as ID %s"%(ExportModule,Obj._GetID()));

        self.__ExporterList.append(Obj._GetID());

        self.__ObjectHash.update({Obj._GetID():Obj});
        self.__ObjectRefCount.update( {Obj._GetID():1} );
        self.Logger.debug("Object Added to Tree...");
        return(Obj._GetID());
        
       
    def ExporterDel(self, ObjectID):
        """ This method stop a export-module """
        Obj = self.__ObjectHash.get(ObjectID);
        if not Obj: raise Exceptions.ItemNotFound("No module found with ID %s!"%ObjectID);

        c = self.__ObjectRefCount.get(ObjectID);
        if c > 1:
            self.__ObjectRefCount.update( {ObjectID:c-1} );
            return(True);

        if not Obj.stop(): raise Exceptions.ModuleError("Error while stop module!");

        del self.__ObjectHash[ObjectID];
        self.__ExporterList.remove(ObjectID);
        del self.__ObjectRefCount[ObjectID];
   
   
    def ExporterList(self):
        """ This method list all loaded export-modules """
        return(self.__ExporterList);
    


    # ######################################################################## #
    # SymbolTreeHandler                                                        # 
    # ######################################################################## #
    def SymbolTreeCheckPath(self, Path):
        """ Checks if the path exists """
        return self.__SymbolTree.CheckFolder(Path) or self.__SymbolTree.CheckSymbol(Path);

    def SymbolTreeCreateFolder(self, Path):
        """
            This method creates a new Folder with the Path 'Path'
            NOTE:
                All folders on the path to 'Path' must exist!
        """
        #check folder-path:
        Path = NameCheck.CheckPath(Path);
        if not Path: raise Exceptions.Error("Invalid format for folder-path \"%s\"!"%Path);

        if not self.__SymbolTree.CreateFolder(Path):
            raise Exceptions.Error("Error while create folder: \"%s\"!"%Path);
        self.Logger.debug("Folder created");
        return(True);

    def SymbolTreeMoveFolder(self, From, To):
        """ This method moves a folder from (From) to (To)."""
        #check path of destination:
        To = NameCheck.CheckPath(To);
        if not To: raise Exceptions.Error("Invalid path \"%s\" for new destination!"%To);
        if not self.__SymbolTree.MoveFolder(From, To):
            raise Exceptions.Error("Error while move folder \"%s\" to \"%s\"!"%(From,To));
        return(True);

    def SymbolTreeDeleteFolder(self,  Path):
        """ This method will delete folder Path """
        if not self.__SymbolTree.DeleteFolder(Path):
            raise Exceptions.Error("Error while delete folder \"%s\"!"%Path);
        self.Logger.debug("Folder %s deleted"%Path);
        return(True);
    

    def SymbolTreeCreateSymbol(self, Path, ObjectID, Address=None, Timeout=0.5):
        """ This method create a new symbol in the symbol-tree. """
        #check symbol-path:
        Path = NameCheck.CheckPath(Path);
        if not Path: raise Exceptions.Error("Invalid path \"%s\" for a symbol!"%Path);

        Obj = self.__ObjectHash.get(ObjectID);
        if not Obj: raise Exception.ItemNotFound("No module with ID %s found!"%ObjectID);

        Connection = Obj.connect(Address);
        if not Connection: 
            raise Exceptions.Error("Can't connect to module %s!"%ObjectID);
        # if connection is connection to a value: set timeout
        if isinstance(Connection, MasterObject.ValueConnection):
            if Timeout: Connection.SetTimeout(Timeout);

        # store in symboltree: (also Address and timeout for rebuild):   
        try: self.__SymbolTree.CreateSymbol(Path, Connection, Address, Timeout);
        except Exception,e:
            Connection.close();
            raise Exceptions.SymbolError("Error while create symbol \"%s\": %s"%(Path,str(e)));
        return(True);

    
    def SymbolTreeMoveSymbol(self, From, To):
        """ This method moves a symbol From -> To. """
        To = NameCheck.CheckPath(To);
        if not To: raise Exceptions.Error("Destination \"%s\" isn't a valid path!"%To);
        if not self.__SymbolTree.MoveSymbol(From,To):
            raise Exceptions.SymbolError("Error while move symbol from %s to %s!"%(From,To));
        return(True);


    def SymbolTreeDeleteSymbol(self, Path):
        """ This method will del symbol Path """
        if not self.__SymbolTree.DeleteSymbol(Path):
            raise Exceptions.SymbolError("Unable to remove symbol \"%s\"!"%Path);
        self.Logger.debug("Symbol %s deleted"%Path);
        return(True);
    

    def SymbolTreeGetValue(self, Path):
        return(self.__SymbolTree.GetValue(Path, self.__GetSystemSession()));
    def SymbolTreeSetValue(self, Path, Value):
        return(self.__SymbolTree.SetValue(Path, Value, self.__GetSystemSession()));
    def SymbolTreeListSymbols(self, Path):
        return(self.__SymbolTree.ListSymbols(Path, self.__GetSystemSession()));
    def SymbolTreeListFolders(self, Path):
        return(self.__SymbolTree.ListFolders(Path, self.__GetSystemSession()));


    def SymbolTreeGetTimeStamp(self, Path):
        return self.__SymbolTree.GetLastUpdate(Path, self.__GetSystemSession());


    def SymbolTreeGetAccess(self, Path):
        owner = self.__SymbolTree.GetOwnerName(Path);
        group = self.__SymbolTree.GetGroupName(Path);
        modus = self.__SymbolTree.GetRightString(Path);
        return( (owner, group, modus) );

    def SymbolTreeSetAccess(self, Path, Owner, Group, Modus):
        if not self.__SymbolTree.SetOwnerName(Path, Owner):
            return(False);
        if not self.__SymbolTree.SetGroupName(Path, Group):
            return(False);
        if not self.__SymbolTree.SetRightString(Path, Modus):
            return(False);
        return(True);





    # ######################################################################## #
    # Private methods!                                                         #
    # ######################################################################## #
    def __GetObjectByID(self,ID):
        self.Logger.debug("Search for %s"%ID);
        return(self.__ObjectHash.get(ID));

    def __GetSystemSession(self):
        return(self.__UserDataBase.OpenSystemSession());


    # ######################################################################## #
    # Methods for providing information about Modules/Objects                  #
    # ######################################################################## #
    def ModInfoXML(self, ModName, Lang):
        return(self.__ModuleManager.GetModuleInfoXML(ModName, Lang));
    def ModInfoModuleExsist(self, ModName):
        return(self.__ModuleManager.IsModule(ModName));
    def ModInfoIsRoot(self, ModName):
        return(self.__ModuleManager.IsModuleRoot(ModName));
    def ModInfoNeedChildAddress(self, ModName):
        return(self.__ModuleManager.NeedChildAddress(ModName));
    def ModInfoGetParaNames(self, ModName):
        return(self.__ModuleManager.GetParameterNames(ModName));
    def ModInfoIsParaDuty(self, ModName, ParaName):
        return(self.__ModuleManager.IsParameterDuty(ModName,ParaName));
    def ModInfoGetParaDefVal(self, ModName, ParaName):
        return(self.__ModuleManager.GetParameterDefaultValue(ModName, ParaName));
            
   
    # ######################################################################## #
    # Methods for object access                                                #
    # ######################################################################## #
    def GetAConnection(self, ObjectID, Address):
        """ This method will return a connection object.
  NOTE: Please use this method only if you use pyDCPU as a library. For example if you
  develop new modules.  """
        Obj = self.__GetObjectByID(ObjectID);
        if not Obj: raise Exceptions.ItemNotFound("No module with ID %s found!"%ObjectID);
        if not hasattr(Obj,"connect"):
            raise Exceptions.BadModule("Can't connect to Obj(%s): no connect() method, may bad API!"%ObjectID);
        Con = Obj.connect(Address);
        if not Con: raise Exceptions.Error("Unable to connect to Module %s"%ObjectID);
        return Con;
        

    # will be removed
    def GetObjectClass(self, ObjectID):
        Obj = self.__GetObjectByID(ObjectID);
        if not Obj: raise Exceptions.ItemNotFound("No module with ID %s found!"%ObjectID);
        return(Obj._GetClass());


    # will be removed
    def GetExportableSymbolTree(self, DefaultUser):
        return(ExportableSymbolTree.ExportableSymbolTree(self.__SymbolTree,
                                                         self.__UserDataBase,
                                                         DefaultUser));
    # will be removed
    def GetTheUserDB(self):
        """ Please don't use this method!"""
        return(self.__UserDataBase);

