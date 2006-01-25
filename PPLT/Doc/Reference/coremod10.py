import pyDCPU;

# init core:
core = pyDCPU.Core(LogLevel='debug');

# load ECHO:
ecoID = core.MasterTreeAdd(None, "Master.Debug.Echo", None, None);

# load HexDump (and attach to ECHO):
hexID = core.MasterTreeAdd(ecoID, "Master.Debug.HexDump", None, None);

# load ReadLine (and attach to HexDump):
rlID  = core.MasterTreeAdd(hexID, "Master.Transport.ReadLine", None,
                           {"LineEnd":"3C454E443E0A"});     # HEX: <END>\n

# create symbol:
core.SymbolTreeCreateSymbol("/echo", rlID);

# write: 
core.SymbolTreeWrite("/echo", "Hello world");
#read sequence from /echo (there is no max length)
print core.SymbolTreeRead("/echo");
