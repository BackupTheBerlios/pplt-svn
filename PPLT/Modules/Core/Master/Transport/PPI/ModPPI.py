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


import pyDCPU;
from ModPPIPacket import *;
from ModPPICalcFCS import *;
import string;

class Object(pyDCPU.MasterObject):
    def setup(self):
        self.__myAddress = self.Parameters.get('Address');
        self.Logger.info("Setup ModPPI");
        
        if not self.__myAddress: raise pyDCPU.ModuleSetup("No PPI address given!");

        self.PPIAddress = int(self.__myAddress);
        return(True);
        
    def read(self, Connection, Len=None):
        RetryCount = 0;
        while RetryCount<3:
            try: return PPIRead(self.Connection, Connection.Address, self.PPIAddress, Len, self.Logger);
            except pyDCPU.ModuleError, e:
                self.Logger.debug("Error while read from parent: %s [%i retrys left]"%(str(e),3-RetryCount));
                self.Connection.flush();
                RetryCount +=1;
        raise e;    # if no retrys left -> reraise exception!
    
    def write(self, Connection, Data):
        RetryCount = 0;
        while RetryCount<3:
            try: return PPIWrite(self.Connection, Connection.Address, self.PPIAddress, Data, self.Logger);
            except pyDCPU.ModuleError, e:
                self.Logger.debug("Error while write to parent: %s [%i retrys left]"%(str(e), 3-RetryCount));
                self.Connection.flush();
                RetryCount +=1;
        raise e;    # if no retrys left -> reraise exception!

    def connect(self,Address):
        if not Address: raise pyDCPU.ModuleError("My child needs a address");
        return pyDCPU.SequenceConnection(self,int(Address));
	
    def close(self):
        self.Logger.debug("closed");
        pass;

    def flush(self):
        self.Logger.debug("Flushing parent");
        self.Connection.flush();
        self.unlock();
        return(True);




def PPIWrite(Connection, Dest, Src, Data, Logger):
		
    #
    # Check Length
    #
    if len(Data) > 256-3:
        Logger.warning("Data to long to send. This is a weak of the Programmer. Mail him!");
        return(None);
		
    #
    # Assamble Packet...
    #
    Packet = ModPPISD2Packet(Src, Dest, Data);
    Mesg = Packet.GetPacket();
		
    #
    # Write Packet...
    #
    Logger.debug("Send Packet");
    Connection.write(Mesg);
    
    #
    # Read Back Reception-Ack
    #
    ACK = Connection.read(1);
    
    #
    # Check Ack
    #
    if len(ACK) == 1: 
        if ord(ACK[0]) == 229: return(len(Data));
    raise pyDCPU.ModuleError("Transmission Error...(at ACK)(%x != e5)"%ord(ACK[0]));

def PPIRead(Connection, Src, Dest, Len, Logger):

    SD1Pack = ModPPISD1Packet(Src,Dest);
    Packet = SD1Pack.GetPacket();
        
    Connection.write(Packet);

    Logger.debug("SD1 Send...");

    
    PPIHead = Connection.read(7);
    
    if len(PPIHead) != 7: raise pyDCPU.ModuleError("Bad packed!");

    if ord(PPIHead[1]) != ord(PPIHead[2]): raise pyDCPU.ModuleError("Realy bad packet!");

    DataLen = ord(PPIHead[1]);
    Logger.debug("Got %i Octs data..."%(DataLen-3));

    if ord(PPIHead[4]) != Dest: raise pyDCPU.ModuleError("BUS error.(packet for %i recived...)"%ord(PPIHead[4]));

    if ord(PPIHead[5]) != Src: raise pyDCPU.ModuleError("BUS error. (packet from %i recived...)"%ord(PPIHead[5]));

    if ord(PPIHead[6]) != 8: raise pyDCPU.ModuleError("Bad FCS (%x)"%ord(PPIHead[6]));

    Data  = Connection.read(DataLen-3);
    
    if len(Data) != DataLen-3: raise pyDCPU.ModuleError("Invalid DataLen (read error)");

    Footer = Connection.read(2);
    
    if len(Footer) != 2: raise pyDCPU.ModuleError("Invalid FooterLen (read error)");

    FCS = ModPPICalcFCS(ord(PPIHead[4]),ord(PPIHead[5]),ord(PPIHead[6]),Data);
    if ord(Footer[0]) != FCS: raise pyDCPU.ModuleError("Transmisstion error (Bad FCS)");
    return(Data);
