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


# Revision:
# 2006-01-21:
#   + added "slots" to change settings at runtime
# 2005-02-04:
#   + raise execptions on io errors...
#

import serial;
import pyDCPU;

class Object(pyDCPU.MasterObject):
    """ This Class impl. a serial interface (UART) for the dcpu FrameWork """
    def setup(self):
        #
        # Init SerialInterface
        #
        self.Logger.info("Setup Serial Port");
        if not self.Parameters.has_key('Port'): raise pyDCPU.ModuleSetup("Can't setup SerialPort! No Port Number/Name");
        
        Port = self.Parameters['Port'];
        self.Logger.debug("Set Port to %s"%Port);
            
        if not self.Parameters.has_key('Speed'): raise pyDCPU.ModuleSetup("Can't setup SerialPort! No Speed");

        Speed = int(self.Parameters['Speed']);
        self.Logger.debug("Set Baudrate to %i"%Speed);

        if not self.Parameters.has_key('Parity'):
            Parity = serial.PARITY_NONE;
        elif self.Parameters['Parity'] == "Odd":
            Parity = serial.PARITY_ODD;
        elif self.Parameters['Parity'] == "Even":
            Parity = serial.PARITY_EVEN;
        else:
            Parity = serial.PARITY_NONE;
        
        if not self.Parameters.has_key('TimeOut'):
            TimeOut = None;
            self.Logger.debug("Set no time out");
        else:
            if self.Parameters['TimeOut'] == "":
                TimeOut = None;
                self.Logger.debug("Set no time out");
            else:
                TimeOut = float(self.Parameters['TimeOut']);
                self.Logger.debug("Set time out to %f"%TimeOut);

        self.SerObj = serial.Serial(port=int(Port),
                                    baudrate = Speed,
                                    parity = Parity,
                                    timeout = TimeOut);
                                    
        if not self.SerObj: raise pyDCPU.ModuleSetup("Error while setup Port...");

        self.SerObj.flush();
        return(True);
        

        

    def read(self, Connection, Len):
        if Connection.Address == 'speed':
            return self.SerObj.getBaudrate();
        elif Connection.Address == 'parity':
            par = self.SerObj.getParity();
            if par == 'N': return 'none';
            elif par == 'E': return 'even';
            return 'odd';
        elif Connection.Address == 'timeout':
            return self.SerObj.getTimeout();
        elif Connection.Address == None:    
            Data = self.SerObj.read(Len);
            if Data == '': raise pyDCPU.ModuleError("Timeout...");
            return(Data);
        raise pyDCPU.ModuleError("Unknown connection address: %s!!!"%Connection.Address);    


    def write(self, Connection, Data):
        if Connection.Address == 'speed':
            self.SerObj.setBaudrate(Data);
            return(1);
        elif Connection.Address == 'parity':
            if Data == 'even': self.SerObj.setParity('E');
            elif Data == 'odd': self.SerObj.setParity('O');
            elif Data == 'none': self.SerObj.setParity('N');
            return(1);
        elif Connection.Address == 'timeout':
            self.SerObj.setTimeout(Data);
            return(1);
        elif Connection.Address == None:    
            try: self.SerObj.write(Data);
            except Exception, e: raise pyDCPU.ModuleError("Unable to write to serial port: %s"%str(e));
            return(len(Data));
        raise pyDCPU.ModuleError("Unknown address: %s!!!"%Connection.Address);    
    

    def connect(self,Address):
        if Address == 'speed':
            Connection = pyDCPU.ValueConnection(self, pyDCPU.TInteger, 'speed');
        elif Address == 'parity':
            Connection = pyDCPU.ValueConnection(self, pyDCPU.TString, 'parity');
        elif Address == 'timeout':
            Connection = pyDCPU.ValueConnection(self, pyDCPU.TFloat, 'timeout');
        elif Address == '' or Address==None:
            Connection = pyDCPU.StreamConnection(self,None);
        else: raise pyDCPU.ModuleError("Address %s not known to connect to UniSerial!"%Address);     
        return(Connection);


    def flush(self):
        self.Logger.debug("Flushing serial device");
        try: self.SerObj.flush();
        except Exception,e : raise pyDCPU.ModuleError("Error while flush device: %s"%str(e));

    def destroy(self):
        try: self.SerObj.close();
        except: raise pyDCPU.ModuleError("Error while flush device: %s"%str(e));
        return(True);
