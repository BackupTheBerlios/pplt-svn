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
# 2005-01-22:
#   changed to new connection-types and exceptions

import pyDCPU;
import time;

"""
    This module collects statistic information about the data
    going throug it.
    The module that wants to access the underlaying modules have
    to be connected to this module with the address "tunnel".
    Addresses and meaning:
    '' or None              =>  the data tunnel
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
        if not isinstance(self.Connection, (pyDCPU.StreamConnection, pyDCPU.SequenceConnection)):
            raise pyDCPU.ModuleError("This module needs a Stream or Sequence connection from parent!");
        self.__ReadCount = 0;
        self.__WriteCount = 0;
        self.__StartTime = int(time.time()-1);
        self.__ErrorCounter = 0;
        
    def connect(self, AddrStr):
        if AddrStr == '' or AddrStr == None:
            if isinstance(self.Connection, pyDCPU.StreamConnection):
                Con = pyDCPU.StreamConnection(self, CHANEL_DATA);
            else: Con = pyDCPU.SequenceConnection(self, CHANEL_DATA);
            self.Logger.debug("Connect to data tunnel");
            return(Con);
        elif AddrStr == 'read_data':
            Con = pyDCPU.ValueConnection(self, pyDCPU.TInteger, CHANEL_RD);
            self.Logger.debug("Connected to read bytes counter");
            return(Con);
        elif AddrStr == 'write_data':
            Con = pyDCPU.ValueConnection(self, pyDCPU.TInteger, CHANEL_WD);
            self.Logger.debug("Connected to write bytes counter");
            return(Con);
        elif AddrStr == 'read_speed':
            Con = pyDCPU.ValueConnection(self, pyDCPU.TFloat, CHANEL_RS);
            self.Logger.debug("Connected to abr. read speed-o-meter");
            return(Con);
        elif AddrStr == 'write_speed':
            Con = pyDCPU.ValueConnection(self, pyDCPU.TFloat, CHANEL_WS);
            self.Logger.debug("Connected to write speed-o-meter");
            return(Con);
        elif AddrStr == 'error':
            Con = pyDCPU.ValueConnection(self, pyDCPU.TInteger, CHANEL_E);
            self.Logger.debug('Connected to error counter');
            return(Con);
        raise pyDCPU.ModuleError("Unknown address: %s"%AddrStr);
    

    def read(self, Connection, Length=None):
        Chanel = Connection.Address;

        if Chanel == CHANEL_DATA:
            try: Data = self.Connection.read(Length);
            except Exception, e:
                self.__ErrorCounter += 1;
                raise e;
            self.__ReadCount += len(Data);
            return(Data);
        elif Chanel == CHANEL_RD: return self.__ReadCount;
        elif Chanel == CHANEL_WD: return self.__WriteCount;
        elif Chanel == CHANEL_RS: return (self.__ReadCount/(int(time.time())-self.__StartTime) );
        elif Chanel == CHANEL_WS: return (self.__WriteCount/(int(time.time())-self.__StartTime) );
        elif Chanel == CHANEL_E:  return self.__ErrorCounter;
        pyDCPU.ModuleError("Invalid Chanel number!");

    def write(self, Connection, Data):
        if Connection.Address == CHANEL_DATA:
            try: Ret = self.Connection.write(Data);
            except Exception, e:
                self.__ErrorCounter += 1;
                raise e;
            self.__WriteCount += len(Data);
            return(Ret);
        else: raise pyDCPU.ModuleError("Statistical values are read-only");
        
    def flush(self): return(self.Connection.flush());


