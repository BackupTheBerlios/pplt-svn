import re

NAIS_INPUT = 1;
NAIS_OUTPUT= 2;
NAIS_MERKER= 3;
NAIS_LINK  = 4;
NAIS_DATA  = 5;
NAIS_FILE  = 6;
NAIS_LINKREG=7;
NAIS_STATUS=10;

NAIS_BOOL  = 1;
NAIS_WORD  = 3;
NAIS_DWORD = 4;

AreaCode= {NAIS_INPUT:'X',
           NAIS_OUTPUT:'Y',
           NAIS_MERKER:'R',
           NAIS_LINK:'L',
           NAIS_DATA:'D',
           NAIS_FILE:'F',
           NAIS_LINKREG:'L'};


class NAIS_Address:
    def __init__(self, AddrStr):
        RE = "^(W|)(X|Y|R|L)([0-9,A-F]+)$|^(D|)(DT|FL|LD)([0-9]+)$"

        self.__Valid    = True;
        self.__Area     = None;
        self.__Segment  = None;
        self.__Offset   = None;
        self.__Size     = None;

        if AddrStr == 'STATUS':
            self.__Area = NAIS_STATUS;
            self.__Size = NAIS_BOOL;
            self.__Segment = 0;
            self.__Offset = 0;
            return;

        m = re.compile(RE).match(AddrStr);
        if not m:
            #logger
            print ("Invalid: %s"%AddrStr);
            self.__Valid = False;

        if self.__Valid:
            t = m.group(1);
            if t == '':
                self.__Size = NAIS_BOOL;
            elif t == 'W':
                self.__Size = NAIS_WORD;

            t = m.group(4);
            if t == '':
                self.__Size = NAIS_WORD;
            elif t == 'D':
                self.__Size = NAIS_DWORD;


            a = m.group(2);
            if a == 'X':
                self.__Area = NAIS_INPUT;
            elif a == 'Y':
                self.__Area = NAIS_OUTPUT;
            elif a == 'R':
                self.__Area = NAIS_MERKER;
            elif a == 'L':
                self.__Area = NAIS_LINK;

            a = m.group(5);
            if a == 'DT':
                self.__Area = NAIS_DATA;
            elif a == 'FL':
                self.__Area = NAIS_FILE;
            elif a == 'LD':
                self.__Area = NAIS_LINKREG;

            if self.__Size == NAIS_BOOL:
                s = m.group(3);
                if len(s) == 1:
                    self.__Segment = 0;
                    self.__Offset  = int(s,16);
                else:
                    self.__Segment = int(s[:-1]);
                    self.__Offset  = int(s[-1:],16);
            elif m.group(3):
                s = m.group(3);
                try:
                    self.__Segment = int(s);
                except:
                    self.__Valid = False;
                self.__Offset  = 0;
            elif m.group(6):
                s = m.group(6);
                self.__Segment = int(s);
                self.__Offset  = 0;

    def IsValid(self):
        return(self.__Valid);
    def GetArea(self):
        return(self.__Area);
    def GetSegment(self):
        return(self.__Segment);
    def GetOffset(self):
        return(self.__Offset);
    def GetSize(self):
        return(self.__Size);
    
