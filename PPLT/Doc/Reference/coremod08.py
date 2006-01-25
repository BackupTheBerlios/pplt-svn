import pyDCPU;

core = pyDCPU.Core();

# setup serial interface:
serID = core.MasterTreeAdd(None, "Master.Interface.UniSerial", None,
                           {'Port':'0', 'Speed':'9600', 'Parity':'Even',
                            'TimeOut':'1.0'});

# setup PPI and attach to serial interface: 
# (PPI address of the PC is #0)
ppiID = core.MasterTreeAdd(serID, 'Master.Transport.PPI', None,
                           {'Address':'0'});

# setup S7 Module and attach to PPI:
# (PPI address of the S7 is #2)
s7ID = core.MasterTreeAdd(ppiID, 'Master.Device.S7', '2', None);

# create symbols:
core.SymbolTreeCreateSymbol("/sm_bit", s7ID, 'SM0.5');
core.SymbolTreeCreateSymbol("/ab0", s7ID, 'AB0');

# read/write symbols:
tmp = core.SymbolTreeGetValue('/ab0');
tmp ^= 0xff;    # invert
core.SymbolTreeSetValue('/ab0', tmp);

print core.SymbolTreeGetValue("/sm_bit");
