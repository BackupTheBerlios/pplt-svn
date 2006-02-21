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


# ChangeLog:
# 2005-08-28:
#   add move/rename folders.
# 2005-08-26:
#   add moveing/renameing symbols feature.
# 2005-08-25:
#   fixed ident error in Folder.DeleteSymbol(Folder.DeleteSymbol())
import SymbolTools;
import Symbol;
import Exceptions;


class Folder:
    """
        Hold Floders and Symbols
    """
    def __init__(self, Name, Possession):
        self.Name       = Name;
        self.Possession = Possession;
        self.FolderHash = {};
        self.SymbolHash = {};


    def Rename(self, Name): self.Name = Name;

    def ListSymbols(self, SessionID):
        if not self.Possession.CanRead(SessionID):
            raise Exceptions.AccessDenied("Session (%s) is not allowed to read from this folder."%SessionID);
        return(self.SymbolHash.keys());
    def ListFolders(self, SessionID):
        if not self.Possession.CanRead(SessionID):
            raise Exceptions.AccessDenied("Session (%s) is not allowed to read from this folder."%SessionID);
        return(self.FolderHash.keys());

    def IsEmpty(self):
        if len(self.SymbolHash.keys()) == 0 and len(self.FolderHash.keys()) == 0:
            return(True);
        return(False);

    
    def AddSymbol(self, Name, Symb):
        if self.FolderHash.has_key(Name) or self.SymbolHash.has_key(Name):
            raise Exceptions.ItemBusy("There is allready a folder or symbol named \"%s\"."%Name);
        if not isinstance(Symb, Symbol.Symbol):
            raise Exceptions.Error("Oops: Given instance is not a symbol! (%s)"%type(Symb));
        
        self.SymbolHash.update( {Name:Symb} );
        
    def RemoveSymbol(self, Name):
        if self.SymbolHash.has_key(Name):
            del self.SymbolHash[Name];
            return;
        raise Exceptions.ItemNotFound("There is no symbol named \"%s\" in this folder."%Name);

    def DeleteSymbol(self, Name):
        if self.SymbolHash.has_key(Name):
            self.SymbolHash[Name].Unregister();
            del self.SymbolHash[Name];
            return;
        raise Exceptions.ItemNotFound("There is no symbol named \"%s\" in this folder."%Name);


    def AddFolder(self, Name, FolderObj):
        if self.FolderHash.has_key(Name) or self.SymbolHash.has_key(Name):
            raise Exceptions.ItemBusy("There is allready a folder or symbol named \"%s\"."%Name);
        if not isinstance(FolderObj, Folder):
            raise Exceptions.Error("Oops: Given instance is not a symbol! (%s)"%type(Symb));
        self.FolderHash.update( {Name: FolderObj} );

    def RemoveFolder(self, Name):
        if self.FolderHash.has_key(Name):
            del self.FolderHash[Name];
            return(True);
        raise Exceptions.ItemNotFound("There is no symbol named \"%s\" in this folder."%Name);

    def DeleteFolder(self, Name):
        if not self.FolderHash.has_key(Name):
            raise Exceptions.ItemNotFound("There is no symbol named \"%s\" in this folder."%Name);
        if not self.FolderHash[Name].IsEmpty():
            raise Exceptions.ItemBusy("Unable to remove the folder: is not empty!");
        del self.FolderHash[Name];


    def GetElementByPath(self, PathToElement):
        """ Get a element from tree by Path """
        (Item, Path) = SymbolTools.PopItemFromPath(PathToElement);
        
        if Item and not Path:
            if self.SymbolHash.has_key(Item):
                return(self.SymbolHash.get(Item));
            elif self.FolderHash.has_key(Item):
                return(self.FolderHash.get(Item));
            else: raise Exceptions.ItemNotFound("No symbol or folder named \"%s\" found!"%Item);
        elif Item and Path:
            if self.FolderHash.has_key(Item):
                return(self.FolderHash[Item].GetElementByPath(Path));
            else: raise Exceptions.ItemNotFound("No folder named \"%s\" found!"%Item);
        raise Exceptions.Error("Ooops!");


    def SetPossession(self, Possession): self.Possession = Possession;

    def GetPossession(self): return(self.Possession);


