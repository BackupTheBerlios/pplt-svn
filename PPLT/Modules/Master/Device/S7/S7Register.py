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


import re;


"""
    This package provides objects for splitting S7 address strings...
"""

S7RegS          = 0x0004;
S7RegSMarker    = 0x0005;
S7RegAE         = 0x0006;
S7RegInput      = 0x0081;
S7RegOutput     = 0x0082;
S7RegMarker     = 0x0083;

S7Bit           = 0x01;
S7BitSize       = 0x08;
S7Byte          = 0x02;
S7ByteSize      = 0x08;
S7Word          = 0x04;
S7WordSize      = 0x10;
S7DWord         = 0x06;
S7DWordSize     = 0x20;


class S7Register:
    def __init__(self,S7AddrStr):
        self.__Area = 0;
        self.__Type = 0;
        self.__Size = 0;
        self.__Major = 0;
        self.__Minor = 0;

        exp = '^(AE|A|E|M|SM|S)(B|W|D|\d{1,}\.)(\d{1,})';

        rex = re.compile(exp);
        match = rex.match(S7AddrStr);
        if not match:
            return(None);

        Area = match.group(1);
        Type = match.group(2);
        if Type != 'B' and Type != 'W' and Type != 'D':
            self.__Major = int(Type[:len(Type)-1]);
            self.__Minor = int(match.group(3));
            Type = None;
        else:
            self.__Major= int(match.group(3));
            self.__Minor = 0;

        #FIXME: Beautify
        if Area == 'A':
            #OUTPUT
            self.__Area = S7RegOutput;
        elif Area == 'E':
            #INPUT
            self.___Area = S7RegInput;
        elif Area == 'M':
            #Marker
            self.__Area = S7RegMarker;
        elif Area == 'SM':
            #Sp. Marker
            self.__Area = S7RegSMarker;
        elif Area == 'AE':
            #AE
            self.__Area = S7RegAE;
        elif Area == 'S':
            #S
            self.__Area = S7RegS;

        if Type == None:
            #Bit
            self.__Type = S7Bit;
            self.__Size = S7BitSize;
        elif Type == 'B':
            #Byte
            self.__Type = S7Byte;
            self.__Size = S7ByteSize;
        elif Type == 'W':
            #Word
            self.__Type = S7Word;
            self.__Size = S7WordSize;
        elif Type == 'D':
            #DWord
            self.__Type = S7DWord;
            self.__Size = S7DWordSize;





    def GetArea(self):
        return(self.__Area);
    def GetMajor(self):
        return(self.__Major);
    def GetMinor(self):
        return(self.__Minor);
    def GetType(self):
        return(self.__Type);
    def GetSize(self):
        return(self.__Size);

