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

SMB28_slot = Core.MasterTreeAttachSymbolSlot(S7, 'SMB28', 'Byte', TimeOut=0.5);
SM05_slot  = Core.MasterTreeAttachSymbolSlot(S7, 'SM0.5', 'Bool', TimeOut=0.25);

Core.SymbolTreeCreateFolder('/s7');
Core.SymbolTreeCreateSymbol('/s7/potti', SMB28_slot, 'Byte');
Core.SymbolTreeCreateSymbol('/s7/takt', SM05_slot, 'Bool');






FPCOM = Core.MasterTreeAdd(None, 'Master.If.UniSerial', None, {'Port':'2',
                                                               'Speed':'19200',
                                                               'Parity':'Odd',
                                                               'TimeOut':'1.0'})
if not FPCOM:
    print "s7com error";
    sys.exit();


FP2RL = Core.MasterTreeAdd(FPCOM, 'Master.Trans.ReadLine', None ,{'LineEnd':'0D'});
if not FP2RL:
    print "fp2rl error";
    sys.exit();

MEWTL = Core.MasterTreeAdd(FP2RL, 'Master.Trans.MEWCOM-TL', None, {'BCC':'True'});
if not MEWTL:
    print "Error while MEWTOCOL-COM TL";
    sys.exit();

MEWCL = Core.MasterTreeAdd(MEWTL, 'Master.Dev.MEWCOM-CL', '01', {});
if not MEWCL:
    print "Error while MEWTOCOL-COM CL";
    sys.exit();


fp2_run= Core.MasterTreeAttachSymbolSlot(MEWCL, 'STATUS', 'Bool', TimeOut=0.1);
fp2_x0 = Core.MasterTreeAttachSymbolSlot(MEWCL, 'R901D', 'Bool', TimeOut=0.5);


Core.SymbolTreeCreateFolder('fp2');
Core.SymbolTreeCreateSymbol('/fp2/takt', fp2_x0, 'Bool');
Core.SymbolTreeCreateSymbol('/fp2/run', fp2_run, 'Bool');




if not Core.ExporterAdd('Server.JVisu', {'Address':'172.17.15.111','Port':'2200'}, 'admin'):
    print "Error while JV";
    sys.exit();

while 1:
    pass;

