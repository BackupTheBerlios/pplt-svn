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

#FIXME:
#   + Unable to delete Symbol from ROOT
#


import string;
import pyDCPUSymbol;
import pyDCPUSymbolTools;
import pyDCPUSymbolFolder;
import UserDB;


class SymbolTree(pyDCPUSymbolFolder.Folder):
    def __init__(self, DefaultUser, DefaultGroup, DefaultRights, UserDBObj, Logger):
        self.__DefaultUser = DefaultUser;
        self.__DefaultGroup = DefaultGroup;
        self.__DefaultRights= DefaultRights;
        self.Logger = Logger;
        self.__UserDB = UserDBObj;
        self.__Name = "/";
        self.__Possession = UserDB.Possession(self.__DefaultUser,
                                                self.__DefaultGroup,
                                                self.__DefaultRights,
                                                self.__UserDB);
        self.SymbolHash = {};
        self.FolderHash = {};




    def GetValue(self, PathToSymbol, SessionID):
        """ Returns the Value of the spec. Symbol in Type fromat.
            To control the access a SessionID is needed! """
        PathList = pyDCPUSymbolTools.SplitPath(PathToSymbol);
        Element = self.__GetElementByPath(PathList);
        if not isinstance(Element, pyDCPUSymbol.Symbol):
            return(False);
        return(Element.GetValue(SessionID));


    
    def SetValue(self, PathToSymbol, Value, SessionID):
        """ Write the value in Value into the symbol addressed by
            PathToSymbol """
        PathList = pyDCPUSymbolTools.SplitPath(PathToSymbol);
        Element = self.__GetElementByPath(PathList);
        if not isinstance(Element, pyDCPUSymbol.Symbol):
            return(False);
        return(Element.SetValue(Value, SessionID));

    

    def ListFolders(self, PathToFolder, SessionID):
        """ List all folders in folder addressed by PathToFolder """
        if PathToFolder == '/':
            return(self.FolderHash.keys());

        PList = pyDCPUSymbolTools.SplitPath(PathToFolder);        
        Element = self.__GetElementByPath(PList);
        if not isinstance(Element, pyDCPUSymbolFolder.Folder):
            return(None);
        return(Element.ListFolders(SessionID));


    def ListSymbols(self, PathToFolder, SessionID):
        """ List all symbols in folder addressed by PathToFolder """
        if PathToFolder == '/':
            return(self.SymbolHash.keys());
        PList = pyDCPUSymbolTools.SplitPath(PathToFolder);        
        Element = self.__GetElementByPath(PList);
        if not isinstance(Element, pyDCPUSymbolFolder.Folder):
            return(None);
        return(Element.ListSymbols(SessionID));



    #
    # The next methods are used by the CoreObject
    # (you would need the SystemSessionID to exec)
    #
    
    
    def CreateFolder(self, PathToFolder):
        """ """
        PList = pyDCPUSymbolTools.SplitPath(PathToFolder);
        if len(PList) == 0:
            return(False);
        Name = PList[-1];
        
        Parent = self.__GetElementByPath(PList[:-1]);

        Possession = UserDB.Possession(self.__DefaultUser,
                                                self.__DefaultGroup,
                                                self.__DefaultRights,
                                                self.__UserDB);

        newFolder = pyDCPUSymbolFolder.Folder(Name, Possession);
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



    def DeleteFolder(self, PathToFolder):
        """ """
        PList = pyDCPUSymbolTools.SplitPath(PathToFolder);
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



    def CreateSymbol(self, PathToSymbol, SymbolSlot, Type):
        """ Create a new Symbol """
        PList = pyDCPUSymbolTools.SplitPath(PathToSymbol);
        if len(PList) == 0:
            return(False);

        Name = PList[-1];
        
        if len(PList) == 1:
            # my self
            pass;
            
        Parent = self.__GetElementByPath(PList[:-1]);
        if not Parent:
            return(False);
        
        Possession = UserDB.Possession(self.__DefaultUser,
                                                 self.__DefaultGroup,
                                                 self.__DefaultRights,
                                                 self.__UserDB);

        newSymbol = pyDCPUSymbol.Symbol(Name,
                                        SymbolSlot,
                                        Type,
                                        Possession,
                                        self.Logger);
        
        if not newSymbol.IsValid():
            return(False);

        if Parent:
            if not Parent.AddSymbol(Name, newSymbol):
                return(False);
        else:
            if not self.AddSymbol(Name, newSymbol):
                return(False);
            
        return(True);



    def DeleteSymbol(self, PathToSymbol):
        """ Delete a Symbol """
        PList = pyDCPUSymbolTools.SplitPath(PathToSymbol);
        if len(PList)==0:
            return(False);

        Name = PList[-1];

        if len(PList)==1:
            if self.SymbolHash.has_key(Name):
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
        PList = pyDCPUSymbolTools.SplitPath(PathToElement);
        Element = self.__GetElementByPath(PList);
        if not Element:
            return(False);

        Possession = UserDBPossession(self.__User,
                                      self.__Group,
                                      self.__permissions,
                                      self.__UserDB);
        if not Element.SetPossession(Possession):
            return(False);
        return(True);
        
    def GetPossession(self, PathToElement):
        PList = pyDCPUSymbolTools.SplitPath(PathToElement);
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
            self.Logger.warning("Element \"%s\" not found."%PathList[0]);
            return(None);

        FList = PathList[:-1];
        Item  = PathList[-1];
        
        PFolder = self;
        for folder in FList:
            SFolder = PFolder.FolderHash.get(folder);
            if not SFolder:
                self.Logger.warning("Can't find subfolder %s\n"%folder);
                return(None);
            PFolder = SFolder;

        if SFolder.FolderHash.has_key(Item):
            return(SFolder.FolderHash.get(Item));
        elif SFolder.SymbolHash.has_key(Item):
            return(SFolder.SymbolHash.get(Item));
        self.Logger.warning("Symbol/Folder \"%s\" not found"%Item);
        return(None);



    def ToXML(self, Document):
        Node = Document.createElement("SymbolTree");
        
        Node.setAttribute("own",str(self.__Possession.GetOwner()));
        Node.setAttribute("grp",str(self.__Possession.GetGroup()));
        Node.setAttribute("mod",str(self.__Possession.GetRight()));

        for folder in self.FolderHash.values():
            subnode = folder.ToXML(Document);
            Node.appendChild(subnode);
        for symbol in self.SymbolHash.values():
            subnode = symbol.ToXML(Document);
            Node.appendChild(subnode);

        return(Node);
