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


import string;

class Possession:
    def __init__(self, UserName, GroupName, RightsString, UserDB):
        self.__OwnerName = UserName;
        self.__GroupName = GroupName;
        self.__RightString = RightsString;
        (self.__OwnerRight,
         self.__GroupRight,
         self.__AnyRight) = SplitRights(RightsString);
        self.__UserDB    = UserDB;


    def GetOwner(self):
        return(self.__OwnerName);
    def GetGroup(self):
        return(self.__GroupName);
    def GetRight(self):
        return(self.__RightString);
    
    def CanRead(self, SessionID):
        if self.__UserDB.IsSystemSession(SessionID):
            return(True);

        sesUser = self.__UserDB.SessionGetUserName(SessionID);
        if not sesUser:
            return(False);

        if sesUser == self.__OwnerName:
            return(self.__OwnerRight.read());
        elif self.__UserDB.IsMemberOf(self.__GroupName, sesUser):
            return(self.__GroupRight.read());
        else:
            return(self.__AnyRight.read());
        return(False);
    
    def CanWrite(self, SessionID):
        if self.__UserDB.IsSystemSession(SessionID):
            return(True);

        sesUser = self.__UserDB.SessionGetUserName(SessionID);
        if not sesUser:
            return(False);

        if sesUser == self.__OwnerName:
            return(self.__OwnerRight.write());
        elif self.__UserDB.IsMemeberOf(self.__GroupName, sesUser):
            return(self.__GroupRight.write());
        else:
            return(self.__AnyRight.write());
        return(False);

    def CanExecute(self, SessionID):
        if self.__UserDB.IsSystemSession(SessionID):
            return(True);

        sesUser = self.__UserDB.SessionGetUserName(SessionID);
        if not sesUser:
            return(False);

        if sesUser == self.__OwnerName:
            return(self.__OwnerRight.execute());
        elif self.__UserDB.IsMemeberOf(self.__GroupName, sesUser):
            return(self.__GroupRight.execute());
        else:
            return(self.__AnyRight.execute());
        return(False);


    def chown(self, newOwner):
        self.__OwnerName = newOwner;
        return(True);
    def chgrp(self, newGroup):
        self.__GroupName = newGroup;
        return(True);
    def chmod(self, RightsString):
        self.__RightString = RightsString;
        (self.__OwnerRight,
         self.__GroupRight,
         self.__AnyRight) = SplitRights(RightsString);
        return(True);
    
    def copy(self):
        return(copy.copy(self));



class Rights:
    def __init__(self, Right = 0):
        self.__read = Right & 0x01;
        self.__write = (Right>>1)&0x01;
        self.__execute = (Right>>2)&0x01;
        
    def read(self):
        return(self.__read);
    def write(self):
        return(self.__write);
    def execute(self):
        return(self.__execute);
    def SetRight(self, Right):
        self.__read = Right & 0x01;
        self.__write = (Right>>1)&0x01;
        self.__execute = (Right>>2)&0x01;
        return(True);



def SplitRights(RightString):
    Owner = Rights();
    Group = Rights();
    Any   = Rights();
    
    if not len(RightString)==3:
        return((Owner, Group, Any));

    OwnerR = string.atoi(RightString[0]);
    GroupR = string.atoi(RightString[1]);
    AnyR   = string.atoi(RightString[2]);

    Owner.SetRight(OwnerR);
    Group.SetRight(GroupR);
    Any.SetRight(AnyR);
    return( (Owner, Group, Any) );
