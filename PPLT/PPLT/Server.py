# ############################################################################ #
# This is part of the PPLT project. PPLT is a framework for industrial         # 
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
# 2005-08-20:
#   - fixed missin check if server load fails @ Server.__init__() 
# 2005-05-27:
#   - fixed bug in Server.__load():
#       missed to remove stop exsisting Core-Exporter on exception while load a new
#   - fixed bug in Server.destroy():
#       method is now error-sensitiv        
#   - fixed missing exception raise in Server.__init__() if server load fails.
import logging;
import Setup


class Server:
    def __init__(self, CoreObject, FileName, ServerName, DefaultUser, Parameters, Root="/"):
        """This is the class for pplt-server"""
        self.__Logger = logging.getLogger('PPLT');
        self.__CoreObject = CoreObject;
        self.__ServerName = ServerName;
        self.__DefaultUser = DefaultUser;
        self.__Parameters = Parameters;
        self.__Root = Root;
        self.__Context = Setup.Context(Parameters, CoreObject, DefaultUser, Root);
        Setup.Setup(self.__Context, FileName);

    
    def destroy(self):
        self.__Context.Unload();
        return(True);

    def getClassAndName(self):
        return(self.__ServerName);
    def getDefaultUser(self):
        return(self.__DefaultUser);
    def getParameters(self):
        return(self.__Parameters);
    def getRoot(self):
        return(self.__Root);
