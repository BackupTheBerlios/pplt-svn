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


import pyDCPU;
import pyDCPU.UserDB;
import logging;

class ExportableSymbolTree:
    def __init__(self, SymbolTree, UserDB, DefaultUser):
        self.__Logger = logging.getLogger('pyDCPU');
        
        if not isinstance(SymbolTree, pyDCPU.SymbolTree):
            raise pyDCPU.Error;
        if not isinstance(UserDB, pyDCPU.UserDB.UserDB):
            raise pyDCPU.Error;
            
        self.__SymbolTree = SymbolTree;
        self.__UserDB = UserDB;
        self.__DefaultSession = UserDB.GetSession(DefaultUser);
        


    def Logon(self, UserName, Password):
        return(self.__UserDB.Logon(UserName, Password));

    def Logoff(self, SessionID):
        return(self.__UserDB.Logoff(SessionID));

    def GetValue(self, SymbolPath, SessionID):
        if not SessionID:
            SessionID = self.__DefaultSession;
        return(self.__SymbolTree.GetValue(SymbolPath,SessionID));

    def SetValue(self, SymbolPath, Value, SessionID):
        if not SessionID:
            SessionID = self.__DefaultSession;        
        return(self.__SymbolTree.SetValue(SymbolPath, Value, SessionID));

    def ListFolders(self, PathToFolder, SessionID):
        if not SessionID:
            SessionID = self.__DefaultSession;
        return(self.__SymbolTree.ListFolders(PathToFolder, SessionID));

    def ListSymbols(self, PathToFolder, SessionID):
        if not SessionID:
            SessionID = self.__DefaultSession;
        return(self.__SymbolTree.ListSymbols(PathToFolder, SessionID));
