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

# CHANGELOG:
# 2005-09-23: 
#   Changed value conversion to XDR


import pyDCPU;
import time;
import struct;
import xdrlib;

"""
    This module collects statistic information about the data
    going throug it.
    The module that wants to access the underlaying modules have
    to be connected to this module with the address "tunnel".
    Addresses and meaning:
    'tunnel'                =>  the data tunnel
    'read_data'             =>  the number of bytes readed
    'write_data'            =>  the number of bytes written
    'read_speed'            =>  the abr. bytes per second by reading 
    'write_speed'           =>  the abr. bytes per second by writing
    'error'                 =>  count the number of errors
"""

CHANEL_DATA     = 0;
CHANEL_RD       = 1;
CHANEL_WD       = 2;
CHANEL_RS       = 3;
CHANEL_WS       = 4;
CHANEL_E        = 10;

class Object(pyDCPU.MasterObject):
    def setup(self):
        self.Logger.debug('Setup statistic module')
        if not isinstance(self.Connection, pyDCPU.MasterConnection):
            self.Logger.error('This is not a root module -> no connection to parent');
            return(False);
        self.__ReadCount = 0;
        self.__WriteCount = 0;
        self.__StartTime = int(time.time());
        self.__ErrorCounter = 0;
        return(True);
        
    def connect(self, AddrStr):
        if AddrStr == 'tunnel':
            Con = pyDCPU.MasterConnection(self, CHANEL_DATA);
            self.Logger.debug("Connect to data tunnel");
            return(Con);
        elif AddrStr == 'read_data':
            Con = pyDCPU.MasterConnection(self, CHANEL_RD);
            self.Logger.debug("Connected to read bytes counter");
            return(Con);
        elif AddrStr == 'write_data':
            Con = pyDCPU.MasterConnection(self, CHANEL_WD);
            self.Logger.debug("Connected to write bytes counter");
            return(Con);
        elif AddrStr == 'read_speed':
            Con = pyDCPU.MasterConnection(self, CHANEL_RS);
            self.Logger.debug("Connected to abr. read speed-o-meter");
            return(Con);
        elif AddrStr == 'write_speed':
            Con = pyDCPU.MasterConnection(self, CHANEL_WS);
            self.Logger.debug("Connected to write speed-o-meter");
            return(Con);
        elif AddrStr == 'error':
            Con = pyDCPU.MasterConnection(self, CHANEL_E);
            self.Logger.debug('Connected to error counter');
            return(Con);
        else:
            self.Logger.error("Address \"%s\" unknown!"%str(AddrStr));
            return(None);
        return(None);
    

    def read(self, Connection, Length):
        if not isinstance(Connection, pyDCPU.MasterConnection):
            self.Logger.error("FATAL: Bad connection!!!");
            raise(pyDCPU.FatIOError);
        Chanel = Connection.Address;

        if Chanel == CHANEL_DATA:
            try:
                Data = self.Connection.read(Length);
            except pyDCPU.IOModError:
                self.__ErrorCounter += 1;
                self.Logger.error("IO Error");
                raise(pyDCPU.IOModError);
            except:
                self.Logger.error("Fat IO Error");
                raise(pyDCPU.FatIOError);
            if Data:
                self.__ReadCount += len(Data);
            return(Data);
        elif Chanel == CHANEL_RD:
            return(ConvToRaw(self.__ReadCount));
        elif Chanel == CHANEL_WD:
            return(ConvToRaw(self.__WriteCount));
        elif Chanel == CHANEL_RS:
            return( ConvToRaw(int( self.__ReadCount/(int(time.time())-self.__StartTime) )));
        elif Chanel == CHANEL_WS:
            return( ConvToRaw(int( self.__ReadCount/(int(time.time())-self.__StartTime) )));
        elif Chanel == CHANEL_E:
            return( ConvToRaw(self.__ErrorCounter) );
        else:
            self.Logger.error('Invalid chanel-number!!!');
            raise(pyDCPU.FatIOError);
        
    def write(self, Connection, Data):
        if Connection.Address == CHANEL_DATA:
            try:
                Ret = self.Connection.write(Data);
            except pyDCPU.IOModError:
                self.Logger.error("IO Error");
                raise(pyDCPU.IOModError);
            except:
                self.Logger.error("Fat IO Error");
                raise(pyDCPU.FatIOError);
            if Data:
                self.__WriteCount += len(Data);
            return(Ret);
        else:
            self.Logger.error("Statistic chanels are read only!");
            raise(pyDCPU.ReadOnlyModError);
        
    def flush(self):
        return(self.Connection.flush());


def ConvToRaw(Value):
    """ This function converts a integer value to it's memory representation """
    packer = xdrlib.Packer();
    packer.pack_int(Value);
    return(packer.get_buffer());
