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
# 2005-05-27:
#	- bug: inconsistent refcounter in Core.MasterTreeDel();

import xml.dom.minidom;
import pyDCPUCoreLogging;
import UserDB;
import Modules;
import pyDCPUSymbolSlot;
import pyDCPUSymbolTree;
import pyDCPUObjectTree;
import ExportableSymbolTree;




# ############################################################################ #
# The CoreClass:                                                               #
#   - handle all interactions with a controler                                 #
#   - manage all important elements internal                                   # 
#   - represent all obj by IDs (so it is exportable by RPC                     #
# ############################################################################ #
class Core:
    """ This is the Core Object/Class
        Basic Features:
            - easy handling of Master, Slave Trees and the
              BridgeList...
            - provide a basic User/Group handling/validating
            - some methods to provide information about the
              modules and the system state.
    """


    # ######################################################################## #
    # The INIT method:                                                         #
    #   + load all modules from mod-dir-list                                   #
    #   + create a logger-object                                               #
    #   + init internal managment objects                                      #
    # ######################################################################## #
    def __init__(self,
                 ModulePath,
                 UserDBFile=None,
                 LogLevel='info',
                 LogFile = None,
                 SysLog = False):
        
        """ This Function will set the Runtime-Options """
        # Save Parameter
        self.__ModuleBase   = ModulePath;
        self.__UserDBFile   = UserDBFile;
        self.__LoggingLevel = LogLevel;
        self.__LoggingFile  = LogFile;
        self.__IsSysLogging = SysLog;
        
        # Setup Logging...
        self.Logger = pyDCPUCoreLogging.SetupLogger(self.__LoggingLevel,
                                                    self.__LoggingFile,
                                                    self.__IsSysLogging);

        # Load user/group database
        self.__UserDataBase = UserDB.UserDB(self.Logger, self.__UserDBFile);
        
#        self.__ExportList      = [];   
        
        # Hash of all created Objects
        self.__ObjectHash      = {};
        self.__ObjectRefCount  = {};

        self.Logger.debug("Load modulemanager");
        self.__ModuleManager = Modules.Importer(self.__ModuleBase);
        self.Logger.debug("all modules loaded");

        #Setup Trees: 
        self.__MasterObjTree = pyDCPUObjectTree.pyObjectTree(self.Logger);

        self.__SymbolTree    = pyDCPUSymbolTree.SymbolTree(self.__UserDataBase.GetSuperUser(),  
                                                           self.__UserDataBase.GetSuperUserGrp(),
                                                           384,		#meaning 600 in OCT
                                                           self.__UserDataBase,
                                                           self.Logger);
        self.__ExporterList  = [];
        
 
    #END OF INIT()



    
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
        #check if this module was loaded in the sameplace with the same prams.
        fingerprint = Modules.Fingerprint(Name = ModName, 
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
            return(Object._GetID());
        
        # Connect new Object with Parent
        if ParentID:
            ParentObj = self.__ObjectHash[ParentID];
            Connection = ParentObj.connect(Address);
            if not Connection:
                self.Logger.error("Error while connect Obj %s to %s"%(Object._GetID,ParentID));
                return(None);
            Connection._SetAddrStr(Address);
        else:
            Connection = None;
            pass;

        Object = self.__ModuleManager.NewMaster(ModName, Connection, Parameter, fingerprint);
        if not Object:
            self.Logger.error("Error while create Object");
            return(None);

        self.Logger.debug("Obj from %s with ID:%s created"%(ModName,Object._GetID()));
               
        if not self.__MasterObjTree.Add(ParentID,Object._GetID()):
            self.Logger.error("Can't add Object...");
            Object.destroy();
            del Object;
            return(None);

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
        Object = self.__ObjectHash[ObjectID];
        if not Object:
            self.Logger.error("No Object with ID %s"%str(ObjectID));
            return(False);

        c = self.__ObjectRefCount.get(ObjectID);
        if c == None:
            self.Logger.warning("Inconsistent ref counter");
            self.__ObjectRefCount.update( {ObjectID:1} );
        if c > 1:
            self.__ObjectRefCount.update( {ObjectID:c-1} );
            self.Logger.debug("Object ref counter redused.");
            return(True);
		
        if not self.__MasterObjTree.Del(ObjectID):
            self.Logger.error("Error while del Object from tree");
            return(False);

        if not Object.destroy():
            self.Logger.error("Error while delete object %s"%str(ObjectID));
            return(False);

        del Object;								#destroy object
        del self.__ObjectRefCount[ObjectID];	#remove from ref-count table
        del self.__ObjectHash[ObjectID];		#remove from object hash

        self.Logger.debug("Object removed and destroyed");
        return(True);



    # ###
    # Attach a SymbolSlot To a MasterObject
    # MasterTreeAttachSymbolSlot(ParentID, Address, TypeName)
    #   - return ObjectID of Slot-Object or None on error...
    # ###
    def MasterTreeAttachSymbolSlot(self, ParentID, Address, TypeName, TimeOut=0.5):
        """
            This method will create and attach a new SymbolSlot to the
            ObjectTree...
        """
        fingerprint = Modules.Fingerprint(Name = '[SymbolSlot]', 
                                          Parent = ParentID, 
                                          Address = Address, 
                                          TypeName = TypeName,
                                          CacheTime = TimeOut);
        if self.__ObjectHash.has_key(fingerprint):
            Object = self.__ObjectHash[fingerprint];
            self.Logger.debug("Return cached Slot");
            c = self.__ObjectRefCount.get(Object._GetID());
            self.__ObjectRefCount.update( {Object._GetID():c+1} );
            return(Object._GetID());
        
        Parent = self.__ObjectHash.get(ParentID);
        if not Parent:
            self.Logger.error("Invalid Parent ID");
            return(None);
            
        Connection = Parent.connect(Address);
        if not Connection:
            self.Logger.error("Error while Connect parent");
            return(None);
        Connection._SetAddrStr(Address);
        
        Slot = pyDCPUSymbolSlot.MasterSlot(Connection, fingerprint, TypeName, self.Logger, TimeOut);
        if not Slot:
            self.Logger.error("Error while create Slot Object");
            return(None);

        if not self.__MasterObjTree.Add(ParentID,fingerprint):
            self.Logger.error("Error while add SlotObject To Tree...");
            return(None);

        self.__ObjectHash.update( {fingerprint:Slot} );
        self.__ObjectRefCount.update( {Slot._GetID():1} );
        return(fingerprint);
        
    def MasterTreeToXML(self,doc):
        """ This method create a xml.dom.minidom.Node with all
            object as subnodes in it """
        mtnode = doc.createElement("MasterTree");
        self.__MasterObjTree.ToXML(mtnode, doc, self);
        return(mtnode);
    def MasterTreeList(self, ParentID):
        """ This method will list all children of the obj [ParentID]... """
        return(self.__MasterObjTree.List(ParentID));
    



    # ######################################################################## #
    # Export Module handling                                                   # 
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #  
    #   +                                                                      # 
    # ######################################################################## #
    def ExporterAdd(self, ExportModule, Parameters, DefaultUser):
        """ This method load an export-module """
        
        fingerprint = Modules.Fingerprint(Name = ExportModule, 
                                          DefaultUser = DefaultUser, 
                                          Parameter = Parameters);
        if self.__ObjectHash.has_key(fingerprint):
            self.Logger.debug("Return cached object");
            Obj = self.__ObjectHash[fingerprint];
            c = self.__ObjectRefCount.get(Obj._GetID());
            self.__ObjectRefCount.update( {Obj._GetID():c+1} );
            return(Obj._GetID());

        ExpSymTree = ExportableSymbolTree.ExportableSymbolTree(self.__SymbolTree,
                                                               self.__UserDataBase,
                                                               DefaultUser);

        Obj = self.__ModuleManager.NewExporter(ExportModule, Parameters, fingerprint, ExpSymTree);
        if not Obj:
            self.Logger.error("Can't create object from %s"%ExportModule);
            return(None);

        self.Logger.debug("Export Module %s loaded as ID %s"%(ExportModule,Obj._GetID()));

        self.__ExporterList.append(Obj._GetID());

        self.__ObjectHash.update({Obj._GetID():Obj});
        self.__ObjectRefCount.update( {Obj._GetID():1} );
        self.Logger.debug("Object Added to Tree...");
        return(Obj._GetID());
        
       
    def ExporterDel(self, ObjectID):
        """ This method stop a export-module """
        Obj = self.__ObjectHash.get(ObjectID);
        if not Obj:
            self.Logger.error("No Object with id %s"%ObjectID);
            return(False);

        c = self.__ObjectRefCount.get(ObjectID);
        if c > 1:
            self.__ObjectRefCount.update( {ObjectID:c-1} );
            return(True);

        if not Obj.stop():
            self.Logger.error("Error while stop Object");
            return(False);

        del self.__ObjectHash[ObjectID];
        self.__ExporterList.remove(ObjectID);
        del self.__ObjectRefCount[ObjectID];
        return(True);
    
    def ExporterList(self):
        """ This method list all loaded export-modules """
        return(self.__ExporterList);
    
    def ExporterToXML(self, doc):
        self.Logger.error("Not implemented yet");
        return(None);    


    # ######################################################################## #
    # SymbolTreeHandler                                                        # 
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #  
    #   +                                                                      # 
    # ######################################################################## #
    def SymbolTreeCreateFolder(self, Path):
        """
            This method creates a new Folder with the Path 'Path'
            NOTE:
                All folders on the path to 'Path' must exist!
        """
        if not self.__SymbolTree.CreateFolder(Path):
            self.Logger.error("Error while create Folder(check path)");
            return(False);
        self.Logger.debug("Folder created");
        return(True);

    def SymbolTreeDeleteFolder(self,  Path):
        """ This method will delete folder Path """
        if not self.__SymbolTree.DeleteFolder(Path):
            self.Logger.error("Error while del folder %s"%Path);
            return(False);
        self.Logger.debug("Folder %s deleted"%Path);
        return(True);
    
    def SymbolTreeCreateSymbol(self, Path, SymbolSlotID):
        """
            This method create a new symbol in the symbol-tree with the slot
            of symbol-slot-ID.
        """
        Slot = self.__ObjectHash.get(SymbolSlotID);
        if not Slot:
            self.Logger.error("No Slot with this ID Found");
            return(False);
        if not self.__SymbolTree.CreateSymbol(Path, Slot):
            self.Logger.error("Error while create Symbol in SymbolTree");
            return(False);
        return(True);

    def SymbolTreeDeleteSymbol(self, Path):
        """ This method will del symbol Path """
        if not self.__SymbolTree.DeleteSymbol(Path):
            self.Logger.error("Unable to delete symbol %s"%Path);
            return(False);
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

    def SymbolTreeToXML(self, doc):        
        return(self.__SymbolTree.ToXML(doc));




    # ######################################################################## #
    # Return the instance know by ID (private)                                 # 
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #  
    #   + return the instance or None on error                                 #
    # ######################################################################## #
    def __GetObjectByID(self,ID):
        if not ID:
            self.Logger.error("No ID");
            return(None);
        self.Logger.debug("Search for %i"%ID);
        return(self.__ObjectHash.get(ID));





    # ######################################################################## #
    # Methods for User/Group handling                                          #
    # ######################################################################## #
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
    def ModInfoGetParOptList(self, ModName, ParaName):
        return(self.__ModuleManager.GetParameterOptionList(ModName, ParaName));
    def ModInfoIsParOptStrict(self, ModName, ParaName):
        return(self.__ModuleManager.GetParameterOptionStrict(ModName, ParaName));
    def ModInfoAddMod(self, ModName):
        return(self.__ModuleManager.AddModuleToDB(ModName));
            
    def ObjectToXML(self, doc, ID):
        """ This method is used by MasterObjTree to save a project """
        obj = self.__GetObjectByID(ID);
        if not obj:
            self.Logger.error("No Object with id %s"%str(ID));
            return(None);
        
        node = obj._ToXMLNode(doc);
        if not node:
            doc.unlink();
            self.Logger.error("Error while create XMLNode");
            return(None);
        return(node);
    
   
    # ######################################################################## #
    # Methods for object access                                                #
    # ######################################################################## #
	# will may be removed
    def GetAConnection(self, ObjectID, Address):
        """
            This method will return a connection object.
            NOTE: Please use this method only if you use pyDCPU as a
                    library.
        """
        Obj = self.__GetObjectByID(ObjectID);
        if not Obj:
            self.Logger.warning("no object found with this ID");
            return(None);
        return(Obj.connect(Address));

	# will be removed
    def GetObjectClass(self, ObjectID):
        Obj = self.__GetObjectByID(ObjectID);
        if not Obj:
            return(None);
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

    # ######################################################################## #
    # Methods to save the current system (Objects, SymbolTree) into XML        #
    # (obj, string or file)                                                    #
    # ######################################################################## #
    def SaveProjectToXML(self):
        """
            This method will return a xml.dom.minidom.Document object
            containing all information about the current system
            needed to rebuilt it later with the same facillities
        """
        dom = xml.dom.minidom.getDOMImplementation();
        doc = dom.createDocument(None, "Project", None);
        docnode = doc.documentElement;

        docnode.setAttribute('loglevel',self.__LoggingLevel);
        docnode.setAttribute('userdb',self.__UserDBFile);

        mat = self.MasterTreeToXML(doc);
        docnode.appendChild(mat);

        syt = self.SymbolTreeToXML(doc);
        docnode.appendChild(syt);
        return(doc);

    def SaveProjectToString(self):
        doc = self.SaveProjectToXML();
        return(doc.toprettyxml(indent='   ',encoding='utf-8'));

    def SaveProjectToFile(self, FileName):
        cont = self.SaveProjectToString();
        try:
            fp = open(FileName, 'w');
        except:
            self.Logger.error("Can't open/create file");
            return(False);
        fp.write(cont);
        fp.close();
        return(True);

