# ########################################################################### #
# This is part of the PPLT project. PPLT is a framework for industrial        #
# communication.                                                              #
# Copyright (C) 2003-2005 Hannes Matuschek <hmatuschek@gmx.net>               #
#                                                                             #
# This library is free software; you can redistribute it and/or               #
# modify it under the terms of the GNU Lesser General Public                  #
# License as published by the Free Software Foundation; either                #
# version 2.1 of the License, or (at your option) any later version.          #
#                                                                             #
# This library is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU            #
# Lesser General Public License for more details.                             #
#                                                                             #
# You should have received a copy of the GNU Lesser General Public            #
# License along with this library; if not, write to the Free Software         #
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA   #
# ########################################################################### #


import logging;

class Version:
    def __init__(self, VerStr):
        self.__Logger = logging.getLogger("PPLT");
        self.__VersionString = VerStr;
        tmp = VerStr.split('.');
        self.__Version = [0, 0, 0];
#       self.__Logger.debug("Try to parse %s"%VerStr);
        #self.__PATCH  = 0;
        l = len(tmp);
        if l > 3: l = 3;
        for n in range(0,l):
            try:
                self.__Version[n] = int(tmp[n]);
            except:
                self.__Version[n] = 0;
#       self.__Logger.debug("Init verion %s"%hex(self));

    def GetMajor(self): return(self.__Version[0]);
    def GetMinor(self): return(self.__Version[1]);
    def GetBugFix(self): return(self.__Version[2]);
    def __int__(self):
        v = self.__Version[0];
        v = (v<<8)|self.__Version[1];
        v = (v<<8)|self.__Version[2];
        return(v);
    def __hex__(self): return(hex(self.__int__()));
    def __str__(self): return(self.__VersionString);
    def __eq__(self, other): return(int(self) == int(other));
    def __ne__(self, other): return(int(self) != int(other));
    def __cmp__(self, other): return(int(self)-int(other));

