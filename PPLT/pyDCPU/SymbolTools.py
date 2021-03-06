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


def SplitPath(Path):
    """Split the give Path into FolderPath and Name"""

    tmp = Path.split('/');
    PList = [];
    for item in tmp:
        if item != '':
            PList.append(item);
    return(PList);


def PopItemFromPath(Path):
    tmp = string.split(Path,'/',1);
    if tmp[0] == '' and len(tmp) == 2:
        tmp = string.split(tmp[1], '/', 1);
        
    if len(tmp) == 1:
        return( (tmp[0], None) );
    elif len(tmp) == 2:
        return( (tmp[0], tmp[1]) );
    else:
        return( (None, None) );


def NormPath(Path):
    nPath = "/";
    PList = SplitPath(Path);
    return (nPath+string.join(PList,"/"));
