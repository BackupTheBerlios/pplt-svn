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

import logging;
import string;

class Possession:
    def __init__(self, UserName, GroupName, Right, UserDB):
        self.__OwnerName = UserName;         # save username
        self.__GroupName = GroupName;        # save groupname
        self.__Right = Right;                # save rights-number
        (self.__OwnerRight,
         self.__GroupRight,
         self.__AnyRight) = SplitRights(Right);    # split the number into objects
        self.__UserDB    = UserDB;           # the user-db
        self.__Logger    = logging.getLogger('pyDCPU');
        rtmp = self.__OwnerRight.ToString();
        rtmp+= self.__GroupRight.ToString();
        rtmp+= self.__AnyRight.ToString();
        self.__Logger.debug("New possession: %s %s %s(%i)"%(self.__OwnerName, self.__GroupName, rtmp,Right));


    def GetOwner(self):
        return(self.__OwnerName);
    def GetGroup(self):
        return(self.__GroupName);
    def GetRight(self):
        return(self.__Right);

    def CanRead(self, SessionID):
        if self.__UserDB.IsSystemSession(SessionID):
            self.__Logger.debug("SystemSession: Access OK");
            return(True);

        sesUser = self.__UserDB.SessionGetUserName(SessionID);
        if not sesUser:
            self.__Logger.debug("No Username for session %s"%SessionID);
            return(False);
        self.__Logger.debug("Session of %s"%sesUser);

        if self.__UserDB.IsSuperUser(sesUser):
            self.__Logger.debug("SuperUserSession: Access OK");
            return(True);

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
        
        if self.__UserDB.IsSuperUser(sesUser):
            return(True);

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
    def chmod(self, Right):
        self.__Right = Right;
        (self.__OwnerRight,
         self.__GroupRight,
         self.__AnyRight) = SplitRights(Right);
        return(True);

    def copy(self):
        return(copy.copy(self));



class Rights:
    def __init__(self, Right = 0):
        self.__execute = Right & 0x01;
        self.__write   = (Right>>1) & 0x01;
        self.__read    = (Right>>2) & 0x01;


    def read(self):
        return(self.__read);
    def write(self):
        return(self.__write);
    def execute(self):
        return(self.__execute);
    def SetRight(self, Right):
        self.__read    = (Right >> 2) & 0x01;
        self.__write   = (Right >> 1) & 0x01;
        self.__execute = Right & 0x01;
        return(True);
    def ToString(self):
        tmp = "";
        if self.__read: tmp += "r";
        else: tmp+="-";
        if self.__write: tmp+= "w";
        else: tmp +="-";
        if self.__execute: tmp+="x";
        else: tmp += "-";
        return(tmp);


def SplitRights(Right):
    Owner = Rights();
    Group = Rights();
    Any   = Rights();
    
#    print "Any  : 0x%x"%(Right&0x07);
#    print "Group: 0x%x"%((Right>>3)&0x07);
#    print "Owner: 0x%x"%((Right>>6)&0x07);

    Any.SetRight(Right & 0x7);
    Group.SetRight((Right >> 3) & 0x7);
    Owner.SetRight((Right >> 6) & 0x7);

    return( (Owner, Group, Any) );
