import struct;
import re;
import string;


# SOURCE 
AGI_SRC_DIGI    = 1;
AGI_SRC_ANA     = 2;
AGI_SRC_MATH    = 3;
AGI_SRC_FORM    = 4;

AGI_CMD_FREQ    = 1;
AGI_CMD_PHASE   = 2;
AGI_CMD_AMP     = 3;
AGI_CMD_MAX     = 4;
AGI_CMD_MIN     = 5;
AGI_CMD_PP      = 6;
AGI_CMD_TOP     = 7;
AGI_CMD_BASE    = 8;
AGI_CMD_WIDTH   = 9;



class Source:
    def __init__(self, Primary, Secondary):
        RE = re.compile("^([D|A])([0-9]+)$|^([M|F])$");
        PME= RE.match(Primary);
        SME= RE.match(Secondary);

        self.__Valid = True;
        self.__PType = None;
        self.__SType = None;
        self.__PNumber = 0;
        self.__SNumber = 0;

        if PME:
            if PME.group(3) != None:
                if PME.group(3) == 'M':
                    self.__PType = AGI_SRC_MATH;
                elif PME.group(3) == 'F':
                    self.__PType = AGI_SRC_FORM;
                else:
                    self.__Valid = False;
            else:
                if PME.group(1) == 'D':
                    self.__PType = AGI_SRC_DIGI;
                elif PME.group(1) == 'A':
                    self.__PType = AGI_SRC_ANA;
                else:
                    self.__Valid = False;
                if self.__Valid:
                    try:
                        self.__PNumber = int(PME.group(2));
                    except:
                        self.__Valid = False;
        else:
            self.__Valid = False;
        if SME and self.__Valid:
            if SME.group(3) != None:
                if SME.group(3) == 'M':
                    self.__SType = AGI_SRC_MATH;
                elif SME.group(3) == 'F':
                    self.__SType = AGI_SRC_FORM;
                else:
                    self.__Valid = False;
            else:
                if SME.group(1) == 'D':
                    self.__SType = AGI_SRC_DIGI;
                elif SME.group(1) == 'A':
                    self.__Sype = AGI_SRC_ANA;
                else:
                    self.__Valid = False;
                if self.__Valid:
                    try:
                        self.__SNumber = int(SME.group(2));
                    except:
                        self.__Valid = False;
        else:
            self.__Valid = False;
            
        
    def GetPrimaryString(self):
        if self.__PType == AGI_SRC_MATH:
            return('M');
        elif self.__PType == AGI_SRC_FORM:
            return('F');
        elif self.__PType == AGI_SRC_DIGI:
            return('DIG%i'%self.__PNumber);
        elif self.__PType == AGI_SRC_ANA:
            return('CHAN%i'%self.__PNumber);
        return('');
    
    def GetSecondaryString(self):
        if self.__PType == AGI_SRC_MATH:
            return('M');
        elif self.__PType == AGI_SRC_FORM:
            return('F');
        elif self.__PType == AGI_SRC_DIGI:
            return('DIG%i'%self.__PNumber);
        elif self.__PType == AGI_SRC_ANA:
            return('CHAN%i'%self.__PNumber);
        return('');

    def IsValid(self):
        return(self.__Valid);


def GetFreq(Connection, Sources):
    cmd = "MEAS:FREQ? %s"%Sources.GetPrimaryString();
    Connection.write(cmd);
    ret = Connection.read(13);
    return(float(ret));

def GetPhase(Con, Src):
    cmd = "MEAS:PHAS? %s,%s"%(Src.GetPrimaryString(), Src.GetSecondaryString());
    Con.write(cmd);
    ret = Con.read(13);
    return(float(ret));

def GetAmp(Con, Src):
    cmd = "MEAS:VAMP? %s"%Src.GetPrimaryString();
    Con.write(cmd);
    ret = Con.read(13);
    return(float(ret));

def GetMax(Con, Src):
    cmd = "MEAS:VMAX? %s"%Src.GetPrimaryString();
    Con.write(cmd);
    ret = Con.read(13);
    return(float(ret));

def GetMin(Con, Src):
    cmd = "MEAS:VMIN? %s"%Src.GetPrimaryString();
    Con.write(cmd);
    ret = Con.read(13);
    return(float(ret));

def GetPP(Con, Src):
    cmd = "MEAS:VPP? %s"%Src.GetPrimaryString();
    Con.write(cmd);
    ret = Con.read(13);
    return(float(ret));

def GetTop(Con, Src):
    cmd = "MEAS:VTop? %s"%Src.GetPrimaryString();
    Con.write(cmd);
    ret = Con.read(13);
    return(float(ret));

def GetWidth(Con, Src):
    cmd = "MEAS:NWID? %s"%Src.GetPrimaryString();
    Con.write(cmd);
    ret = Con.read(13);
    return(float(ret));

def PackDouble(Value):
    return( struct.pack("d",float(Value)) );
