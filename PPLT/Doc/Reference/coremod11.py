import pyDCPU;

# init core:
core = pyDCPU.Core();

# load serial interface:
serID = core.MasterTreeAdd(None, "Master.Inteface.UniSerial", None
                           {'Port':'0','Speed':'19200','Parity':'Odd',
                            'TimeOut':'1.0'});

# load readline because the MEWTOCOL-COM works line-wise:
rlID  = core.MasterTreeAdd(serID, 'Master.Transport.ReadLine', None,
                           {'LineEnd':'0D'});

# load MEWCOM-TL transport-layer:
mtlID = core.MasterTreeAdd(rlID,  'Master.Transport.MEWCOM-TL', None,
                           {'BCC':'True'});

# load MEWCOM-CL command-messages:
mclID = core.MasterTreeAdd(mtlID, 'Master.Device.MEWCOM-CL', "1", None);

# create symbols:
core.SymbolTreeCreateSymbol("/state", mclID, "STATUS");
core.symbolTreeCreateSymbol("/Y0", mclID, "Y0");

# set PLC into "run":
core.SymbolTreeSetValue("/state", True);

# set output bit 1 to True:
core.SymbolTreeSetValue("/Y0", True);
