# ############################################################################ #
# This is part of the pyDCPU project. pyDCPU is a framework for industrial     # 
#   communication.                                                             # 
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
import logging;


class Converter:
    def __init__(self, Type):
        self.__TypeName = Type;
        self.__Logger = logging.getLogger('pyDCPU');
        
        if Type == 'Bool':
            self.__D2VConverter = D2VBool;
            self.__V2DConverter = V2DBool;
            self.__Size = 1;
            self.__State = True;
        elif Type == 'Byte':
            self.__D2VConverter = D2VByte;
            self.__V2DConverter = V2DByte;
            self.__Size = 1;
            self.__State = True;
        elif Type == 'Word':
            self.__D2VConverter = D2VWord;
            self.__V2DConverter = V2DWord;
            self.__Size = 2;
            self.__State = True;
        elif Type == 'DWord':
            self.__D2VConverter = D2VDWord;
            self.__V2DConverter = V2DDWord;
            self.__Size = 4;
            self.__State = True;
        elif Type == 'Float':
            self.__D2VConverter = D2VFloat;
            self.__V2DConverter = V2DFloat;
            self.__Size = 4; #FIXME: Size = ????
            self.__State = True;
        elif Type == 'Double':
            self.__D2VConverter = D2VDouble;
            self.__V2DConverter = V2DDouble;
            self.__Size = 8; #FIXME: Size=????
            self.__State = True;
        elif Type == 'String':
            self.__D2VConverter = D2VString;
            self.__V2DConverter = V2DString;
            self.__Size = 1024;
            self.__State = True;
        else:
            self.__D2VConverter = None;
            self.__V2dConverter = None;
            self.__Size = 1024;
            self.__State = False;
            self.__TypeName = None;



    def GetState(self):
        return(self.__State);
    def GetSize(self):
        return(self.__Size);

    
    def ConvertToData(self, Value):
        return(self.__V2DConverter(Value));
    def ConvertToValue(self, Data):
        if not Data:
            return(None);
        #ignore size if type = string
        if not self.__TypeName == 'String':
            if not len(Data) == self.__Size:
                return(None);
        return(self.__D2VConverter(Data));
    




def D2VBool(Data):
    if not Data:
        return(None);
    if not len(Data) == 1:
        return(None);
    (Value,) = struct.unpack('B',Data);
    if Value:
        return(True);
    return(False);
def V2DBool(Value):
    if Value:
        return(struct.pack('B',1));
    else:
        return(struct.pack('B',0));


def D2VByte(Data):
    (Value,) = struct.unpack('B',Data);
    return(Value);
def V2DByte(Value):
    if Value == None:
        return(None);
    Value = int(Value) % 256;
    return(struct.pack('B',Value));


def D2VWord(Data):
    (Value,) = struct.unpack('H',Data);
    return(Value);
def V2DWord(Value):
    if Value == None:
        return(None);
    Value = int(Value) %256;
    return(struct.pack('H',Value));


def D2VDWord(Data):
    (Value,) = struct.unpack('I',Data);
    return(Value);
def V2DDWord(Value):
    if Value == None:
        return(None);
    return(struct.pack('I',int(Value)));


def D2VFloat(Data):
    (Value,) = struct.unpack('f',Data);
    return(Value);
def V2DFloat(Value):
    if Value == None:
        return(None);
    return(struct.pack('f',float(Value)));


def D2VDouble(Data):
    (Value,) = struct.unpack('d',Data);
    return(Value);
def V2DDouble(Value):
    if Value == None:
        return(None);
    return(struct.pack('d',float(Value)));

def D2VString(Data):
    return(Data);
def V2DString(Value):
    return(str(Value));
