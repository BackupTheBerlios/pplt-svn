#!/usr/bin/python
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

# ChangeLog:
#
#
#


import re;



RE_SLOT     = "^[a-z|A-Z|0-9|_|\-]+::[a-z|A-Z|0-9|_|\-]+::[a-z|A-Z|0-9|_|\-]+$";
RE_DEV_SRV  = "^[a-z|A-Z|0-9|_|\-]+\.([a-z|A-Z|0-9|_|\-]+\.)*[a-z|A-Z|0-9|_|\-]+$"
RE_USR_GRP  = "^[a-z|A-Z|0-9|_|\-]+$";
RE_PATH     = "^/[a-z|A-Z|0-9|_|\-]*(/[a-z|A-Z|0-9|_|\-]+)*$";


""" Internal used functions to check alias-, device- , server-, ..., -names. """ 

def CheckSlot(Name):
    exp = re.compile(RE_SLOT);
    Name = Name.strip();
    if not re.match(exp, Name):
        return(None);
    return(Name);

def CheckDevice(Name):
    exp = re.compile(RE_DEV_SRV);
    Name = Name.strip();
    if not re.match(exp, Name):
        return(None);
    return(Name);

def CheckServer(Name):
    return(CheckDevice(Name));

def CheckUser(Name):
    exp = re.compile(RE_USR_GRP);
    Name = Name.strip();
    if not re.match(exp, Name):
        return(None);
    return(Name);

def CheckGroup(Name):
    return(CheckUser(Name));

def CheckAlias(Name):
    return(CheckUser(Name));

def CheckPath(Name):
    exp = re.compile(RE_PATH);
    Name = Name.strip();                #remove whitespaces
    if len(Name)>1 and Name[-1]=='/':   #remove tailing slash
        Name = Name[:-1];
    if not re.match(exp, Name):
        return(None);
    return(Name);




if __name__ == "__main__":
    name = "/folder/";
    name = CheckPath(name);
    if not name:
        print "Invalid format.";
    else:
        print "Ok"
