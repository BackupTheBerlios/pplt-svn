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

import GSMUtils;
import pyDCPU;
import struct;
import xdrlib;



# Changelog:
# 2006-02-08:
#   Updated to new exceptions.



class GSMAddress:
    def __init__(self, Type, Value):
        self.__Type  = Type;
        self.__Value = Value;
    def GetType(self):
        return(self.__Type);
    def GetValue(self):
        return(self.__Value);
    
NETWORK         = 1
BATTERY         = 2;
QUALITY         = 3;
ERRORRATE       = 4;
MANUFACTURER    = 10;
MODEL           = 11;
SMS             = 20;
ADDRHASH        = {'network':NETWORK,
                   'battery':BATTERY,
                   'quality':QUALITY,
                   'errorrate':ERRORRATE,
                   'manufacturer':MANUFACTURER,
                   'model':MODEL};


class Object(pyDCPU.MasterObject):
    def setup(self): self.Logger.info("Setup GSM")


    def connect(self, AddrStr):
        if not AddrStr: raise pyDCPU.ModuleError("Need address for connection!");

        if AddrStr.find('sms:')==0:     #if addr-str begins with "sms:"
            tmp = AddrStr.split(':');
            if not len(tmp) == 2:
                raise pyDCPU.ModuleError("Invalid format: \"%s\" should be \"sms:0123456789\"!"%AddrStr);
            Addr = GSMAddress(SMS, tmp[1]);
            Con = pyDCPU.ValueConnection(self, pyDCPU.TString, Addr);
            self.Logger.debug("SMS destination: %s"%str(tmp[1]));
        elif ADDRHASH.has_key(AddrStr):
            Addr = GSMAddress(ADDRHASH[AddrStr],None);
            if Addr.GetType() in (NETWORK, BATTERY, QUALITY, ERRORRATE):
                Type = pyDCPU.TInteger;
            else: Type = pyDCPU.TString;
            Con = pyDCPU.ValueConnection(self, Type, Addr);
        else: raise pyDCPU.ModuleError("Invalid addrformat: \"%s\" ;look at the documentation."%AddrStr);
        return(Con);



    def read(self, Connection, Len=None):
        if Connection.Address.GetType() == BATTERY:
            return int(GSMUtils.GetBattery(self.Connection));
        elif Connection.Address.GetType() == NETWORK:
            s = GSMUtils.GetNetwork(self.Connection);
            if len(s)<2: raise pyDCPU.Error("Invalid format returned from device!");
            self.Logger.debug("Network status %s"%s[1]);
            return int(s[1]);
        elif Connection.Address.GetType() == QUALITY:
            s = GSMUtils.GetQuality(self.Connection);
            if len(s) != 2: raise pyDCPU.Error("Invalid format returned from deivce!");
            return int(s[0]);
        elif Connection.Address.GetType() == ERRORRATE:
            s = GSMUtils.GetQuality(self.Connection);
            if len(s) != 2: raise pyDCPU.Error("Invalid format returned form device!");
            return int(s[1]);
        elif Connection.Address.GetType() == MANUFACTURER:
            return GSMUtils.GetManufacturer(self.Connection);
        elif Connection.Address.GetType() == MODEL:
            return GSMUtils.GetModel(self.Connection);
        elif Connection.Address.GetType() == SMS:
            raise pyDCPU.AccessDenied("SMS can't be read! You can only send some!");
        raise pyDCPU.ItemNotFound("Ivalid chanel address \"%s\"!"%str(Connection.Address.GetType()));
        


    def write(self, Connection, Data):
        self.Logger.debug("Send sms...");
        if Connection.Address.GetType() == SMS:
            Dest = Connection.Address.GetValue();
            ret = GSMUtils.SendSMS(self.Connection, Dest, Data);
            return(len(Data));
        raise pyDCPU.ItemNotFound("Invalid chanel \"%s\"!"%str(Connection.Address.GetType()));
