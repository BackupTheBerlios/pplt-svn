import re;
import sys;


IEC_INPUT = 1;
IEC_OUTPUT= 2;
IEC_MERKER= 3;
IEC_BOOL  = 10;
IEC_WORD  = 12;
IEC_DWORD = 13;

class NAIS_IEC_Address:
    def __init__(self, AddrStr):
        EA_RE = "^%(I|Q)((X)([0-9]+)\.([0-9]+)$|(W)([0-9]+)$)" #re 
        IECRE = "^%(M)((W|D)([1-6,8,9]|10).([0-9]+)$|(X)(0|7|11).([0-9]+).([0-9]+)$)"
        self.__Valid = True;
        self.__AREA  = None;
        self.__TYPE  = None;
        self.__SEGMENT = None;
        self.__MAJOR = None;
        self.__MINOR = None;

        iecre = re.compile(IECRE);
        ea_re = re.compile(EA_RE);

        m = ea_re.match(AddrStr);
        if not m:
            m = iecre.match(AddrStr);
            if not m:
                print "Invalid";
                self.__Valid = False;

        if self.__Valid:
            mod = m.group(1);
            if mod == 'I':
                self.__AREA = IEC_INPUT;
            elif mod == 'Q':
                self.__AREA = IEC_OUTPUT;
            elif mod == 'M':
                self.__AREA = IEC_MERKER;
            else:
                self.__Valid = False;

        if self.__Valid  and ((self.__AREA == IEC_INPUT) or (self.__AREA == IEC_OUTPUT)):
            if m.group(3) == 'X':
                self.__TYPE = IEC_BOOL;
                self.__MAJOR = int(m.group(4));
                self.__MINOR  = int(m.group(5));
                self.__SEGMENT = None;
            elif m.group(6) == 'W':
                self.__TYPE = IEC_WORD;
                self.__SEGMENT = None;
                self.__MAJOR = int(m.group(7));
                self.__MINOR = None;
            else:
                print "not %s nor %s"%(m.group(3),m.group(6))
                self.__Valid = False;

        if self.__Valid and (self.__AREA == IEC_MERKER):
            if m.group(3) == 'W':
                self.__TYPE = IEC_WORD;
            elif m.group(3) == 'D':
                self.__TYPE = IEC_DWORD;
            elif m.group(6) == 'X':
                self.__TYPE = IEC_BOOL;
            else:
                self.__TYPE = None;
            
            if self.__TYPE == IEC_WORD or self.__TYPE == IEC_DWORD:
                self.__SEGMENT = int(m.group(4));
                self.__MAJOR   = int(m.group(5));
                self.__MINOR   = None;
            elif self.__TYPE == IEC_BOOL:
                self.__SEGMENT = int(m.group(7));
                self.__MAJOR   = int(m.group(8));
                self.__MINOR   = int(m.group(9));
            
    def IsValid(self):
        return(self.__Valid);
    def GetArea(self):
        return(self.__AREA);
    def GetType(self):
        return(self.__TYPE);
    def GetSegment(self):
        return(self.__SEGMENT);
    def GetMajor(self):
        return(self.__MAJOR);
    def GetMinor(self):
        return(self.__MINOR);





ADDR = NAIS_IEC_Address("%MX1.1");

if ADDR.IsValid():
    print ADDR.GetArea();
    print ADDR.GetType();
    print ADDR.GetSegment();
    print ADDR.GetMajor();
    print ADDR.GetMinor();
