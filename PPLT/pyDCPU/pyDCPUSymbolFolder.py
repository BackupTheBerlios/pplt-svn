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


import pyDCPUSymbolTools;
import pyDCPUSymbol;



class Folder:
    """
        Hold Floders and Symbols
    """
    def __init__(self, Name, Possession):
        self.Name       = Name;
        self.Possession = Possession;
        self.FolderHash = {};
        self.SymbolHash = {};



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

    
    def AddSymbol(self, Name, Symbol):
        if self.FolderHash.has_key(Name) or self.SymbolHash.has_key(Name):
            return(False);
        if not isinstance(Symbol, pyDCPUSymbol.Symbol):
            return(False);
        
        self.SymbolHash.update( {Name:Symbol} );
        return(True);
        
    def DeleteSymbol(self, Name):
        if self.SymbolHash.has_key(Name):
	    self.SymbolHash[Name].Unregister();
            del self.SymbolHash[Name];
            return(True);



    def AddFolder(self, Name, FolderObj):
        if self.FolderHash.has_key(Name) or self.SymbolHash.has_key(Name):
            return(False);
        if not isinstance(FolderObj, Folder):
            return(None);
        self.FolderHash.update( {Name: FolderObj} );
        return(True);

    def DeleteFolder(self, Name):
        if not self.FolderHash.has_key(Name):
            return(False);
        if not self.FolderHash[Name].IsEmpty():
            return(False);
        del self.FolderHash[Name];
        return(True);

    

    def GetElementByPath(self, PathToElement):
        """ Get a element from tree by Path """
        (Item, Path) = pyDCPUSymbolTools.PopItemFromPath(PathToElement);
        
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

    def ToXML(self, Document):
        Node = Document.createElement("Folder");
        
        Node.setAttribute("name",self.Name);
        Node.setAttribute("own",str(self.Possession.GetOwner()));
        Node.setAttribute("grp",str(self.Possession.GetGroup()));
        Node.setAttribute("mod",str(self.Possession.GetRight()));

        for folder in self.FolderHash.values():
            subnode = folder.ToXML(Document);
            Node.appendChild(subnode);
        for symbol in self.SymbolHash.values():
            subnode = symbol.ToXML(Document);
            Node.appendChild(subnode);

        return(Node);
