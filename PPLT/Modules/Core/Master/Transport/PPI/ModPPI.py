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
        
        if not self.__myAddress:
            self.Logger.warning("No Address");
            return(False);
        self.PPIAddress = int(self.__myAddress);
        return(True);
        
    def read(self, Connection, Len):
        RetryCount = 0;
        while RetryCount<3:
            Ret = PPIRead(self.Connection, Connection.Address, self.PPIAddress, Len, self.Logger);
            if Ret:
                return(Ret);
            self.Logger.error("Error while read from parent: flush & retry (%i retrys left)"%(3-RetryCount));
            self.Connection.flush();
            RetryCount +=1;
        self.Logger.error("3 Errors: Connection broken???");
        raise(pyDCPU.IOModError);
    
    def write(self, Connection, Data):
        RetryCount = 0;
        while RetryCount<3:
            Ret = PPIWrite(self.Connection, Connection.Address, self.PPIAddress, Data, self.Logger);
            if Ret:
                return(Ret);
            self.Logger.error("Error while write to parent: flush & retry (%i retrys left)"%(3-RetryCount));
            self.Connection.flush();
            RetryCount +=1;
        self.Logger.error("3 Errors: Connection broken???");
        raise(pyDCPU.IOModError);

    def connect(self,Address):
        if not Address:
            self.Logger.error("my child needs a address");
            return(None);
        Connection = pyDCPU.SequenceConnection(self,int(Address));
        return(Connection);
	
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
    try:
        Connection.write(Mesg);
    except:
        Logger.error("Error while write to BUS");
        return(None);
    
    #
    # Read Back Reception-Ack
    #
    try:
        ACK = Connection.read(1);
    except:
        Logger.error("BUSIO Error: flushing bus");
        return(None);
    
    if not ACK:
        Logger.warning("Error while read from parent");
        return(None);
    
    #
    # Check Ack
    #
    if len(ACK) == 1:
        if ord(ACK[0]) == 229:
            return(len(Data));
        else:
            Logger.warning("Transmission Error...(at ACK)(%x != e5)"%ord(ACK[0]));
            return(None);
    else:
        Logger.warning("Error while read...");
        return(None);
    return(None);


def PPIRead(Connection, Src, Dest, Len, Logger):

    SD1Pack = ModPPISD1Packet(Src,Dest);
    Packet = SD1Pack.GetPacket();
        
    if Connection.write(Packet) != len(Packet):
        Logger.warning("Error while send SD1");
        return(None);

    Logger.debug("SD1 Send...");

    try:
        PPIHead = Connection.read(7);
    except:
        Logger.error("IO Error");
        return(None);
    
    if len(PPIHead) != 7:
        Logger.warning("Error while get PPI-Packet-Header");
        return(None);

    if ord(PPIHead[1]) != ord(PPIHead[2]):
        Logger.warning("Transmission error...");
        #FIXME: wait for some bytes and then:
        return(None);

    DataLen = ord(PPIHead[1]);
    Logger.debug("Got %i Octs data..."%(DataLen-3));

    if ord(PPIHead[4]) != Dest:
        Logger.warning("BUS error.(packet for %i recived...)"%ord(PPIHead[4]));
        return(None);

    if ord(PPIHead[5]) != Src:
        Logger.warining("BUS error. (packet from %i recived...)"%ord(PPIHead[5]));
        return(None);

    if ord(PPIHead[6]) != 8:
        Logger.warning("Bad FCS (%x)"%ord(PPIHead[6]));
        return(None);

    try:
        Data  = Connection.read(DataLen-3);
    except:
        Logger.warning("Error while read from Parent");
        return(None);
    
    if len(Data) != DataLen-3:
        Logger.warning("Invalid DataLen (read error)");
        return(None);

    try:
        Footer = Connection.read(2);
    except:
        Logger.warning("Error while read from Parent");
        return(None);
    
    if len(Footer) != 2:
        Logger.warning("Invalid FooterLen (read error)");
        return(None);

    FCS = ModPPICalcFCS(ord(PPIHead[4]),ord(PPIHead[5]),ord(PPIHead[6]),Data);
    if ord(Footer[0]) != FCS:
        Logger.warning("Transmisstion error (Bad FCS)");
        return(None);
    
    return(Data);
