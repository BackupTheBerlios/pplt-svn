# ############################################################################ #
# This is part of the PPLT project.                                            #
#                                                                              #
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



import struct;
from ModPPICalcFCS import *;
import string;

class ModPPISD2Packet:
    def __init__(self,Send,Recv,Data):
        SD2		= 104;				#0x68
        Len 	        = len(Data)+3;		
        SAddr 	        = Send;
        RAddr	        = Recv;
        FC		= 108;				#0x6C
        FCS		= ModPPICalcFCS(SAddr,RAddr,FC,Data);
        END		= 22;				#0x16
		
        FMT = "BBBBBBB%isBB" %(len(Data));
        self.Packet = struct.pack(FMT, SD2,Len,Len,SD2,RAddr,SAddr,FC,Data,FCS,END);
		
	
    def GetPacket(self):
        return(self.Packet);



class ModPPISD1Packet:
    def __init__(self,Send,Recv):
        SD1 = 16;
        SAddr = Send;
        RAddr = Recv;
        FC = 92;
        FCS = ModPPICalcFCS(SAddr,RAddr,FC,"");
        END = 22;

        FMT = "BBBBBB";
        self.Packet = struct.pack(FMT, SD1, SAddr, RAddr, FC, FCS, END);

    def GetPacket(self):
        return(self.Packet);
