# ############################################################################ #
# This is part of the pyDCPU project. pyDCPU is a framework for industrial     # 
#   communication.                                                             # 
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

# ChangeLog:
# 2005-08-28:
#   add moveing/renameing for folders. (need to be tested)
# 2005-08-26:
#   add moveing/renameing symbols feature.
# 2005-08-25:
#   - fixed bug in SymbolTree.SetPossesion() 
# 2005-05-27:
#   - bug in DeleteSymbol(): was unable to delete symbol from root

#FIXME:
#   - the symboltree have to have a owner,group and rights


import string;
import Symbol;
import SymbolTools;
import SymbolFolder;
import UserDB;
from Possession import Possession
import logging;

class SymbolTree(SymbolFolder.Folder):
    def __init__(self, DefaultUser, DefaultGroup, DefaultRights, UserDBObj):
        self.__DefaultUser = DefaultUser;
        self.__DefaultGroup = DefaultGroup;
        self.__DefaultRights= DefaultRights;
        self.Logger = logging.getLogger("pyDCPU");
        self.__UserDB = UserDBObj;
        self.__Name = "/";
        self.__Possession = Possession(self.__DefaultUser,
                                       self.__DefaultGroup,
                                       self.__DefaultRights,
                                       self.__UserDB);
        self.Logger.debug("Defalt user: %s;   default grp: %s;   default right: %i"%(self.__DefaultUser, self.__DefaultGroup, self.__DefaultRights));
        self.SymbolHash = {};
        self.FolderHash = {};




    def GetValue(self, PathToSymbol, SessionID):
        """ Returns the Value of the spec. Symbol in Type fromat.
            To control the access a SessionID is needed! """
        PathList = SymbolTools.SplitPath(PathToSymbol);
        Element = self.__GetElementByPath(PathList);
        if not isinstance(Element, Symbol.Symbol):
            return(False);
        return(Element.GetValue(SessionID));



    def SetValue(self, PathToSymbol, Value, SessionID):
        """ Write the value in Value into the symbol addressed by
            PathToSymbol """
        PathList = SymbolTools.SplitPath(PathToSymbol);
        Element = self.__GetElementByPath(PathList);
        if not isinstance(Element, Symbol.Symbol):
            self.Logger.error("%s doesn't exists!"%PathToSymbol);
            return(False);
        return(Element.SetValue(Value, SessionID));

    def CheckFolder(self, PathToFolder):
        """ Check if folder exists. """
        PathList = SymbolTools.SplitPath(PathToFolder);
        Element = self.__GetElementByPath(PathList);
        if not isinstance(Element, SymbolFolder.Folder):
            return(False);
        return(True);

    def CheckSymbol(self, PathToSymbol):
        """ Check if symbol exists. """
        PathList = SymbolTools.SplitPath(PathToSymbol);
        Element = self.__GetElementByPath(PathList);
        if not isinstance(Element, Symbol.Symbol):
            return(False);
        return(True);

    def ListFolders(self, PathToFolder, SessionID):
        """ List all folders in folder addressed by PathToFolder """
        if PathToFolder == '/':
            return(self.FolderHash.keys());

        PList = SymbolTools.SplitPath(PathToFolder);
        Element = self.__GetElementByPath(PList);
        if not isinstance(Element, SymbolFolder.Folder):
            return(None);
        return(Element.ListFolders(SessionID));


    def ListSymbols(self, PathToFolder, SessionID):
        """ List all symbols in folder addressed by PathToFolder """
        if PathToFolder == '/':
            return(self.SymbolHash.keys());
        PList = SymbolTools.SplitPath(PathToFolder);
        Element = self.__GetElementByPath(PList);
        if not isinstance(Element, SymbolFolder.Folder):
            return(None);
        return(Element.ListSymbols(SessionID));

    
    def GetTypeName(self, PathToSymbol, SessionID):
        """ Return the name of the original type of the source. """
        PList = SymbolTools.SplitPath(PathToSymbol);
        Element = self.__GetElementByPath(PList);
        print "Typename of (%s)%s"%(PathToSymbol,Element);
        if not isinstance(Element, Symbol.Symbol): return None;
        return Element.GetTypeName();

    def GetLastUpdate(self, PathToSymbol, SessionID):
        """ Return the timestamp of the symbol. """
        PList = SymbolTools.SplitPath(PathToSymbol);
        Element = self.__GetElementByPath(PList);
        if not isinstance(Element, Symbol.Symbol): return 0;
        return Element.GetLastUpdate();
         
    def GetQuality(self, PathToSymbol, SessionID):
        """ Returns the quality of the symbol. """
        PList = SymbolTools.SplitPath(PathToSymbol);
        Element = self.__GetElementByPath(PList);
        if not isinstance(Element, Symbol.Symbol): return None;
        return Element.GetQuality();

    #
    # The next methods are used by the CoreObject
    #


    def CreateFolder(self, PathToFolder):
        """ """
        PList = SymbolTools.SplitPath(PathToFolder);
        if len(PList) == 0:
            return(False);
        Name = PList[-1];

        Parent = self.__GetElementByPath(PList[:-1]);

        possession = Possession(self.__DefaultUser,
                                self.__DefaultGroup,
                                self.__DefaultRights,
                                self.__UserDB);

        newFolder = SymbolFolder.Folder(Name, possession);
        if not newFolder:
            self.Logger.error("Error while create Folder-Obj");
            return(False);

        if not Parent:
            self.AddFolder(Name,newFolder);
        else:
            if not Parent.AddFolder(Name, newFolder):
                self.Logger.error("Error while add folder");
                return(False);
        return(True);

    def MoveFolder(self, From, To):
        OPList = SymbolTools.SplitPath(From);
        OName  = OPList[-1];
        SPList = OPList[:-1];
        Src    = "/"+string.join(SPList,"/");
        NPList = SymbolTools.SplitPath(To);
        NName  = NPList[-1];
        DPList = NPList[:-1];
        Dest   = "/"+string.join(DPList,"/");

        #check if source exists:
        if not self.CheckFolder(From):
            self.Logger.error("Can't move folder %s: Folder doesn't exists."%From);
            return(False); 
        #check if destination is a symbol:
        if self.CheckSymbol(To):
            self.Logger.error("Can't move folder %s: %s already exists."%(From,To));
            return(False);
        #check if destination is a folder:
        if self.CheckFolder(To):    
            self.Logger.error("Can't move folder %s: %s already exists."%(From,To));
            return(False);

        #remove folder from source:
        folder_obj = self.__GetElementByPath(OPList);
        src_obj = self.__GetElementByPath(SPList);
        src_obj.RemoveFolder(OName);
        #check if dest-folder isn't in src-folder:
        if not self.CheckFolder(Dest):
            src_obj.AddFolder(OName, folder_obj);
            self.Logger.error("Can't move folder %s to %s!"%(From,To));
            return(None);
        #move folder
        dest_obj = self.__GetElementByPath(DPList);
        folder_obj.Rename(NName);
        dest_obj.AddFolder(NName, folder_obj);
        return(True);


    def DeleteFolder(self, PathToFolder):
        """ """
        PList = SymbolTools.SplitPath(PathToFolder);
        if len(PList)==0:
            return(False);

        Name = PList[-1];

        if len(PList) == 1:
            if not self.FolderHash.has_key(Name):
                return(False);
            if self.FolderHash[Name].IsEmpty():
                del self.FolderHash[Name];
                return(True);
            return(False);


        Parent = self.__GetElementByPath(PList[:-1]);

        if not Parent:
            return(False);
        if not Parent.DeleteFolder(Name):
            return(False);
        return(True);



    def CreateSymbol(self, PathToSymbol, Connection):
        """ Create a new Symbol """
        PList = SymbolTools.SplitPath(PathToSymbol);
        if len(PList) == 0:
            return(False);

        Name = PList[-1];
        
        if len(PList) == 1:
            # my self
            pass;
            
        Parent = self.__GetElementByPath(PList[:-1]);
        if not Parent:
            return(False);
        
        possession = Possession(self.__DefaultUser,
                                self.__DefaultGroup,
                                self.__DefaultRights,
                                self.__UserDB);

        newSymbol = Symbol.Symbol(Name,
                                  Connection,
                                  possession);
        
        if not newSymbol.IsValid():
            return(False);

        if Parent:
            if not Parent.AddSymbol(Name, newSymbol):
                return(False);
        else:
            if not self.AddSymbol(Name, newSymbol):
                return(False);
            
        return(True);


    def MoveSymbol(self, OldPath, NewPath):
        """ Move a symbol. """
        OPList = SymbolTools.SplitPath(OldPath);
        NPList = SymbolTools.SplitPath(NewPath);

        if len(OPList)<1 or len(NPList)<1:
            return(False);
        self.Logger.debug("Try to move symbol %s to %s"%(OldPath,NewPath));
        #check if source-symbol and destination-folder exists.
        if not self.CheckSymbol(OldPath):
            self.Logger.error("Movesymbol: Source doesn't exists.");
            return(False);
        if len(NPList)>1:
            NParent = self.__GetElementByPath(NPList[:-1]);
            if not isinstance(NParent, SymbolFolder.Folder):
                return(None);
            self.Logger.debug("Movesymbol: Destinationfolder is a folder.");
        #check if destinatino already exists
        if self.CheckSymbol(NewPath):
            self.Logger.error("Can't move symbol: Destination already exists (Symbol)");
            return(False);
        if self.CheckFolder(NewPath):
            self.Logger.error("Can't move symbol: Destination already exists (Folder)");
            return(False);

        #self.Logger.debug("Seems all ok for moving symbol.");

        OName = OPList[-1];
        NName = NPList[-1];
        
        #remove symbol from source folder
        if len(OPList) == 1:
            Symbol = self.SymbolHash.get(OName);
            if not Symbol:
                self.Logger.error("Symbol %s not found in my list."%OName);
                return(False);
            del self.SymbolHash[OName];
        else:
            Symbol = self.__GetElementByPath(OPList);
            if not isinstance(Symbol, Symbol.Symbol):
                self.Logger.error("Symbol %s not found."%OldPath);
                return(False);
            OParent = self.__GetElementByPath(OPList[:-1]);
            OParent.RemoveSymbol(OName);
        
        #add symbol to destination
        Symbol.Rename(NName);
        if len(NPList)==1:
            self.SymbolHash.update( {NName:Symbol} );
            return(True);
        if not NParent.AddSymbol(NName, Symbol):
            #if symbol could not added to new folder 
            #    ->move it back where it comes from.
            Symbol.Rename(OName);
            if len(OPList)==1:
                self.SymbolHash.update( {OName:Symbol} );
                return(False);
            OParent.AddSymbol(OName,Symbol);
            return(False);
        return(True);


    def DeleteSymbol(self, PathToSymbol):
        """ Delete a Symbol """
        PList = SymbolTools.SplitPath(PathToSymbol);
        if len(PList)==0:
            return(False);

        Name = PList[-1];

        if len(PList)==1:
            if self.SymbolHash.has_key(Name):
                self.SymbolHash[Name].Unregister();
                del self.SymbolHash[Name];
                return(True);
            return(False);
                
        Parent = self.__GetElementByPath(PList[:-1]);
            
        if not Parent:
            return(False);  # FIXME: ohoh..
        if not Parent.DeleteSymbol(Name):
            return(False);
        return(True);



    def SetPossession(self, PathToElement, User, Group, Permissions):
        """ Set the Possession to a folder or symbol """
        PList = SymbolTools.SplitPath(PathToElement);
        Element = self.__GetElementByPath(PList);
        if not Element:
            return(False);

        Possession = Possession(User,
                                Group,
                                Permissions,
                                self.__UserDB);
        if not Element.SetPossession(Possession):
            return(False);
        return(True);
        
    def GetPossession(self, PathToElement):
        PList = SymbolTools.SplitPath(PathToElement);
        Element = self.__GetElementByPath(PList);
        if not Element:
            return(None);
        return(Element.GetPossession());


    def GetOwnerName(self, Path):
        pos = self.GetPossession(Path);
        if not pos:
            return(None);
        return(pos.GetOwner());

    def SetOwnerName(self, Path, Name):
        pos = self.GetPossession(Path);
        if not pos:
            return(False);
        if not self.__UserDB.UserExists(Name):
            return(False);
        return(pos.chown(Name));
        
    def GetGroupName(self, Path):
        pos = self.GetPossession(Path);
        if not pos:
            return(None);
        return(pos.GetGroup());

    def SetGroupName(self, Path, Name):
        pos = self.GetPossession(Path);
        if not pos:
            return(False);
        if not self.__UserDB.GroupExists(Name):
            return(False);
        return(pos.chgrp(Name));

    def GetRightString(self, Path):
        pos = self.GetPossession(Path);
        if not pos:
            return(None);
        return(pos.GetRight());

    def SetRightString(self, Path, Right):
        pos = self.GetPossession(Path);
        if not pos:
            return(False);
        return(pos.chmod(Right));
    
    def __GetElementByPath(self, PathList):
        """ Get a element from tree by Path """
        #PathList = pyDCPUSymbolTools.SplitPath(PathToElement);

        if len(PathList)==0:
            return(self);
        if len(PathList)==1:
            if self.FolderHash.has_key(PathList[0]):
                return(self.FolderHash[PathList[0]]);
            elif self.SymbolHash.has_key(PathList[0]):
                return(self.SymbolHash[PathList[0]]);
            self.Logger.debug("Element \"%s\" not found."%PathList[0]);
            return(None);

        FList = PathList[:-1];
        Item  = PathList[-1];
        
        PFolder = self;
        for folder in FList:
            SFolder = PFolder.FolderHash.get(folder);
            if not SFolder:
                self.Logger.debug("Can't find subfolder %s\n"%folder);
                return(None);
            PFolder = SFolder;

        if SFolder.FolderHash.has_key(Item):
            return(SFolder.FolderHash.get(Item));
        elif SFolder.SymbolHash.has_key(Item):
            return(SFolder.SymbolHash.get(Item));
        self.Logger.debug("Symbol/Folder \"%s\" not found"%Item);
        return(None);



    def ToXML(self, Document):
        Node = Document.createElement("SymbolTree");
        
        #Node.setAttribute("own",str(self.__Possession.GetOwner()));
        #Node.setAttribute("grp",str(self.__Possession.GetGroup()));
        #Node.setAttribute("mod",str(self.__Possession.GetRight()));

        for folder in self.FolderHash.values():
            subnode = folder.ToXML(Document);
            Node.appendChild(subnode);
        for symbol in self.SymbolHash.values():
            subnode = symbol.ToXML(Document);
            Node.appendChild(subnode);
        return(Node);
