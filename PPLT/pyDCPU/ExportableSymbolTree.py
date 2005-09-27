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


#ChangeLog:
# 2005-06-25:
#   - fixed bad symbol-path translation in
#       ExportableSybolTree.SetValue():62
# 2005-06-04:
#   + Add function Normpath()
#   + Add variable root item, means that 
#       you can now export parts of the 
#       symboltree

import pyDCPU;
import pyDCPU.UserDB;
import logging;
import string;

class ExportableSymbolTree:
    def __init__(self, SymbolTree, UserDB, DefaultUser, Root = '/'):
        self.__Logger = logging.getLogger('pyDCPU');

        if not isinstance(SymbolTree, pyDCPU.SymbolTree):
            raise pyDCPU.Error;
        if not isinstance(UserDB, pyDCPU.UserDB.UserDB):
            raise pyDCPU.Error;

        self.__SymbolTree = SymbolTree;
        self.__UserDB = UserDB;
        self.__DefaultSession = UserDB.GetSession(DefaultUser);
        self.__Root = Root;


    def Logon(self, UserName, Password):
        return(self.__UserDB.Logon(UserName, Password));

    def Logoff(self, SessionID):
        return(self.__UserDB.Logoff(SessionID));

    def GetValue(self, SymbolPath, SessionID):
        Path = Normpath(self.__Root+"/"+SymbolPath);
        if not SessionID:
            SessionID = self.__DefaultSession;
        return(self.__SymbolTree.GetValue(Path,SessionID));

    def SetValue(self, SymbolPath, Value, SessionID):
        Path = Normpath(self.__Root+"/"+SymbolPath);
        if not SessionID:
            SessionID = self.__DefaultSession;
        return(self.__SymbolTree.SetValue(Path, Value, SessionID));

    def ListFolders(self, PathToFolder, SessionID):
        Path = Normpath(self.__Root+"/"+PathToFolder);
        if not SessionID:
            SessionID = self.__DefaultSession;
        return(self.__SymbolTree.ListFolders(Path, SessionID));

    def ListSymbols(self, PathToFolder, SessionID):
        Path = Normpath(self.__Root+"/"+PathToFolder);
        if not SessionID:
            SessionID = self.__DefaultSession;
        return(self.__SymbolTree.ListSymbols(Path, SessionID));

    def GetLastUpdate(self, PathToSymbol, SessionID):
        Path = Normpath(self.__Root+"/"+PathToSymbol);
        if not SessionID: SessionID = self.__DefaultSession;
        return self.__SymbolTree.ListSymbols(Path, SessionID);

    def GetTypeName(self, PathToSymbol, SessionID):
        Path = Normpath(self.__Root+"/"+PathToSymbol);
        if not SessionID: SessionID = self.__DefaultSession;
        return self.__SymbolTree.GetTypeName(Path, SessionID);

def Normpath(Path):
    tmp = Path.split('/');
    ntmp = []
    for item in tmp:
        if item != '':
            ntmp.append(item);
    return("/"+string.join(ntmp,"/"));
