import pyDCPU;

# setup core:
core = pyDCPU.Core(LogLevel="debug");

# setup NULL
nilID = core.MasterTreeAdd(None, "Master.Debug.Null", None, None);

# setup HexDump (to read the packages PPI will send)
hexID = core.MasterTreeAdd(nilID, "Master.Debug.HexDump", None, None);

# setup the PPI module:
ppiID = core.MasterTreeAdd(hexID, 'Master.Transport.PPI', None,
                           {'Address':'0'});

# create symbols:
# 'connects' to 'device' #2 in PPI BUS
core.SymbolTreeCreateSymbol("/ppi", ppiID, "2");

# write some stuff to PPI:
core.SymbolTreeWrite("/ppi", "Hallo Welt...");
