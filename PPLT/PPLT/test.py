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








FPWEB = Core.MasterTreeAdd(None, 'Master.If.Socket', None, {'TimeOut':'1.0'});
if not FPWEB:
    print "Error while Serial";
    sys.exit();

FP2RL = Core.MasterTreeAdd(FPWEB, 'Master.Trans.ReadLine', '172.17.15.112:9094',{'LineEnd':'0D'});
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

fp0_x0 = Core.MasterTreeAttachSymbolSlot(MEWCL, 'X0', 'Bool', TimeOut=0.1);
fp0_x1 = Core.MasterTreeAttachSymbolSlot(MEWCL, 'X1', 'Bool', TimeOut=0.1);
fp0_y0 = Core.MasterTreeAttachSymbolSlot(MEWCL, 'Y0', 'Bool', TimeOut=0.1);
fp0_y1 = Core.MasterTreeAttachSymbolSlot(MEWCL, 'Y1', 'Bool', TimeOut=0.1);
fp0_run= Core.MasterTreeAttachSymbolSlot(MEWCL, 'STATUS', 'Bool', TimeOut=0.1);

Core.SymbolTreeCreateFolder('fp0');
Core.SymbolTreeCreateSymbol('/fp0/x0', fp0_x0, 'Bool');
Core.SymbolTreeCreateSymbol('/fp0/x1', fp0_x1, 'Bool');
Core.SymbolTreeCreateSymbol('/fp0/y0', fp0_y0, 'Bool');
Core.SymbolTreeCreateSymbol('/fp0/y1', fp0_y1, 'Bool');
Core.SymbolTreeCreateSymbol('/fp0/run', fp0_run, 'Bool');



S55Com = Core.MasterTreeAdd(None, 'Master.If.UniSerial', None, {'Port':'2',
                                                               'Speed':'115200',
                                                               'Parity':'None',
                                                               'TimeOut':'1.0'})
if not S55Com:
    print "s55com error";
    sys.exit();


S55RL = Core.MasterTreeAdd(S55Com, 'Master.Trans.ReadLine', None, {'LineEnd':'0D0A'});
if not S55RL:
    print "s55rl error";
    sys.exit();
S55ID = Core.MasterTreeAdd(S55RL, 'Master.Dev.GSM', None, {});
if not S55ID:
    print "s55id error";
    sys.exit();
    
s55_bat = Core.MasterTreeAttachSymbolSlot(S55ID, 'battery', 'DWord', TimeOut=2.0);
s55_qual = Core.MasterTreeAttachSymbolSlot(S55ID, 'quality', 'DWord', TimeOut=2.0);
s55_manu = Core.MasterTreeAttachSymbolSlot(S55ID, 'manufacturer', 'String', TimeOut=2.0);
s55_model = Core.MasterTreeAttachSymbolSlot(S55ID, 'model', 'String', TimeOut=2.0);

Core.SymbolTreeCreateFolder("s55");
Core.SymbolTreeCreateSymbol('/s55/bat', s55_bat, 'DWord');
Core.SymbolTreeCreateSymbol('/s55/qual', s55_qual, 'DWord');
Core.SymbolTreeCreateSymbol('/s55/manu', s55_manu, 'String');
Core.SymbolTreeCreateSymbol('/s55/mod', s55_model, 'String');





AGICOM = Core.MasterTreeAdd(None, 'Master.If.UniSerial', None,{'Port':'0',
                                                               'Speed':'57600',
                                                               'Parity':'None',
                                                               'TimeOut':'1.0'});

AGIRL = Core.MasterTreeAdd(AGICOM, 'Master.Trans.ReadLine', None, {'LineEnd':'0A'});
if not AGIRL:
    print "agirl error";
    sys.exit();

AGI = Core.MasterTreeAdd(AGIRL, 'Master.Dev.5462X', None, {'PSource':'A1','SSource':'A2'});
if not AGI:
    print "AGI error";
    sys.exit();

agi_amp = Core.MasterTreeAttachSymbolSlot(AGI, 'amp', 'Double',TimeOut=0.5);
agi_freq = Core.MasterTreeAttachSymbolSlot(AGI, 'freq', 'Double',TimeOut=0.5);
Core.SymbolTreeCreateFolder('agi');
Core.SymbolTreeCreateSymbol('/agi/amp', agi_amp, 'Double');
Core.SymbolTreeCreateSymbol('/agi/freq', agi_freq, 'Double');



if not Core.ExporterAdd('Server.JVisu', {'Address':'172.17.15.111','Port':'2200'}, 'admin'):
    print "Error while JV";
    sys.exit();

while 1:
    pass;
