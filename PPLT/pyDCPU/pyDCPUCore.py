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

import xml.dom.minidom;
import pyDCPUCoreLogging;
import UserDB;
import Modules;
import pyDCPUSymbolSlot;
import pyDCPUSymbolTree;
import pyDCPUObjectTree;
import ExportableSymbolTree;
import Exceptions;

#import sys;
import os;
import thread;



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
    def __init__(self, ModuleDBFile=None,
                 UserDBFile=None,
                 LogLevel='info',
                 LogFile = None,
                 SysLog = False):
        
        """ This Function will set the Runtime-Options """
        # Save Parameter
        self.__UserDBFile = UserDBFile;
        self.__LoggingLevel = LogLevel;
        self.__LoggingFile  = LogFile;
        self.__IsSysLogging = SysLog;
        self.__ModuleDBFile = ModuleDBFile;
        
        # Setup Logging...
        self.Logger = pyDCPUCoreLogging.SetupLogger(self.__LoggingLevel,
                                                    self.__LoggingFile,
                                                    self.__IsSysLogging);

        # Load user/group database
        self.__UserDataBase = UserDB.UserDB(self.Logger, self.__UserDBFile);
        
#        self.__ExportList      = [];   
        
        # Hash of all created Objects
        self.__ObjectHash      = {};   

        self.Logger.debug("Load modulemanager");
        self.__ModuleManager = Modules.Importer(ModuleDBFile,self.Logger);
        self.Logger.debug("all modules loaded");

        #Setup Trees: 
        self.__MasterObjTree = pyDCPUObjectTree.pyObjectTree(self.Logger);
        self.__MasterTreeChangeID = 0;

        self.__SymbolTree    = pyDCPUSymbolTree.SymbolTree(self.__UserDataBase.GetSuperUser(),  
                                                           self.__UserDataBase.GetSuperUserGrp(),
                                                           '710',
                                                           self.__UserDataBase,
                                                           self.Logger);
        self.__SymbolTreeChangeID = 0;

        self.__ExporterList  = [];
        self.__ExporterChangeID = 0;
        
 
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


        Object = self.__ModuleManager.NewMaster(ModName, Connection, Parameter);
        if not Object:
            self.Logger.error("Error while create Object");
            return(None);

        self.Logger.debug("Obj from %s with ID:%i created"%(ModName,Object._GetID()));
               
        if not self.__MasterObjTree.Add(ParentID,Object._GetID()):
            self.Logger.error("Can't add Object...");
            Object.destroy();
            del Object;
            return(None);

        self.__ObjectHash.update({Object._GetID():Object});
        self.Logger.debug("Object Added to Tree...");

        self.__UpdateMasterTreeChangeID();
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
            self.Logger.error("No Object with ID %i"%ObjectID);
            return(False);

        if not self.__MasterObjTree.Del(ObjectID):
            self.Logger.error("Error while del Object from tree");
            return(False);

        if not Object.destroy():
            self.Logger.error("Error while delete object %i"%ObjectID);
            return(False);
        del Object;
        self.Logger.debug("Object removed and destroyed");

        self.__UpdateMasterTreeChangeID();
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
        Parent = self.__ObjectHash.get(ParentID);
        if not Parent:
            self.Logger.error("Invalid Parent ID");
            return(None);

        Connection = Parent.connect(Address);
        if not Connection:
            self.Logger.error("Error while Connect parent");
            return(None);
        Connection._SetAddrStr(Address);
        
        SlotID = self.__ModuleManager.NewID();
        if not SlotID:
            self.Logger.error("Can't create a new ID for SlotObj...");
            return(None);
        
        Slot = pyDCPUSymbolSlot.MasterSlot(Connection, SlotID, TypeName, self.Logger, TimeOut);
        if not Slot:
            self.Logger.error("Error while create Slot Object");
            return(None);

        if not self.__MasterObjTree.Add(ParentID,SlotID):
            self.Logger.error("Error while add SlotObject To Tree...");
            return(None);

        self.__ObjectHash.update( {SlotID:Slot} );
        
        self.__UpdateMasterTreeChangeID();
        
        return(SlotID);
        
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

        ExpSymTree = ExportableSymbolTree.ExportableSymbolTree(self.__SymbolTree,
                                                               self.__UserDataBase,
                                                               DefaultUser);

        Obj = self.__ModuleManager.NewExporter(ExportModule, Parameters, ExpSymTree);
        if not Obj:
            self.Logger.error("Can't create object from %s"%ExportModule);
            return(None);

        self.Logger.debug("Export Module %s loaded as ID %i"%(ExportModule,Obj._GetID()));

        self.__ExporterList.append(Obj._GetID());

        self.__ObjectHash.update({Obj._GetID():Obj});
        self.Logger.debug("Object Added to Tree...");

#        self.__UpdateMasterTreeChangeID();
        return(Obj._GetID());
        
       
    def ExporterDel(self, ObjectID):
        """ This method stop a export-module """
        Obj = self.__ObjectHash.get(ObjectID);
        if not Obj:
            self.Logger.error("No Object with id %i"%ObjectID);
            return(False);
        if not Obj.stop():
            self.Logger.error("Error while stop Object");
            return(False);
        del self.__ObjectHash[ObjectID];
        self.__ExporterList.remove(ObjectID);
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
    
    def SymbolTreeCreateSymbol(self, Path, SymbolSlotID, TypeName):
        """
            This method create a new symbol in the symbol-tree with the slot
            of symbol-slot-ID.
        """
        Slot = self.__ObjectHash.get(SymbolSlotID);
        if not Slot:
            self.Logger.error("No Slot with this ID Found");
            return(False);
        if not self.__SymbolTree.CreateSymbol(Path, Slot, TypeName):
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
    def SymbolTreeListFolder(self, Path):
        return(self.__SymbolTree.ListFolders(Path, self.__GetSystemSession()));

    def SymbolTreeGetOwner(self, Path):
        return(self.__SymbolTree.GetOwnerName(Path));
    def SymbolTreeSetOwner(self, Path, Name):
        return(self.__SymbolTree.SetOwnerName(Path, Name));
    def SymbolTreeGetGroup(self, Path):
        return(self.__SymbolTree.GetGroupName(Path));
    def SymbolTreeSetGroup(self, Path, Name):
        return(self.__SymbolTree.SetGroupName(Path, Name));
    def SymbolTreeGetRight(self, Path):
        return(self.__SymbolTree.GetRightString(Path));
    def SymbolTreeSetRight(self, Path, Right):
        return(self.__SymbolTree.SetRightString(Path, Right));
    
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
    # Methods to provide information about the state of module trees           #
    # ######################################################################## #
    def MasterTreeChangeID(self):
        """
            This method returns a ID that indicates if the master tree
            has been changed.
        """
        return(self.__MasterTreeChangeID);

    def __UpdateMasterTreeChangeID(self):
        """
            This (private) method creates a new MasterTreeChangeID
        """
        self.__MasterTreeChangeID += 1;
        return(None);
    

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

    def GetObjectClass(self, ObjectID):
        Obj = self.__GetObjectByID(ObjectID);
        if not Obj:
            return(None);
        return(Obj._GetClass());



    def GetExportableSymbolTree(self, DefaultUser):
        return(ExportableSymbolTree.ExportableSymbolTree(self.__SymbolTree,
                                                         self.__UserDataBase,
                                                         DefaultUser));

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
        docnode.setAttribute('moduledb',self.__ModuleDBFile);

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
            file = open(FileName, 'w');
        except:
            self.Logger.error("Can't open/create file");
            return(False);
        file.write(cont);
        file.close();
        return(True);

