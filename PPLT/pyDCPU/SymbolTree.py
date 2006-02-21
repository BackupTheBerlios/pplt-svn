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
import Exceptions;
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
            raise Exceptions.ItemNotFound("Symbol %s not found!"%PathToSymbol);
        return(Element.GetValue(SessionID));



    def SetValue(self, PathToSymbol, Value, SessionID):
        """ Write the value in Value into the symbol addressed by
            PathToSymbol """
        PathList = SymbolTools.SplitPath(PathToSymbol);
        Element = self.__GetElementByPath(PathList);
        if not isinstance(Element, Symbol.Symbol):
            raise Exceptions.ItemNotFound("Symbol %s not found!"%PathToSymbol);
        return(Element.SetValue(Value, SessionID));

    def Read(self, PathToSymbol, Length, SessionID):
        """ Read from symbol (for stream an sequence symbols) """
        PathList = SymbolTools.SplitPath(PathToSymbol);
        Element = self.__GetElementByPath(PathList);
        if not isinstance(Element, Symbol.Symbol):
            raise Exceptions.ItemNotFound("Symbol %s not found!"%PathToSymbol);
        return(Element.Read(Length, SessionID));

    def Write(self, PathToSymbol, Data, SessionID):
        """ Read from symbol (for stream an sequence symbols) """
        PathList = SymbolTools.SplitPath(PathToSymbol);
        Element = self.__GetElementByPath(PathList);
        if not isinstance(Element, Symbol.Symbol):
            raise Exceptions.ItemNotFound("Symbol %s not found!"%PathToSymbol);
        return(Element.Write(Data, SessionID));

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
            raise Exceptions.ItemNotFound("%s is not a folder or doesn't exists!"%PathToFolder);
        return(Element.ListFolders(SessionID));


    def ListSymbols(self, PathToFolder, SessionID):
        """ List all symbols in folder addressed by PathToFolder """
        if PathToFolder == '/':
            return(self.SymbolHash.keys());
        PList = SymbolTools.SplitPath(PathToFolder);
        Element = self.__GetElementByPath(PList);
        if not isinstance(Element, SymbolFolder.Folder):
            raise Exceptions.ItemNotFound("%s is not a folder or doesn't exists!"%PathToFolder);
        return(Element.ListSymbols(SessionID));

    
    def GetTypeName(self, PathToSymbol, SessionID):
        """ Return the name of the original type of the source. """
        PList = SymbolTools.SplitPath(PathToSymbol);
        Element = self.__GetElementByPath(PList);
        if not isinstance(Element, Symbol.Symbol):
            raise Exceptions.ItemNotFound("%s is not a symbol or doesn't exists!"%PathToSymbol);
        return Element.GetTypeName();

    def GetLastUpdate(self, PathToSymbol, SessionID):
        """ Return the timestamp of the symbol. """
        PList = SymbolTools.SplitPath(PathToSymbol);
        Element = self.__GetElementByPath(PList);
        if not isinstance(Element, Symbol.Symbol):
            raise Exceptions.ItemNotFound("%s is not a symbol or doesn't exists!"%PathToSymbol);
        return Element.GetLastUpdate();
         
    def GetQuality(self, PathToSymbol, SessionID):
        """ Returns the quality of the symbol. """
        PList = SymbolTools.SplitPath(PathToSymbol);
        Element = self.__GetElementByPath(PList);
        if not isinstance(Element, Symbol.Symbol): 
            raise Exceptions.ItemNotFound("%s is not a symbol or doesn't exists!"%PathToSymbol);
        return Element.GetQuality();

    #
    # The next methods are used by the CoreObject
    #


    def CreateFolder(self, PathToFolder):
        """ """
        PList = SymbolTools.SplitPath(PathToFolder);
        if len(PList) == 0: raise Exceptions.SymbolError("Can't create folder at %s"%PathToFolder);
        Name = PList[-1];

        Parent = self.__GetElementByPath(PList[:-1]);

        possession = Possession(self.__DefaultUser,
                                self.__DefaultGroup,
                                self.__DefaultRights,
                                self.__UserDB);

        newFolder = SymbolFolder.Folder(Name, possession);

        if not Parent:
            self.AddFolder(Name,newFolder);
        else: Parent.AddFolder(Name, newFolder);

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
            raise Exceptions.ItemNotFound("Can't move folder %s to %s: source doesn't exists!"%(From,To));
        #check if destination is a symbol:
        if self.CheckSymbol(To):
            raise Exceptions.SymbolError("Can't move folder %s to %s: destination allready exists!"%(From,To));

        #remove folder from source:
        folder_obj = self.__GetElementByPath(OPList);
        src_obj = self.__GetElementByPath(SPList);
        src_obj.RemoveFolder(OName);
        #check if dest-folder isn't in src-folder:
        if not self.CheckFolder(Dest):
            src_obj.AddFolder(OName, folder_obj);
            raise Exceptions.SymbolError("Can't move folder %s to %s: destination is part of the source!"%(From,To));
        #move folder
        dest_obj = self.__GetElementByPath(DPList);
        folder_obj.Rename(NName);
        dest_obj.AddFolder(NName, folder_obj);


    def DeleteFolder(self, PathToFolder):
        """ """
        PList = SymbolTools.SplitPath(PathToFolder);
        if len(PList)==0: raise Exceptions.SymbolError("Can't delete folder \"%s\"!"%PathToFolder);

        Name = PList[-1];

        if len(PList) == 1:
            if not self.FolderHash.has_key(Name):
                raise Exceptions.ItemNotFound("Can't delete folder %s: Folder not found!"%PathToFolder);
            if self.FolderHash[Name].IsEmpty():
                del self.FolderHash[Name];
                return;
            raise Exceptions.ItemBusy("Can't delete folder %s: folder not empty!"%PathToFolder);    

        Parent = self.__GetElementByPath(PList[:-1]);

        if not Parent:
            raise Exceptions.ItemNotFound("Can't delete folder %s: not found!"%PathToFolder);
        Parent.DeleteFolder(Name);



    def CreateSymbol(self, PathToSymbol, Connection, Address, Timeout):
        """ Create a new Symbol """
        PList = SymbolTools.SplitPath(PathToSymbol);
        if len(PList) == 0: raise Exceptions.SymbolError("Unable to create symbol %s!"%PathToSymbol);

        Name = PList[-1];
        
        if len(PList) == 1:
            # my self
            pass;
            
        Parent = self.__GetElementByPath(PList[:-1]);
        if not Parent:
            raise Exceptions.ItemNotFound("Unable to create symbol %s: Folder not found!"%PathToSymbol);
        
        possession = Possession(self.__DefaultUser,
                                self.__DefaultGroup,
                                self.__DefaultRights,
                                self.__UserDB);

        newSymbol = Symbol.Symbol(Name,
                                  Connection,
                                  Address,
                                  Timeout,
                                  possession);
        
        if Parent: Parent.AddSymbol(Name, newSymbol);
        else: self.AddSymbol(Name, newSymbol);
            


    def MoveSymbol(self, OldPath, NewPath):
        """ Move a symbol. """
        OPList = SymbolTools.SplitPath(OldPath);
        NPList = SymbolTools.SplitPath(NewPath);

        if len(OPList)<1 or len(NPList)<1:
            raise Exceptions.ItemNotFound("Unable to move symbol %s to %s!"%(OldPath, NewPath));
        self.Logger.debug("Try to move symbol %s to %s"%(OldPath,NewPath));
        #check if source-symbol and destination-folder exists.
        if not self.CheckSymbol(OldPath):
            raise Exceptions.ItemNotFound("Can't move symbol %s to %s: source doesn't exists!"%(OldPath,NewPath));
        if len(NPList)>1:
            NParent = self.__GetElementByPath(NPList[:-1]);
            if not isinstance(NParent, SymbolFolder.Folder):
                raise Exceptions.ItemNotFound("Can't move symbols %s to %s: destiantion not found!"%(OldPath,NewPath));
            self.Logger.debug("Movesymbol: Destinationfolder is a folder.");
        #check if destinatino already exists
        if self.CheckSymbol(NewPath): 
            raise Exceptions.ItemNotFound("Can't move symbol %s to %s: destination allready exists!"%(OldPath,NewPath));
        if self.CheckFolder(NewPath):
            raise Exceptions.ItemNotFound("Can't move symbol %s to %s: destination allready exists!"%(OldPath,NewPath));

        #self.Logger.debug("Seems all ok for moving symbol.");

        OName = OPList[-1];
        NName = NPList[-1];
        
        #remove symbol from source folder
        if len(OPList) == 1:
            SymbolObj = self.SymbolHash.get(OName);
            if not SymbolObj:
                raise Exceptions.ItemNotFound("Can't move symbol %s to %s: source not found!"%(OldPath,NewPath));
            del self.SymbolHash[OName];
        else:
            SymbolObj = self.__GetElementByPath(OPList);
            if not isinstance(SymbolObj, Symbol.Symbol):
                raise Exceptions.ItemNotFound("Can't move symbol %s to %s: Source not found!"%(OldPath,NewPath));
            OParent = self.__GetElementByPath(OPList[:-1]);
            OParent.RemoveSymbol(OName);
        
        #add symbol to destination
        SymbolObj.Rename(NName);
        if len(NPList)==1:
            self.SymbolHash.update( {NName:SymbolObj} );
            return;
        try: NParent.AddSymbol(NName, SymbolObj);
        except Exception, e:
            #if symbol could not added to new folder 
            #    ->move it back where it comes from.
            SymbolObj.Rename(OName);
            if len(OPList)==1:
                self.SymbolHash.update( {OName:SymbolObj} );
                raise Exceptions.Error("Can't add symbol %s to new folder: Mail author! (%s)"%(OldPath, str(e)));
            OParent.AddSymbol(OName,SymbolObj);
            raise Exceptions.Error("Can't add symbol %s to new folder: Mail author! (%s)"%(OldPath, str(e)));


    def DeleteSymbol(self, PathToSymbol):
        """ Delete a Symbol """
        PList = SymbolTools.SplitPath(PathToSymbol);
        if len(PList)==0: raise Exceptions.ItemNotFound("Can't delete folder %s: item not found!"%PathToSymbol);

        Name = PList[-1];

        if len(PList)==1:
            if self.SymbolHash.has_key(Name):
                self.SymbolHash[Name].Unregister();
                del self.SymbolHash[Name];
                return;
            raise Exceptions.ItemNotFound("Can't delete symbol %s: item not found!"%PathToSymbol);
                
        Parent = self.__GetElementByPath(PList[:-1]);
            
        if not Parent:
            raise Exceptions.ItemNotFound("Can't delete symbol %s: Symbol not found!"%PathToSymbol);
        Parent.DeleteSymbol(Name);


    def SetSymbolRefresh(self, PathToSymbol, Refresh):
        """ Resets the refresh-rate of the symbol! """
        PList = SymbolTools.SplitPath(PathToSymbol);
        if len(PList) == 0:
            raise Exceptions.ItemNotFound("Can't set refresh-rate of \"%s\": symbol not found!"%PathToSymbol);
        Name = PList[-1];

        if len(PList)==1:
            if self.SymbolHash.has_key(Name):
                return self.SymbolHash[Name].SetRefresh(Refresh);
            raise Exceptions.ItemNotFound("Can't set refresh-rate of symbol %s: item not found!"%PathToSymbol);
                
        Symbol = self.__GetElementByPath(PList);
        if not Symbol: raise pyDCPU.ItemNotFound("Can't set refresh-rate for \"%s\": Symbol not found."%PathToSymbol);
        Symbol.SetRefresh(Refresh);
    
    
    def GetSymbolRefresh(self, PathToSymbol):
        """ Returns the refresh-rate of the given symbol! """
        PList = SymbolTools.SplitPath(PathToSymbol);
        if len(PList) == 0:
            raise Exceptions.ItemNotFound("Can't get refresh-rate of \"%s\": symbol not found!"%PathToSymbol);
        Name = PList[-1];

        if len(PList)==1:
            if self.SymbolHash.has_key(Name):
                return self.SymbolHash[Name].GetRefresh();
            raise Exceptions.ItemNotFound("Can't can't get refresh-rate for \"%s\": item not found!"%PathToSymbol);
                
        Symbol = self.__GetElementByPath(PList);
        if not Symbol: raise pyDCPU.ItemNotFound("Can't get refresh-rate for \"%s\": Symbol not found."%PathToSymbol);
        return Symbol.GetRefresh();
 

    def SetPossession(self, PathToElement, User, Group, Permissions):
        """ Set the Possession to a folder or symbol """
        PList = SymbolTools.SplitPath(PathToElement);
        Element = self.__GetElementByPath(PList);
        if not Element: raise Exceptions.ItemNotFound("Can't find item %s!"%PathToElement);

        Possession = Possession(User,
                                Group,
                                Permissions,
                                self.__UserDB);
        Element.SetPossession(Possession);
        
    def GetPossession(self, PathToElement):
        PList = SymbolTools.SplitPath(PathToElement);
        Element = self.__GetElementByPath(PList);
        if not Element: raise Exceptions.ItemNotFound("Can't find %s!"%PathToElement);
        return(Element.GetPossession());


    def GetOwnerName(self, Path):
        pos = self.GetPossession(Path);
        if not pos: raise Exceptions.ItemNotFound("Can't find %s!"%Path);
        return(pos.GetOwner());

    def SetOwnerName(self, Path, Name):
        pos = self.GetPossession(Path);
        if not pos: raise Exceptions.ItemNotFound("Can't find %s!"%Path);
        if not self.__UserDB.UserExists(Name):
            raise Exceptions.ItemNotFound("Owner (%s) of %s not in user-db!"%(Name,Path));
        pos.chown(Name);

    def GetGroupName(self, Path):
        pos = self.GetPossession(Path);
        if not pos: raise Exceptions.ItemNotFound("Can't find %s!"%Path);
        return(pos.GetGroup());

    def SetGroupName(self, Path, Name):
        pos = self.GetPossession(Path);
        if not pos: raise Exceptions.ItemNotFound("Can't find %s!"%Path);
        if not self.__UserDB.GroupExists(Name):
            raise Exceptions.ItemNotFound("Group %s not in user-db!"%Name);
        pos.chgrp(Name);
        
    def GetRightString(self, Path):
        pos = self.GetPossession(Path);
        if not pos: raise Exceptions.ItemNotFound("Can't find %s!"%Path);
        return(pos.GetRight());

    def SetRightString(self, Path, Right):
        pos = self.GetPossession(Path);
        if not pos: raise Exceptions.ItemNotFound("Can't find %s!"%Path);
        self.Logger.debug("set modus to %s(%s)."%(Right,type(Right)));
        #modus = int(Right,8);
        pos.chmod(Right);

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
            return None;

        FList = PathList[:-1];
        Item  = PathList[-1];
        
        PFolder = self;
        for folder in FList:
            SFolder = PFolder.FolderHash.get(folder);
            if not SFolder:
                return None; 
            PFolder = SFolder;

        if SFolder.FolderHash.has_key(Item):
            return(SFolder.FolderHash.get(Item));
        elif SFolder.SymbolHash.has_key(Item):
            return(SFolder.SymbolHash.get(Item));
        return None;




