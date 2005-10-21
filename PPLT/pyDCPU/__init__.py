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

__author__  = 'Hannes Matuschek <hmatuschek@gmx.net>'
__status__  = 'beta'
__version__ = '0.9.0'
__date__    = '2005-08-28'

VERSION = 0x000900;              # this version-number is used internal to check
                                 # if a module fit in this system.

#
# Definition of types:
#
TBool = "Bool";
TInteger = "Integer";
TUnsignedInteger = "uInteger";
TLong = "Long";
TUnsignedLong = "uLong";
TFloat = "Float";
TDouble = "Double";
TString = "String";
TArrayOfBool = "ArrayBool";
TArrayOfInteger = "ArrayInteger";
TArrayOfUnsignedInteger = "ArrayuInteger";
TArrayOfLong = "ArrayLong";
TArrayOfUnsignedLong = "ArrayuLong";
TArrayOfFloat = "ArrayFloat";
TArrayOfDouble = "ArrayDouble";
TArrayOfString = "ArrayString";
TRaw = "Raw"



from Exceptions import *;
from pyDCPUCore import *;
from pyDCPUSymbolTree import *
from MasterObject import *;
from pyDCPUExportObject import *;
from ExportableSymbolTree import *;
from pyDCPUConverter import *;
