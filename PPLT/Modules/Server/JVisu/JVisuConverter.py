import pyDCPU;
from JVisuTypes import *;

def ToData(Value, Type):
    if Type == JVISU_TYP_BOOL:
        return(pyDCPU.V2DBool(Value));
    elif Type == JVISU_TYP_BYTE:
        return(pyDCPU.V2DByte(Value));
    elif Type == JVISU_TYP_WORD:
        return(pyDCPU.V2DWord(Value));
    elif Type == JVISU_TYP_DWORD:
        return(pyDCPU.V2DDWord(Value));
    elif Type == JVISU_TYP_FLOAT:
        return(pyDCPU.V2DFloat(Value));
    elif Type == JVISU_TYP_DOUBLE:
        return(pyDCPU.V2DDouble(Value));
    elif Type == JVISU_TYP_STRING:
        return(pyDCPU.V2DString(Value));
    else:
        return(None);


def ToValue(Value, Type):
    if Type == JVISU_TYP_BOOL:
        return(pyDCPU.D2VBool(Value));
    elif Type == JVISU_TYP_BYTE:
        return(pyDCPU.D2VByte(Value));
    elif Type == JVISU_TYP_WORD:
        return(pyDCPU.D2VWord(Value));
    elif Type == JVISU_TYP_DWORD:
        return(pyDCPU.D2VDWord(Value));
    elif Type == JVISU_TYP_FLOAT:
        return(pyDCPU.D2VFloat(Value));
    elif Type == JVISU_TYP_DOUBLE:
        return(pyDCPU.D2VDouble(Value));
    elif Type == JVISU_TYP_STRING:
        return(pyDCPU.D2VString(Value));
    else:
        return(None);
