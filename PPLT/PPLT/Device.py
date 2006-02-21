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
# 2006-02-09:
#   * updated to new core-api and exceptions
# 2005-08-20:
#   - Fixed missing check for setup failure in Device.__init__()
# 2005-05-27:
#   Release as version 0.2.0
#   - Fixed bug in Device.unregister(): 
#       Generated inconsitent Object-Ref-Conter in Core.
    
import logging;
import pyDCPU;
import Setup;

class Device:
    def __init__(self, CoreObject, FileName, DeviceName, Parameters):
        """ This is the Device Object for the PPLT system. 
 It parse the given device-decription-file load all pyDCPU modules
 descibed."""
        #save core object
        self.__CoreObject = CoreObject;
        self.__DeviceName = DeviceName;
        self.__Parameters = Parameters;
        # get logger
        self.__Logger = logging.getLogger('PPLT');
 
        # load setupdescription from file...
        self.__Context = Setup.Context(self.__Parameters, self.__CoreObject)
        self.__Logger.debug("Load %s from %s"%(DeviceName, FileName));
        Setup.Setup(self.__Context, FileName);


    def destroy(self):
        """ This method will destroy a instance of this class """
        self.__Context.Unload();
        

    def GetIDByNameSpace(self, NameSpace):
        """ Will bind a Symbol to NameSpace::Address """
        # get deviceID by namespace:
        return self.__Context.GetObjByNameSpace(NameSpace);

    def getClassAndName(self):
        return(self.__DeviceName);
    def getParameters(self):
        return(self.__Parameters);
