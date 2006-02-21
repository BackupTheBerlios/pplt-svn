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



import GSMSMS;
import logging;
import readline;



# Changelog:
# 2006-02-08:
#   updated to new exceptions.



def Reset(Con):
    Con.flush();
    Con.write("ATZ\r\n");
    readline.read(Con,"\r\n");
    readline.read(Con,"\r\n");
    if readline.read(Con,"\r\n") == 'OK': return(Con.flush());
    raise pyDCPU.ModuleError("Unable to reset mobile-phone.");

def GetServiceCenter(Con):
    Con.flush();
    Con.write('AT+CSCA?\r\n');
    readline.read(Con,"\r\n");          # get echo ...
    tmp = readline.read(Con,"\r\n");
    if tmp == 'ERROR': raise pyDCPU.ModuleError("Mobile-phone returned ERROR.");
    readline.read(Con,"\r\n");          # read empty line
    if not readline.read(Con,"\r\n") == 'OK':
        raise pyDCPU.ModuleError("Mobile-phone returned ERROR.");
    if -1 == tmp.find('"'): raise pyDCPU.ModuleError("Mad format returned by mobile-phone!");
    sc = tmp.split('"')[1];
    return("\"%s\""%sc);

def GetManufacturer(Con):
    Con.write('AT+CGMI\r\n');
    readline.read(Con,"\r\n");      # get echo
    s = readline.read(Con,"\r\n");
    if s == 'ERROR': raise pyDCPU.ModuleError("Mobile-phone returned error!");
    readline.read(Con,"\r\n");      # read empty line
    if not readline.read(Con,"\r\n") == 'OK':
        raise pyDCPU.ModuleError("Mobile-phone returned error!");
    return(s);

def GetModel(Con):
    Con.write('AT+CGMM\r\n');
    readline.read(Con,"\r\n");      # get echo
    s = readline.read(Con,"\r\n");
    if s == 'ERROR': raise pyDCPU.ModuleError("Mobilephone returned error.");
    readline.read(Con,"\r\n");      # get empty line;
    if not readline.read(Con,"\r\n") == 'OK':
        raise pyDCPU.ModuleError("Mobile-phone returned ERROR.");
    return(s);
    
def GetQuality(Con):
    Con.write('AT+CSQ\r\n');
    readline.read(Con,"\r\n");      # get echo
    tmp = readline.read(Con,"\r\n");
    if tmp == 'ERROR': raise pyDCPU.ModuleError("Mobile-phone returned Error");
    readline.read(Con,"\r\n");      # read empty line
    if not readline.read(Con,"\r\n") == 'OK':
        raise pyDCPU.ModuleError("MobilePhone returned error.");
    tq = tmp.split(' ')[1];
    q = tq.split(',');
    return(q);

def GetBattery(Con):
    Con.write('AT+CBC\r\n');
    readline.read(Con,"\r\n");      # get echo
    tmp = readline.read(Con,"\r\n");
    if tmp == 'ERROR': raise pyDCPU.ModuleError("Mobile-phone returned error.");
    readline.read(Con,"\r\n");      # read empty line
    if not readline.read(Con,"\r\n") == 'OK':
        raise pyDCPU.ModuleError("Mobile-phone returned error");
    tq = tmp.split(' ')[1];
    q = tq.split(',')[1];
    return(q);

def GetNetwork(Con):
    Con.write('AT+CREG?\r\n');
    readline.read(Con,"\r\n");      # get echo
    tmp = readline.read(Con,"\r\n");
    if tmp == 'ERROR': raise pyDCPU.ModuleError("MobilePhone returned error!");
    readline.read(Con,"\r\n");      # read empty line;
    if not readline.read(Con,"\r\n") == 'OK':
        raise pyDCPU.ModuleError("Mobile phone returned error.");
    tq = tmp.split(' ');
    if len(tq)>1: q = tq[1].split(',');
    else: raise pyDCPU.ModuleError("Mobilephone returned mad format!");
    return(q);

def SendSMS(Con, Dest, Msg):
    logger = logging.getLogger("pyDCPU");
    sms = GSMSMS.PDUSMS(Dest,Msg);
    data = sms.SMSToHex();

    if not data: raise Exception("No data given to send!");
    logger.debug("SMSPDU(hex): %s"%data);
    Con.write("AT+CMGS=%i\r%s\x1A"%(int(len(data)/2),data));
    logger.debug("SMS \"%s\" send..."%Msg);
    readline.read(Con,"\r\n"); #get echo
    readline.read(Con,"\r\n");
    tmp = readline.read(Con,"\r\n");
    logger.debug("Phone returned: %s"%str(tmp));
    if not 0 == tmp.find('+CMGS:'):
        raise Exception("Error while send sms \"%s\" to %s."%(tmp,Dest));
    return(True);
