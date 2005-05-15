import pyDCPU;
import sys;
import time;
import binascii;
import re;




Core = pyDCPU.Core(ModuleDBFile = 'C:\PYTHON23\PPLT\ModuleDB.xml',
                   UserDBFile = 'C:\PYTHON23\PPLT\UserDB.xml',
                   LogLevel = 'info',
                   LogFile = None,#'log.log',
                   SysLog = False);


S7Com = Core.MasterTreeAdd(None, 'Master.If.UniSerial', None, {'Port':'0',
                                                               'Speed':'9600',
                                                               'Parity':'Even',
                                                               'TimeOut':'1.0'})
if not S7Com:
    print "s7com error";
    sys.exit();

PPI = Core.MasterTreeAdd(S7Com, 'Master.Trans.PPI', None, {'Address':'0'});
if not PPI:
    print "ppi error";
    sys.exit();

S7 = Core.MasterTreeAdd(PPI, 'Master.Dev.S7', '2', {});
if not S7:
    print "S7 error";
    sys.exit();

AB0_slot  = Core.MasterTreeAttachSymbolSlot(S7, 'AB0', 'Byte', TimeOut=0.25);

Core.SymbolTreeCreateFolder('/s7');
Core.SymbolTreeCreateSymbol('/s7/AB0', AB0_slot, 'Byte');

Value = 0;
while True:
    Core.SymbolTreeSetValue('/s7/AB0',Value);
    Value = Value << 1;
    if not Value & 0x63:
        Value |= 1;
