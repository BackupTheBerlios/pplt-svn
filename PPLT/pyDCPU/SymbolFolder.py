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



class Folder:
    """
        Hold Floders and Symbols
    """
    def __init__(self, Name, Possession):
        self.Name       = Name;
        self.Possession = Possession;
        self.FolderHash = {};
        self.SymbolHash = {};


    def Rename(self, Name):
        self.Name = Name;
        return(True);

    def ListSymbols(self, SessionID):
        if not self.Possession.CanRead(SessionID):
            return(None);
        return(self.SymbolHash.keys());
    def ListFolders(self, SessionID):
        if not self.Possession.CanRead(SessionID):
            return(None);
        return(self.FolderHash.keys());

    def IsEmpty(self):
        if len(self.SymbolHash.keys()) == 0 and len(self.FolderHash.keys()) == 0:
            return(True);
        return(False);

    
    def AddSymbol(self, Name, Symb):
        if self.FolderHash.has_key(Name) or self.SymbolHash.has_key(Name):
            return(False);
        if not isinstance(Symb, Symbol.Symbol):
            return(False);
        
        self.SymbolHash.update( {Name:Symb} );
        return(True);
        
    def RemoveSymbol(self, Name):
        if self.SymbolHash.has_key(Name):
            del self.SymbolHash[Name];
            return(True);
        return(False);

    def DeleteSymbol(self, Name):
        if self.SymbolHash.has_key(Name):
            self.SymbolHash[Name].Unregister();
            del self.SymbolHash[Name];
            return(True);
        return(False);


    def AddFolder(self, Name, FolderObj):
        if self.FolderHash.has_key(Name) or self.SymbolHash.has_key(Name):
            return(False);
        if not isinstance(FolderObj, Folder):
            return(None);
        self.FolderHash.update( {Name: FolderObj} );
        return(True);

    def RemoveFolder(self, Name):
        if self.FolderHash.has_key(Name):
            del self.FolderHash[Name];
            return(True);
        return(False);

    def DeleteFolder(self, Name):
        if not self.FolderHash.has_key(Name):
            return(False);
        if not self.FolderHash[Name].IsEmpty():
            return(False);
        del self.FolderHash[Name];
        return(True);


    def GetElementByPath(self, PathToElement):
        """ Get a element from tree by Path """
        (Item, Path) = SymbolTools.PopItemFromPath(PathToElement);
        
        if Item and not Path:
            if self.SymbolHash.has_key(Item):
                return(self.SymbolHash.get(Item));
            elif self.FolderHash.has_key(Item):
                return(self.FolderHash.get(Item));
            else:
                return(None);
        elif Item and Path:
            if self.FolderHash.has_key(Item):
                return(self.FolderHash[Item].GetElementByPath(Path));
            else:
                return(None);
        else:
            return(None);
        return(None);



    def SetPossession(self, Possession):
        self.Possession = Possession;
        return(True);

    def GetPossession(self):
        return(self.Possession);


